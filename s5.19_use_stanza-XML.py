# Import modules to open files using regexes; use regexes; use Stanza;  read and write XML files
import glob
import re
import stanza
from lxml import etree

# Initiate the Stanza module; define the language of the texts,
# and the types of information Stanza needs to add to each word
nlp = stanza.Pipeline("en", processors="tokenize,mwt,pos,lemma")
# Find all the .txt files in the current folder
files = glob.glob("*.txt")
# For each file, do:
for file in files:
    # Read the name of the file, delete the extension '.txt', and store
    # it inside of a variable
    filename = re.sub(".txt", "", file)
    # Open, read, and process the contents of the file with Stanza
    doc = nlp(open(file, encoding="utf-8").read())
    # Create the root <text> element tag - with no extra attributes - that will wrap the content of the file
    text = etree.Element("text")
    # Initiate a counter that increases by 1 for every sentence, then
    # for every sentence do:
    for i, sentence in enumerate(doc.sentences, start=1):
        # Create an <s> tag element to enclose the sentence, and assign
        # the attribute 'n' containing as value the number of the sentence
        s = etree.SubElement(text, "s", n=str(i))
        # For every word in the sentence do:
        for word in sentence.words:
            # If the word is a punctuation mark:
            if word.pos == "PUNCT":
                # Enclose it inside of a <c> tag element, and add its POS and lemma as attributes
                etree.SubElement(
                    s, "c", pos=str(word.pos), lemma=str(word.lemma).lower()
                ).text = str(word.text)
            # If the word is not a punctuation mark:
            else:
                # Enclose it inside of a <w> tag element, and add its POS and lemma as attributes
                etree.SubElement(
                    s, "w", pos=str(word.pos), lemma=str(word.lemma).lower()
                ).text = str(word.text)
    # Add the sentences and the words inside of the 'text' element
    tree = etree.ElementTree(text)
    # Write the resulting XML structure to a file named after the input filename, using utf-8 encoding, adding the XML declaration
    # at the start of the file and graphically formatting the layout ('pretty_print')
    tree.write(
        filename + ".xml", pretty_print=True, xml_declaration=True, encoding="utf-8"
    )