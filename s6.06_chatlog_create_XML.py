'''
    Script s6.03 | v1.0.0 | consult <https://catlism.github.io> for more info.
    part of Di Cristofaro, Matteo. Corpus Approaches to Language in Social Media. New York: Routledge, 2023. https://doi.org/10.4324/9781003225218.
    Copyright (C) 2023 Matteo Di Cristofaro

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# Import (in order) the modules to: read/write CSV files; find files using regular expressions;
# work with regular expressions; generate random strings; to generate random numbers; randomise data;
# create dictionaries (the 'defaultdict' has the ability to handle missing data in dictionaries,
# in contrast to Python's default dictionary); read/write XML files
import csv
import glob
import re
import string
from random import randint
import random
from collections import defaultdict
from lxml import etree

# List all CSV files in the current folder
csvfiles = glob.glob("*.csv")

# Create two dictionaries: one ('user_types_dict') to store usernames mapped against their 'role' (g = groomer, d = decoy);
# the other ('timings_dict') to store usernames mapped against the total amount of time it interacted with one or more decoys
user_types_dict = defaultdict(list)
timings_dict = defaultdict(list)

# Open the metadata file (named .cs to avoid being read as a CSV chat log file) and read it as a csv file
metadata_file = csv.reader(
    open("metadata_file.cs", "r", encoding="utf-8"), delimiter="\t"
)
# For each row, do:
for row in metadata_file:
    # Read the username and its role and add the information to the dictionary 'user_types_dict'
    user_types_dict[row[0].lower()].append(row[1])
    # Read the total amount of time a groomer interacted with a decoy, and assign the value to the dictionary 'timings_dict'
    timings_dict[row[0].lower()].append(row[2])


# Create a function to add the type (g or d) to the username passed to the function during the data processing
def get_user_type(text):
    # Read the username, convert it to lowercase, and store it in the variable 'user'
    user = text.lower()
    # If 'user' is found in 'user_types_dict', extract its type label and store it in the variable 'usertype'
    if user in user_types_dict:
        usertype = str(user_types_dict[user][0])
    # Else if not found, assign the value 'na' to the variable 'usertype'
    else:
        usertype = "na"
    # Output the value of 'usertype'
    return usertype


# Create a function to add the total time of interaction to the corpus during the data processing, using the same rationale and
# operations employed in 'get_user_type'
def get_user_timing(text):
    username = text.lower()
    if username in timings_dict:
        timing = str(timings_dict[username])
    else:
        timing = "na"
    return timing


# Build the emoticons conversion steps; adapted from the emoticons.py function by Brendan O'Connor
# https://github.com/aritter/twitter_nlp/blob/65f3d77134c40d920db8d431c5c6faef1c051c94/python/emoticons.py
# Define the regular expression that will be used during the data processing to identify emoticons
regex_compile = lambda pat: re.compile(pat, re.UNICODE)
# Define the characters for eyes, nose, mouth to be used in the regular expressions; each
NormalEyes = r"[:=]"
Wink = r"[;]"
NoseArea = r"(|o|O|-)"
HappyMouths = r"[D\)\]]"
SadMouths = r"[\(\[]"
KissMouths = r"[\*]"
Tongue = r"[pP]"

# Construct the possible combinations into regular expressions
happysmiley_regex = (
    "("
    + NormalEyes
    + "|"
    + Wink
    + ")"
    + NoseArea
    + "("
    + HappyMouths
    + "|"
    + Tongue
    + ")"
)
sadsmiley_regex = "(" + NormalEyes + "|" + Wink + ")" + NoseArea + "(" + SadMouths + ")"
kisssmiley_regex = (
    "(" + NormalEyes + "|" + Wink + ")" + NoseArea + "(" + KissMouths + ")"
)
# Compile the regular expressions using the previously defined 'regex_compile'
happysmiley_compile = regex_compile(happysmiley_regex)
sadsmiley_compile = regex_compile(sadsmiley_regex)
kisssmiley_compile = regex_compile(kisssmiley_regex)

# Define the root <corpus> XML element tag of the output file
corpus = etree.Element("corpus")

# For each CSV chat log file, do:
for csvfile in csvfiles:
    # Create the <text> root element tag as child of the <corpus> root element
    text_tag = etree.SubElement(corpus, "text")

    # Create a function to generate a random ID using the 'random_number' variable (defined further below), plus a
    # set of randomly chosen letters
    def id_generator(N):
        return "".join(
            random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N
            )
        )

    # Generate a random number to be used for the creation of the unique <text> ID
    random_number = str(randint(0, 100000000))
    # Generate a random ID and assign it as value of the <text> attribute 'id'
    text_tag.attrib["id"] = str(id_generator(10) + random_number)

    # Create an empty list to store the usernames found in the chat log
    usernames_list = []

    # Open the chat log file and read it as a csv file
    input_csv = csv.reader(open(csvfile, "r", newline="", encoding="utf-8"))
    # Store the filename without extension inside the variable 'filename_without_csv'
    filename_without_csv = csvfile.replace(".csv", "")
    # Skip the first line of the CSV chat log file containing the columns header
    next(input_csv, None)
    # Iterate over each row and store them inside of the variable 'rows'
    rows = [r for r in input_csv]
    # For each row, count its position (starting from 1; this is equal to the turn number in the chat) and store it in
    # the variable 'line_number', then do:
    for line_number, row in enumerate(rows, start=1):
        # Create the <u> element tag for the chat turn (i.e. the chat message)
        turn_tag = etree.SubElement(text_tag, "u")
        # Assign the row position in the csv file as value of the <u> attribute 'turn'
        turn_tag.attrib["turn"] = str(line_number)
        # Read the username from the first column of the chat log file, clean it from any potential leading or trailing whitespace,
        # and assign it as value of the <u> attribute 'username'
        turn_tag.attrib["username"] = str(row[0]).strip()
        # Write the username (without any potential whitespace) to the list of usernames for this chat log
        usernames_list.append(str(row[0]).strip())
        # Read the timestamp from the third column of the chat log file and assign it as value of the <u> attribute 'time'
        turn_tag.attrib["time"] = str(row[2])
        # Read the date on which the message was sent from the fourth column of the chat log file, and assign it as value of
        # the <u> attribute 'date'
        turn_tag.attrib["date"] = str(row[3])
        # Using the 'get_user_type' function with the username as input, extract the type of user and assign it as value of the
        # <u> attribute 'usertype'
        turn_tag.attrib["usertype"] = get_user_type(str(row[0]).strip())
        # Read the chat message from the second column of the chat log file and store it inside a variable
        message = row[1]
        # Test for the presence of emoticons in the message using the three previously compiled regular expressions, and if found substitute it with the respective substitution-label (§_HAPPY-SMILEY_§, §_SAD-SMILEY_§, or §_KISS-SMILEY_§)
        if happysmiley_compile.search(message):
            message = re.sub(happysmiley_compile, " §HAPPY-SMILEY§ ", message)
        elif sadsmiley_compile.search(message):
            message = re.sub(sadsmiley_compile, " §SAD-SMILEY§ ", message)
        elif kisssmiley_compile.search(message):
            message = re.sub(kisssmiley_compile, " §KISS-SMILEY§ ", message)
        # Assign the formatted message as text of the <u> element tag
        turn_tag.text = message

    # Read all the unique values in the list of usernames, and for each one do:
    for username in set(usernames_list):
        # Get the user type
        user_type = get_user_type(username)
        # If the user type is equal to 'g' (i.e. groomer), get the total amount of time they spent chatting and assign it to
        # the <text> attribute 'timing', and add the groomer's username as value of the <text> attribute 'user'
        if user_type == "g":
            text_tag.attrib["timing"] = re.sub(
                "(\[|\]|')", "", get_user_timing(username)
            )
            text_tag.attrib["user"] = username

# Create the XML structure by adding all the extracted elements to the main 'corpus' tag
tree = etree.ElementTree(corpus)
# The resulting XML structure is written to the XML file named after the original CSV chat log file using utf-8 encoding,
# adding the XML declaration at the beginning and graphically formatting the layout ('pretty_print')
tree.write(
    filename_without_csv + ".xml",
    pretty_print=True,
    xml_declaration=True,
    encoding="utf-8",
)