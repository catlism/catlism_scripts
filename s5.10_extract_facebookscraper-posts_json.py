'''
    Script to collect data from Instagram | v1.0.0
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

# Import modules for: regular expressions; reading JSON files; loading files using regular expression;
# working with XML files; reading timestamps as date objects;
import re
import json
import glob
from lxml import etree
from dateutil import parser

# Get a list of all the files with .json extension
files = glob.glob("*.json")
# For each file, do:
for single_file in files:
    # Delete the extension from the filename and store it inside of the 'filename' variable
    filename = single_file.replace(".json", "")

    # Open the file and do:
    with open(single_file, encoding="utf-8") as f:
        # Read its contents and save them to the 'contents' variable
        contents = f.read()
        # Use a regular expression to remove extra commas between JSON objects; this fixes a bug in the current version of
        # facebook-scraper (v0.2.59) whereby more than one comma may be inserted between JSON objects, rendering the contents
        # unparsable by Python
        contents = re.sub("\},{2,}\{", "},{", contents)

    # Load the read contents as JSON
    data = json.loads(contents)
    # Create the <text> root element tag where the post contents and details are stored in the final XML
    text_tag = etree.Element("text")

    # For each object in the JSON, corresponding to one post, do:
    for post in data:
        # Create the <post> element tag to enclose one single post
        post_tag = etree.SubElement(text_tag, "post")
        # Assign a set of attributes to <post> using the data extracted from the metadata data-points, as well as the
        # textual content of the post as text of the <post> element tag
        post_tag.attrib["id"] = post["post_id"]
        post_tag.attrib["author"] = post["username"]
        post_tag.attrib["author_id"] = str(post["user_id"])
        post_tag.attrib["comments"] = str(post["comments"])
        post_tag.attrib["shares"] = str(post["shares"])
        post_tag.text = post["text"]

        # Extract the date and transform it into a datetime object, then extract the two-digit day and month along the 4-digit
        # year and assign them to the three attributes 'date_d', 'date_m', and 'date_y' respectively
        post_date = parser.parse(post["time"])
        post_tag.attrib["date_d"] = str(post_date.day)
        post_tag.attrib["date_m"] = str(post_date.month)
        post_tag.attrib["date_y"] = str(post_date.year)

        # Check if the number of 'likes' and 'reactions' is present: if so, assign the values to the two attributes, if not
        # assign the value 0
        post_tag.attrib["likes"] = str(
            post["likes"] if post["likes"] is not None else 0
        )
        post_tag.attrib["reactions_count"] = str(
            post["reaction_count"] if post["reaction_count"] is not None else 0
        )

        # Check if details concerning reactions are present, i.e. if the dictionary for reactions exists and the key 'sad' exists
        reactions = post.get("reactions")
        if isinstance(reactions, dict) and reactions.get("sad"):
            # If present, assign the total number of 'sad' reactions to the 'reactions_sad' attribute
            post_tag.attrib["reaction_sad"] = str(reactions.get("sad"))
        else:
            # If not, assign the value 0
            post_tag.attrib["reaction_sad"] = "0"

        # Check if the array of comments is not empty, i.e. if check if the metadata data-point for comments is present
        # (if the data was collected withouth the '--comments' the array is always empty; if '--comments' was used,
        # array may be empty if no comments were made to the post. If the array is empty, proceed with the next item
        if post["comments_full"] is None:
            continue

        # For each found comment, do:
        for comment in post["comments_full"]:
            # Create the <comment> element tag to enclose the contents of the comment
            comment_tag = etree.SubElement(post_tag, "comment")
            # Assign a set of attributes to <comment>, including 'type' with value 'c' indicating this is a comment
            # and not a reply to a comment (identified by the value 'r'), as well as the textual content of the
            # post as text of the <post> element tag
            comment_tag.attrib["type"] = "c"
            comment_tag.attrib["comment_to"] = post["post_id"]
            comment_tag.attrib["id"] = comment["comment_id"]
            comment_tag.attrib["author"] = comment["commenter_name"]
            comment_tag.attrib["author_id"] = comment["commenter_id"]

            # Extract the date and transform it into a datetime object - if present, otherwise
            # extract the two-digit day and month along the 4-digit year and assign them to
            # the three attributes 'date_d', 'date_m', and 'date_y' respectively
            comment_date = (
                parser.parse(comment["comment_time"])
                if comment["comment_time"] is not None
                else None
            )

            comment_tag.attrib["date_d"] = str(
                comment_date.day if comment_date is not None else "na"
            )
            comment_tag.attrib["date_m"] = str(
                comment_date.month if comment_date is not None else "na"
            )
            comment_tag.attrib["date_y"] = str(
                comment_date.year if comment_date is not None else "na"
            )
            comment_tag.text = comment["comment_text"]

            # Check if the array of replies exists; if it does not, proceed with the next item
            if not comment["replies"]:
                continue

            # For each reply found, do:
            for reply in comment["replies"]:
                # Create the <comment> element tag to enclose the contents of the reply
                reply_tag = etree.SubElement(post_tag, "comment")

                # Assign a set of attributes to <comment>, including 'type' with value 'r' indicating
                # this is a reply to a comment and not a direct comment to the post (identified by the value 'c'),
                # as well as the textual content of the  post as text of the <post> element tag
                reply_tag.attrib["type"] = "r"
                reply_tag.attrib["comment_to"] = comment["comment_id"]
                reply_tag.attrib["id"] = reply["comment_id"]
                reply_tag.attrib["author"] = reply["commenter_name"]
                reply_tag.attrib["author_id"] = reply["commenter_id"]
                reply_date = (
                    parser.parse(reply["comment_time"])
                    if reply["comment_time"] is not None
                    else None
                )
                reply_tag.attrib["date_d"] = str(
                    reply_date.day if reply_date is not None else "na"
                )
                reply_tag.attrib["date_m"] = str(
                    reply_date.month if reply_date is not None else "na"
                )
                reply_tag.attrib["date_y"] = str(
                    reply_date.year if reply_date is not None else "na"
                )
                reply_tag.text = reply["comment_text"]

    # Build the XML structure with all the elements collected so far
    tree = etree.ElementTree(text_tag)
    # Write the resulting XML structure to a file named after the input filename, using utf-8 encoding, adding the XML declaration
    # at the start of the file and graphically formatting the layout ('pretty_print')
    tree.write(
        filename + ".xml", pretty_print=True, xml_declaration=True, encoding="utf-8"
    )