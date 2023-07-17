# Import the module to interpret strings as dates
import dateutil.parser as parser

# Assign a string to the variable 'text'
text = "Friday 15th April 2022 17:10:05 +0200"
# Process 'text' through the date parsers, and assign it to the variable 'date'
date = parser.parse(text)
# Print the date object using ISO 8601 format
print(date.isoformat())
# output: 2022-04-15T17:10:05+02:00