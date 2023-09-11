'''
    Script s5.05 | v1.0.0 | consult <https://catlism.github.io> for more info.
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

# Import modules for: loading files using regular expression; using 'textract' functionalities
from glob import glob
import textract

# List all filenames with the .pdf extension
files = glob("*.pdf")

# For each filename in the list, do:
for file in files:
    # Remove the '.pdf' extension and save the resulting filename to the variable 'filename'
    filename = file.replace(".pdf", "")
    # Open and process the file through 'textract', using UTF-8 as output encoding
    doc = textract.process(file, output_encoding="utf-8")
    # Create and open the output file, and write the extracted contents as raw bytes ("wb")
    with open(filename + ".txt", "wb") as file_output:
        file_output.write(doc)