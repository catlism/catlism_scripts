'''
    Script s5.20 | v1.0.0 | consult <https://catlism.github.io> for more info.
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

# Import modules to open files using regexes; use regexes; use Stanza;  read and write XML files
import glob
import re
import stanza
from lxml import etree

# Initiate the Stanza module, and define the language of the texts,
# and the types of information Stanza needs to add to each word
nlp = stanza.Pipeline("en", processors="tokenize,mwt,pos,lemma")
# Select all .txt files in the current folder
files = glob.glob("*.txt")
# For each file, do:
for file in files:
    # Read the name of the file, delete the extension '.txt', and store
    # it inside a variable
    filename = re.sub(".txt", "", file)
    # Open, read, and process the file with Stanza
    doc = nlp(open(file, encoding="utf-8").read())
    # Create the root <text> element tag - with no extra attributes - that will wrap the content of the file
    text = etree.Element("text")
    # Initiate a counter that increases by 1 for every sentence, then
    # for every sentence do:
    for i, sentence in enumerate(doc.sentences, start=1):
        # Initialise and empty list that will contain the lines of tagged text for the currently processed sentence
        tagged = []
        # Create an <s> tag element to enclose the sentence, and assign
        # the attribute 'n' containing as value the number of the sentence
        s = etree.SubElement(text, "s", n=str(i))
        # For every word in the sentence do:
        for word in sentence.words:
            # Construct the line that contains the word as it appears in the text,
            # its lemma, and its POS function, each one separated from the other using
            # a tab
            line = word.text + "\t" + word.lemma + "\t" + word.pos
            # Add the line to the list of tagged lines
            tagged.append(line)
        # Collate all the tagged contents saved to the list 'tagged' and enclose them inside of the <s> element tag
        s.text = "\n".join(tagged)
    tree = etree.ElementTree(text)
    # Write the resulting XML structure to a '.vrt' file named after the input filename, using utf-8 encoding, adding the XML
    # declaration at the start of the file and graphically formatting the layout ('pretty_print')
    tree.write(
        filename + ".vrt", pretty_print=True, xml_declaration=True, encoding="utf-8"
    )