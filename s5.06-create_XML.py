# Import modules for: loading files using regular expression; using regular expressions; using dataframes;
# reading/writing XML files
import glob
import re
import pandas as pd
from lxml import etree

# Create a function to remove illegal XML characters. These are control characters identified by code points included in the
# ranges defined in the 'return' output. In XML 1.0 the only control characters allowed are tab, line feed, and carriage return (often 
# interpreted as whitespaces or line-breaks), represented by Unicode code points U+0009, U+000A, U+000D (written in hexadecimal 
# format in the function, e.g. 0x9 for U+0009). Function adapted from:
# https://github.com/faizan170/resume-job-match-nlp/blob/573484a9b180950ddd373615e2f09ae163d7b0ae/main.py
def remove_control_characters(c):
    # Read the Unicode code point of the character, and store it into the 'codepoint' variable
    codepoint = ord(c)
    # Return the character if it is an XML allowed one
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
        )

# Create an empty list to store the found filenames 
list_of_filenames = []
# Compile a regular expression to capture the URN code from the filenames that have the string '_0' - indicating that they are the 
# first file  for each single URN
urnRegex = re.compile(
    "etd-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]_0*.txt"
)
# List all filenames including the URN regular expression plus the '_0' indicating that they are the first file
# for each single URN
files = sorted(
    glob.glob(
        "etd-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]_0*.txt"
    )
)
# Add the found filenames to the list 'list_of_filenames'
list_of_filenames.append(files)


# Create a metadata database (mdb) using the metadata csv file; set the urn as index, and remove duplicates.
# This is needed since the same thesis can appear more than once if it is catalogued under different categories on MoreThesis.
mdb = pd.read_csv("metadata_all.csv", sep="\t", encoding="utf-8")
mdb = mdb.set_index("urn")
mdb = mdb.groupby(mdb.index).first()

# For each filename in the found ones:
for file in files:
    # Extract the URN from the filename
    urn = re.search("(etd-[0-9]{8}-[0-9]{6})_[0-9]{1,2}.*", file).group(1)
    # Create the output filename by appending '.xml' to the URN
    output_file = urn + ".xml"
    # Create the root tag element <doc> to include all the generated XML contents
    doc = etree.Element("doc")
    # Assign a number of attributes to <doc>, extracting their values from 'mdb' using the URN as key to find them - except
    # for the URN itself
    doc.attrib["urn"] = urn
    doc.attrib["type"] = mdb.loc[urn, "tipo_tesi"]
    # Remove the comma between the author's surname and name
    doc.attrib["author"] = re.sub(",", "", mdb.loc[urn, "autore"])
    doc.attrib["title"] = mdb.loc[urn, "titolo_it"]
    # As not all the theses may have an English title, check if it is so, and assign value 'na' when not available
    doc.attrib["title_en"] = mdb.loc[urn, "titolo_en"] if not type(None) else "na"
    doc.attrib["department"] = mdb.loc[urn, "struttura"]
    doc.attrib["degree"] = mdb.loc[urn, "corso_di_studi"]
    # Extract the date (in the format YYYY-MM-DD) and capture each part into a group
    date = re.search("([0-9]{4})-([0-9]{2})-([0-9]{2})", mdb.loc[urn, "data"])
    doc.attrib["date_y"] = date.group(1)
    doc.attrib["date_m"] = date.group(2)
    doc.attrib["date_d"] = date.group(3)

    # Create an empty list to contain the cleaned contents of the thesis    
    all_thesis_texts = []

    # For each .txt file containing the processed URN, do:
    for f in sorted(glob.glob(urn + "*.txt")):
        # Open the file and read its contents)
        one_file = open(f, "r", encoding="utf8").read()
        # Using the function 'remove_control_characters', clean the contents from characters that are illegal in XML, and store the
        # resulting cleaned text in the variable 'cleaned_text'
        cleaned_text = ''.join(c for c in one_file if remove_control_characters(c))
        # Add 'cleaned_text' to the list 'all_thesis_texts'
        all_thesis_texts.append(cleaned_text)
    
    # Assign all the texts in 'all_thesis_texts' as text of the <doc> element tag
    doc.text = " ".join(all_thesis_texts)
    # Build the XML structure with all the elements collected so far
    tree = etree.ElementTree(doc)
    # Write the resulting XML structure to the output file, using utf-8 encoding, adding the XML declaration
    # at the start of the file and graphically formatting the layout ('pretty_print')
    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="utf-8")