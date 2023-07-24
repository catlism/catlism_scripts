# Import the required modules to read/write csv and xml files; and to read/write XML files
import csv
from lxml import etree

# Create the root element of the XML structure - <corpus> -, which will contain all the extracted tweets
# as elements defined by the <text> element tag (one tweet = one text)
corpus = etree.Element("corpus")

# Open the csv file containing the data collected by twint
csv_data = open("twint_output.csv", "r", newline="", encoding="utf-8")
# Read the content of the file, where each value is separated from the others by a tab (\t) character
csv_data_reader = csv.reader(csv_data, delimiter="\t")
# Skip the first row, containing the header
next(csv_data_reader, None)
# Create a list of all the rows and store it in the variable 'rows'
rows = [r for r in csv_data_reader]
# For each row in the list of rows, do:
for row in rows:
    # Extract each relevant value and store it inside a single variable, by indicating the
    # column number where the value is stored in the original data. Python counts from 0, so e.g. column
    # number 7 is read as number 6
    tweet_id = row[0]
    tweet_date = row[2]
    tweet_username = row[6]
    tweet_user_realname = row[7]
    tweet_content = row[10]
    # The following variables should contain the value 0 if no urls are included or the tweet is not a retweet,
    # and the value 1 when links are present or the tweet is a retweet. For urls, the script checks whether the length
    # of the original value is shorter than 3 characters (i.e. it only contains the empty square brackets), in which
    # case it assigns the value 0 as no value is present in the data. For 'tweet_isretweet' it checks if the word 'False'
    # appears in the data and assigns 0 if it does or 1 otherwise.
    tweet_urls_present = 0 if len(row[13]) < 3 else 1
    tweet_isretweet = 0 if row[21] == "False" else 1
    # The extracted values are assigned as values to the attributes of <text>.
    # The actual content of the tweet is then enclosed inside of <text> using the notation '.text'
    etree.SubElement(
        corpus,
        "text",
        id=str(tweet_id),
        csv_date_created=str(tweet_date),
        csv_username=str(tweet_username),
        csv_user_realname=str(tweet_user_realname),
        csv_urls_present=str(tweet_urls_present),
        csv_isretweet=str(tweet_isretweet),
    ).text = str(tweet_content)
# The XML structure is created by adding all the extracted elements to the main <corpus> element tag
tree = etree.ElementTree(corpus)
# The resulting XML structure is written to the output.xml file using utf-8 encoding, adding the XML declaration
# at the beginning and graphically formatting the layout ('pretty_print')
tree.write("twint_out.xml", pretty_print=True, xml_declaration=True, encoding="utf-8")