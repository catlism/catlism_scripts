'''
    Script s5.09 | v1.0.0 | consult <https://catlism.github.io> for more info.
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

# Import modules for: loading files using regular expression; reading JSON files; working with .xz compressed files;
# working on local folders and files; using regular expressions; working with XML files
import glob
import json
import lzma
import os
import re
from lxml import etree

# Create and compile a regular expression to capture the timestamp included in the filenames downloaded by instaloader
dates_filter = re.compile(
    "([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}_UTC).*", re.UNICODE
)

# Create an empty list to store all the timestamps retrieved from filenames
dates = []
# List all the files in the current folder (the one where the script resides)
files = glob.glob("*.*")

# For every single file found:
for single_file in files:
    # Use the 'dates_filter' regex to find the date in the filename, and store it in the variable 'found_date'
    found_date = re.search(dates_filter, single_file)
    # If the date is found and is not already included in the list 'dates', add it; otherwise, proceed to the next step
    if found_date is not None and found_date[1] not in dates:
        dates.append(found_date[1])

# For every date in the list of dates, do
for date in dates:
    # Create the root element tag <text> to include all the contents relative to the date (i.e. the post and its relative comments)
    text_tag = etree.Element("text")

    # Build the filename of the compressed JSON containing the post contents and metadata, and store it in a variable
    archive_filename = date + ".json.xz"
    # Check if the file exist on disk; if not, skip this date and start from the beginning
    if not os.path.isfile(archive_filename):
        print("File " + archive_filename + "not found, skipping...")
        continue

    # Create the <item> element tag to store the contents of the post
    item_tag = etree.SubElement(text_tag, "item")
    # Open the compressed JSON file and do:
    with lzma.open(archive_filename) as f:
        # Read its contents and store them into a variable
        contents = f.read()
        # Decode the contents to UTF-8
        contents = contents.decode("utf-8")
    # Load the decoded contents as a JSON file
    data = json.loads(contents)

    # Assign the main JSON data-point to the variable 'node', to avoid repeating a longer string throughout the code
    node = data["node"]
    # Extract a number of values from JSON data-points, and assign each one of them to a separate attribute of <item>
    item_tag.attrib["id"] = str(node["shortcode"])
    item_tag.attrib["type"] = "post"
    item_tag.attrib["created"] = str(node["taken_at_timestamp"])
    item_tag.attrib["username"] = str(node["owner"]["username"])
    item_tag.attrib["comments"] = str(node["edge_media_to_comment"]["count"])
    # The following data-points are checked: if they do not exist, a value of 'none' and 'na' is assigned
    # to the two attributes respectively
    item_tag.attrib["location"] = str(
        node["location"]["slug"] if node["location"] is not None else "none"
    )
    item_tag.attrib["likes"] = str(
        data["node"]["edge_media_preview_like"]["count"]
        if "edge_media_preview_like" in data["node"]
        else "na"
    )
    # Try to extract the textual content of the post: if the key exists, extract it; if not, assign an empty string to the variable
    # that stores the caption
    try:
        text_post_caption = str(
            node["edge_media_to_caption"]["edges"][0]["node"]["text"]
        )
    except IndexError:
        text_post_caption = ""
    # Enclose the textual content of the post inside <item>
    item_tag.text = text_post_caption

    # Check if data-point 'edge_sidecar_to_children' exists (i.e. if the post contains multiple multimedia files)
    if "edge_sidecar_to_children" in node:
        # For each object (i.e. multimedia file) found, start a counter to assign a progressive number (starting from 1)
        # to each one of them, and then do:
        for media_num, media in enumerate(
            node["edge_sidecar_to_children"]["edges"], start=1
        ):
            # Extract a number of values from JSON data-points, and assign each one of them to a separate variable
            media_shortcode = str(media["node"].get("shortcode", "na"))
            # Check if the data-point 'is_video' exists, and if so assign the value 'video' to 'media_type';
            # otherwise assign it the value 'image'
            media_type = "video" if media["node"]["is_video"] else "image"
            # Check if the data-points 'is_video' exists: if so, assign the name of the media using the string '.mp4',
            # if not assign the string '.jpg'
            media_name = (
                str(date + "_" + str(media_num) + ".mp4")
                if media["node"]["is_video"]
                else str(date + "_" + str(media_num) + ".jpg")
            )
            # Check if the following data-points exists: if they do, extract their value and assign them to two separate variables;
            # if not, assign the value 'na' to the variable
            media_accessibility_caption = (
                str(media["node"]["accessibility_caption"])
                if "accessibility_caption" in media["node"]
                else "na"
            )
            media_views = (
                str(media["node"]["video_view_count"])
                if media["node"]["is_video"]
                else "na"
            )
            # Create a <media> element tag inside of <item>, and assign it all the previously extracted elements as
            # values to its attributes
            etree.SubElement(
                item_tag,
                "media",
                mediafile=media_name,
                mediatype=media_type,
                mediadescr=media_accessibility_caption,
                media_shortcode=media_shortcode,
                media_views=media_views,
            )
    # Otherwise, if data-point 'edge_sidecar_to_children' does not exist (i.e. if the post contains one single multimedia file)
    else:
        # Extract a number of values from JSON data-points, and assign each one of them to a separate variable - using
        # the same criteria adopted for the ones extracted from 'edge_sidecar_to_children'
        media_shortcode = str(node["shortcode"])
        media_type = "video" if node["is_video"] else "image"
        media_name = str(date + ".mp4") if node["is_video"] else str(date + ".jpg")
        media_accessibility_caption = (
            str(node["accessibility_caption"])
            if "accessibility_caption" in node
            else "na"
        )
        media_views = str(node["video_view_count"]) if node["is_video"] else "na"

        etree.SubElement(
            item_tag,
            "media",
            mediafile=media_name,
            mediatype=media_type,
            mediadescr=media_accessibility_caption,
            media_shortcode=media_shortcode,
            media_views=media_views,
        )

    # Build the filename for the comments file
    comments_filename = str(date + "_comments.json")
    # Check if the comments file exists, and if so do:
    if os.path.isfile(comments_filename):
        # Open the comments file and do:
        with open(comments_filename, encoding="utf-8") as f:
            # Read its contents as JSON and store them into a variable
            comments = json.loads(f.read())
        # For each comment in the contents do:
        for comment in comments:
            # Create an <item> element tag
            item_tag = etree.SubElement(text_tag, "item")
            # Extract a number of values from JSON data-points, and assign each one of them to a separate attribute of <item>
            item_tag.attrib["id"] = str(comment["id"])
            item_tag.attrib["type"] = "comment"
            item_tag.attrib["created"] = str(comment["created_at"])
            item_tag.attrib["username"] = comment["owner"]["username"]
            # The location is not present in the data-points for a comment; however, to have a structure that is consisten with
            # the <item> element tag when used for a post (for which a location may be present) the attribute is added with value 'na'
            item_tag.attrib["location"] = "na"
            item_tag.attrib["likes"] = str(comment["likes_count"])
            item_tag.attrib["comments"] = str(
                len(comment["answers"]) if comment["answers"] is not None else "na"
            )
            item_tag.text = comment["text"]

    # Write the extracted data formatted in XML to the final XML structure
    tree = etree.ElementTree(text_tag)
    # Write the resulting XML structure to the output file, using utf-8 encoding, adding the XML declaration
    # at the start of the file and graphically formatting the layout ('pretty_print')
    tree.write(date + ".xml", pretty_print=True, xml_declaration=True, encoding="utf-8")