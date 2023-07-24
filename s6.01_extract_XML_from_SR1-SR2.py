# Import modules for:  loading files using regular expression; regular expressions; generating random numbers;
# using BeautifulSoup; reading timestamps as date objects; working with XML files
import glob
import re
from random import randint
from bs4 import BeautifulSoup
from dateutil import parser
from lxml import etree

# Create a dictionary with the replacement labels for the subfora names
replacements = {
    "bounties": "B01",
    "bug reports": "B02",
    "cryptocurrency": "B03",
    "customer support": "B04",
    "drug safety": "B05",
    "feature requests": "B06",
    "legal": "B07",
    "newbie discussion": "B08",
    "off topic": "B09",
    "philosophy, economics and justice": "B10",
    "press corner": "B11",
    "product offers": "B12",
    "product requests": "B13",
    "rumor mill": "B14",
    "security": "B15",
    "shipping": "B16",
    "silk road discussion": "B17",
    "the ross ulbricht case  &amp;  theories": "B18",
}

# Create the function to convert the subforum names into their equivalent (arbitrarily chosen) labels
def assign_subforum_label(text):
    # Remove any leading or trailing whitespace from the subforum name, and convert all letters to lower case
    text = text.lower()
    # Transform the name into its equivalent label, storing it into the variable 'label'
    label = replacements[text]
    # Return the variable 'label' as output
    return label


# Find all the files in the indicated subfolder, sorting them alphabetically
files = sorted(glob.glob("./SR2_files/*.*"))

# For each file in the list of files, do:
for file in files:
    # Create the main 'doc' element tag, which serves in the XML output as root element; here one separate 'doc' is created for
    # each original input file
    doc = etree.Element("doc")
    # Extract the name of the file excluding the leading "index.php?=" string, and store it inside the variable 'filename'
    filename = re.search("index.*\=(.*)", file).group(1).strip()
    # Assign it as value of the <doc> attribute 'filename'
    doc.attrib["filename"] = filename
    # Extract the numerical sequence appearing in the filename, to be later used as part of the XML 'id' attribute
    filename_number = re.search("index.*\=([0-9]{1,10})", file).group(1).strip()
    # Append a random number to the extracted 'filename_number' to generate a pseudo-random value for the <doc> element
    # tag 'id' attribute
    random_id = str(filename_number) + "_" + str(randint(0, 100000))
    # Assign the generated 'random_id' as value of the attribute 'id'
    doc.attrib["id"] = random_id
    # Open the input file
    f = open(file, encoding="utf-8")
    # Read the file with BeautifulSoup
    soup = BeautifulSoup(f, "lxml")

    # Extract the title of the thread
    thread_title = soup.find("title").get_text()
    # Get the <div> element containing the forum breadcrumns, i.e. the hierarchical menu showing the path of the forum
    # thread being extracted, in bullet point format
    navigate_section = soup.find("div", {"class": "navigate_section"})
    # Write to 'subforum_name' the next-to-last element from the bullet point list, which indicates the forum section containing
    # the thread being extracted; and replace the right double angle quotes (ASCII code character '187') from the name of the
    # subforum with nothing
    subforum_name = (
        navigate_section.find_all("li")[-2].get_text().replace(chr(187), "").strip()
    )
    # Assign to 'subforum_label' the custom label for the forum section, derived from 'subforum_name' using the
    # 'assign_subforum_label' function
    subforum_label = assign_subforum_label(subforum_name)

    # Get the <div> element containing all the posts
    posts_section = soup.find("div", {"id": "forumposts"})
    # For each single post do:
    for single_post in posts_section.find_all("div", {"class": "post_wrapper"}):
        # Create a <text> element tag to enclose the post
        text_tag = etree.SubElement(doc, "text")
        # Assign the title of thread to the <text> attribute 'title'
        text_tag.attrib["title"] = thread_title
        # Assign the name of the subforum to the <text> attribute 'subforum'
        text_tag.attrib["subforum"] = subforum_name
        # Assign the subforum label to the <text> attribute 'subforum_label'
        text_tag.attrib["subforum_label"] = subforum_label
        # Extract the username of the author of the post
        username = single_post.find("div", {"class": "poster"}).h4.get_text().strip()
        # Assign it as value of the attribute 'author' in the text metadata fields
        text_tag.attrib["author"] = username

        # Get the <div> element containing the details of the post
        post_details = single_post.find("div", {"class": "keyinfo"})
        # Extract the progressive number of the post, where number 1 is the first reply to the post, etc...
        get_post_number = re.search(
            ".*#([0-9]{1,5}).*",
            post_details.find("div", {"class": "smalltext"}).get_text(),
        )
        # Assign the number of the post from 'get_post_number' to the variable 'post_number', or set it to 0 if the post
        # is the first of the thread - since no number is included in the details of the first post
        post_number = get_post_number.group(1) if get_post_number is not None else 0
        # Assign it as value of the attribute 'post_number' in the <text> metadata fields
        text_tag.attrib["post_number"] = str(post_number)

        # Get the string of text containing the date on which the message was posted
        get_post_date = re.search(
            ".*on:(.*)", post_details.find("div", {"class": "smalltext"}).get_text()
        ).group(1)
        # Convert the string date into a datetime object, after removing the right double angle quotes
        post_date = parser.parse(get_post_date.replace(chr(187), ""))
        # Extract the time of posting (hours and minutes) using the custom format HHMM - built through the 'strftime' method - and
        # save it to the variable 'post_date_time'
        post_date_time = post_date.strftime("%H%M")
        # Extract the day, month, year from the datetime object (using the standard notation '.day', '.month', '.year' to
        # obtain 2 and 4-digit formats) and save each one to a different variable, then assign all the date elements to
        # different metadata attributes
        text_tag.attrib["date_d"] = str(post_date.day)
        text_tag.attrib["date_m"] = str(post_date.month)
        text_tag.attrib["date_y"] = str(post_date.year)
        text_tag.attrib["date_time"] = str(post_date_time)

        # Get the <div> containing the content of the post, i.e. the message
        post_section = single_post.find("div", {"class": "post"})
        # Check if the message contains "a quote", i.e. if the message the current one replies to is included inside the post; if
        # so, exclude it from the extraction, extract the message and assign it to the variable 'post_content'
        try:
            post_section.find("div", {"class": "quoteheader"}).extract()
            post_section.find("blockquote").extract()
            post_content = post_section.get_text()
        # If no quotation is present, extract the message and store it inside the variable 'post_content'
        except AttributeError:
            post_content = post_section.get_text()
        # Write the extracted message as text of the 'text' element tag
        text_tag.text = post_content

    # Build the XML structure with all the elements collected so far
    tree = etree.ElementTree(doc)
    # Write the resulting XML structure to a file named after the input filename, using utf-8 encoding, adding the XML declaration
    # at the start of the file and graphically formatting the layout ('pretty_print')
    tree.write(
        filename + ".xml", pretty_print=True, xml_declaration=True, encoding="utf-8"
    )