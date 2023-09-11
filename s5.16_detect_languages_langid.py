'''
    Script s5.16 | v1.0.0 | consult <https://catlism.github.io> for more info.
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

# Import the modules to read file according to regular expressions, to read/write csv files,
# to use regular expressions, and to detect the languages
import glob
import csv
import re
import langid

# Create the output csv file (and relative writer) that will contain the results of the detections, using the 'append'
# ("a") mode to continuously write new lines to the end of the file
csvfile = open("language_count.csv", "a", encoding="utf-8")
csvfile_writer = csv.writer(csvfile)
# Write the header of the csv file
csvfile_writer.writerow(
    [
        "doc_id",
        "en",
        "% en",
        "it",
        "% it",
        "es",
        "% es",
        "fr",
        "% fr",
        "de",
        "% de",
        "n_lines",
    ]
)

# Search for .txt files in all the subfolders of the current folder - where the script resides
files = glob.glob("./**/*.txt", recursive=True)

# For each file do:
for file in files:
    # Extract the filename and its path, without the file extension
    filename = re.sub(".txt", "", file)
    # Create an empty list that will contain all the lines of the input file
    all_lines = []
    # Open the input file
    text_content = open(file, "r", encoding="utf-8").readlines()
    # Read each line of the input file, and for each one do:
    for i in text_content:
        # Detect the language of the line
        langcode = langid.classify(i)[0]
        # Add the language ISO 639-1 code to the created list
        all_lines.append(langcode)
    # Count the total number of lines in the input file, and store it into a variable
    lines_count = len(all_lines)
    # Count the number of lines detected as English and other languages, and store each one in a separate variable
    en_count = all_lines.count("en")
    it_count = all_lines.count("it")
    es_count = all_lines.count("es")
    fr_count = all_lines.count("fr")
    de_count = all_lines.count("de")
    # Count the percentage of each language in the document, using the above results, and store results in separate variables
    en_perc = round((en_count / lines_count) * 100)
    it_perc = round((it_count / lines_count) * 100)
    es_perc = round((es_count / lines_count) * 100)
    fr_perc = round((fr_count / lines_count) * 100)
    de_perc = round((de_count / lines_count) * 100)
    # Create the csv line to be written, using the variables storing the different collected values
    csv_line = [
        filename,
        en_count,
        en_perc,
        it_count,
        it_perc,
        es_count,
        es_perc,
        fr_count,
        fr_perc,
        de_count,
        de_perc,
        lines_count,
    ]
    # Write the above line to the csv file
    csvfile_writer.writerow(csv_line)