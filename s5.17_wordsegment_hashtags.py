# Import the module to use regular expressions, and the one for segmenting strings of multiple words joined together
# into single words
import re
import wordsegment

# Load the list of English words supported by the module
wordsegment.load()
# Compile the regular expression to identify hashtags (including the two possible symbols) and the text string that follows
hashtag_re = re.compile("(?:^|\s)([＃#]{1})(\w+)", re.UNICODE)

# Open and read the data file, and store its contents in the variable 'file_contents'
file_contents = open("twint_output.xml", "r", encoding="utf-8").read()
# Search for every hashtag appearing in the contents, and for each one do
for hashtag in re.findall(hashtag_re, file_contents):c
    # Merge the hashtag symbol and the following string into one single string and store it in the variable 'found_hashtag'
    found_hashtag = "".join(hashtag)
    # Save the string (without the hashtag symbol) into the variable 'clean_hashtag'
    clean_hashtag = hashtag[1]
    # Apply the word segmentation on the hashtag string, and save the resulting string to the 'segmented' variable
    segmented = " ".join(wordsegment.segment(clean_hashtag))
    # Construct the final tag element 'exhashtag' using the non-segmented version of the string as value to the argument 'original',
    # and include the segmented version as enclosed by the tag
    tag = f"<exhashtag original='{clean_hashtag}'>{segmented}</exhashtag>"
    # Replace every instance of the original hashtag (composed by the hashtag symbol followed by the text string) with the final tag element
    file_contents = file_contents.replace(found_hashtag, tag)

# Open the output file
with open("cleaned_hashtags.xml", "w", encoding="utf-8") as out_file:
    # Write the modified contents to the output file
    out_file.write(file_contents)