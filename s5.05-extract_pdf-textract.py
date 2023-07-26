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