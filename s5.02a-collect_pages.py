'''
    Script s5.02a | v1.0.0 | consult <https://catlism.github.io> for more info.
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

# Import modules for: reading/writing CSV files; using regular expressions; working with SSL certificates;
# loading files using regular expression; pausing the script; using BeautifulSoup
import csv
import re
import ssl
from glob import glob
from time import sleep
from bs4 import BeautifulSoup

# the variable and the import below allow the crawler to browse https pages when invalid certificates are used in the
# website to be scraped. Adapted from:
# https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
ssl._create_default_https_context = ssl._create_unverified_context
from selenium import webdriver

# Define the options to pass to Firefox webdriver (i.e. the Selenium mechanisms that will control Firefox through the
# instructions imparted by this script)
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
# Create the Firefox webdriver
driver = webdriver.Firefox(options=options)

# Find all the filenames containing the string 'links.csv' preceded by any character(s)
files = glob("*links.csv")

# Set the headers Firefox will use to access the web pages
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
}

# For each file found, do:
for file in files:
    # Open and read the file as CSV
    reader_csv = csv.reader(open(file, "r"))
    # Skip the first line of the CSV containing the header
    next(reader_csv, None)
    # Create a list containing all the rows of the CSV
    rows = [r for r in reader_csv]
    # For each row (i.e. each link) in the list do:
    for row in rows:
        # Search for the string corresponding to the URN in the link
        urn_search = re.search(r".*?available/(.*?)/", row[0])
        # Extract the URN and store it in the variable 'urn'
        urn = urn_search.group(1)
        # Use the webdriver to read the page indicated by the link
        driver.get(row[0])
        # Read the source code of the page using BeautifulSoup, and store it in the variable 'soup'
        soup = BeautifulSoup(driver.page_source, "lxml")
        # Open the output file inside the subfolder 'downloaded', using the URN as its filename, followed by '.html'
        with open("downloaded/" + urn + ".html", "a") as file_output:
            # Write the source code of the page into the output file
            file_output.write(str(soup))
        # Wait 4 secons before restarting the loop
        sleep(4)