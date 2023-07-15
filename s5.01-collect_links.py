# Import modules for: regular expressions; loading files using regular expression; reading/writing CSV files;
# using BeautifulSoup
import re
from glob import glob
import csv
from bs4 import BeautifulSoup

# List all filenames with the .html extension and store the list in the variable 'files'
files = glob("*.html")
# Create the header (i.e. the first row containing the column names) for the output CSV file
csv_header = ["link", "downloaded"]

# For each found HTML file do:
for file in files:
    # Open the file
    f = open(file, encoding="utf-8")
    # From the original filename, strip the '.html' extension
    filename = file.replace(".html", "")
    # Read the contents of the file through BeautifulSoup and store them inside the variable 'soup'
    soup = BeautifulSoup(f, "lxml")
    # Create the CSV output file (named after the original HTML one) to write the output contents
    with open(filename + "_links.csv", "a") as file_output:
        # Start writing the output file
        writer = csv.writer(file_output)
        # Write the header
        writer.writerow(csv_header)
        # Create an empty list to store the collected URLs
        url = []
        # Find all URLs matching the regular expression, and for each one do:
        for link in soup.find_all("a", {"href": re.compile(r".*?theses/available.*?")}):
            # Write the found URL and write it to the output file
            writer.writerow([link["href"], "n"])