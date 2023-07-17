# Import modules for: regular expressions; downloading data from URLs; loading files using regular expression;
# let the script wait a number of seconds before proceeding; using BeautifulSoup
import re
import urllib.request
from glob import glob
from time import sleep
from bs4 import BeautifulSoup

# Create a list of all the filenames with '.html' extension contained in the subfolder 'downloaded' and all of its possible subfolders
files = glob("./downloaded/*.html")

# For each filename found do:
for file in files:
    # Open the file
    f = open(file, "r", encoding="utf-8")
    # Read the contents of the file with BeautifulSoup and store them inside of the variable 'soup'
    soup = BeautifulSoup(f, "lxml")
    # Check if at least one <a> element tag with the string 'pdf' in its link is present in the HTML code
    # (i.e. if the page contains at least one link to a PDF file); if so do:
    if soup.find_all("a", {"href": re.compile("pdf")}):
        # For each link found, initiate a counter to preserve the order in which the files appear in the 
        # catalogue card, starting from 0 (the file appearing at the top), and do:
        for counter, link in enumerate(soup.find_all("a", {"href": re.compile("pdf")})):
            # Construct the download link by appending the website path to the partial link found in the 'href' attribute
            file_link = "https://morethesis.unimore.it" + (link["href"])
            # Extract the URN from 'file_link', and assign it to the variable 'urn_code'
            urn_code = re.search("(etd.*?)/", file_link).group(1)
            # Extract the original filename from 'link'
            filename = link.get_text()
            # Download the PDF file(s) to the sub-folder 'pdfs' (it must be created manually if it does not already exist),
            # assigning each file a name according to the structure URN_PROGRESSIVE-NUMBER_ORIGINAL-FILENAME.pdf
            urllib.request.urlretrieve(
                file_link, "pdfs/" + urn_code + "_" + str(counter) + "_" + filename
            )
            # Wait 4 seconds before downloading any other file
            sleep(4)
    # If no <a> element tag with the string 'pdf' is found, move to the next catalogue card
    else:
        continue