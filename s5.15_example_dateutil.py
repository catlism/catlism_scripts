'''
    Script s5.15 | v1.0.0 | consult <https://catlism.github.io> for more info.
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

# Import the module to interpret strings as dates
import dateutil.parser as parser

# Assign a string to the variable 'text'
text = "Friday 15th April 2022 17:10:05 +0200"
# Process 'text' through the date parsers, and assign it to the variable 'date'
date = parser.parse(text)
# Print the date object using ISO 8601 format
print(date.isoformat())
# output: 2022-04-15T17:10:05+02:00