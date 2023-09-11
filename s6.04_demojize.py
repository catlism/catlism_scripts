'''
    Script s6.04 | v1.0.0 | consult <https://catlism.github.io> for more info.
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

# Import the required module to transliterate emojis
import emoji

# Define the function called 'demojize')
def demojize(text, output):
    """Converts emoji(s) found in a string of text into their transliterated CLDR version; input is:

    text: the string of text with one or more emojis
    output: the format of the 'output.

    If 'output' is set to 'default', the result for 🙃 is {upside-down_face}
    If 'output' is set to custom, result is {upside^down^face}

    Usage follows the syntax
    demojize(INPUT, FORMAT)
    """

    # If 'output' is set to 'default', apply the standard transliteration using square brackets as delimiters
    if output == "default":
        return emoji.demojize(text, delimiters=("{", "}"))
    # Else if set to 'custom' do:
    elif output == "custom":
        # Create a list and store inside of it the text to be processed
        out_text = list(text)
        # Use the function 'emoji_count' to count the total number of identified emojis
        emoji_count = emoji.emoji_count(out_text)
        # For each identified emoji do:
        for i in range(emoji_count):
            # Take the first (and only) emoji in the list of emojis found, created through the function 'emoji_list'.
            # The function create, for each emoji, three data-points: 'emoji' containing the actual emoji;
            # 'match_start' indicates the positional value of the first character of the emoji; 'match_end the positional
            # value of the last character of the emoji.
            first_emoji = emoji.emoji_list(out_text)[0]
            # Store the three aforementioned data-points in three separate variables
            found_emoji = first_emoji["emoji"]
            emoji_start = first_emoji["match_start"]
            emoji_end = first_emoji["match_end"]
            # Apply the standard demojize function to the identified emoji, and replace the underscore _ with the character ^
            demojized = str(
                " " + emoji.demojize(found_emoji, delimiters=("{", "}")) + " "
            ).replace("_", "^")
            # Replace the hyphen with the character ^
            demojized = demojized.replace("-", "^")
            # Replace the emoji with its transliterated version in the original text
            out_text[emoji_start:emoji_end] = demojized
        # Return the full text with transliterated emojis
        return "".join(out_text)