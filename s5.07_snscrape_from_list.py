'''
    Script to collect data from Instagram | v1.0.0
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

# Adapted from the following sources
# https://github.com/MartinBeckUT/TwitterScraper/blob/127b15b3878ab0c1b74438011056d89152701db1/snscrape/python-wrapper/snscrape-python-wrapper.py
# https://github.com/satomlins/snscrape-by-location/blob/1f605fb6e1caff3577198792a7717ffbf3c3f454/snscrape_by_location_tutorial.ipynb
# Import the modules for: using snscrape; working with dataframes; employing command-line arguments; using regular expressions

import snscrape.modules.twitter as sntwitter
import pandas as pd
import argparse
import re

# Add the ability to specify arguments for the script
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# Construct the first argument as the name of the file containing the search terms
parser.add_argument("searchlist")
# Construct the optional second argument (following the label --max) as the maximum number of tweets to be collected
# for each search term
parser.add_argument(
    "--max",
    dest="maxResults",
    type=lambda x: int(x)
    if int(x) >= 0
    else parser.error("--max-results N must be zero or positive"),
    metavar="N",
    help="Only return the first N results",
)
# Read the provided arguments
args = parser.parse_args()
# Read the first argument as the name of the file containing the search terms
search_list = args.searchlist
# Read the second (optional) argument as the maximum number of tweets to be collected for each search term
maxResults = args.maxResults

# Open the search terms list
with open(search_list, "r", encoding="utf-8") as f:
    # For every search terms do
    for word in f:
        # Eliminate the 'newline' character (\n)
        word = word.rstrip("\n")
        # Clean the search term from characters that are invalid in filenames using a regular expression; this is used for the output file only.
        # From https://stackoverflow.com/a/71199182
        clean_word = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", word)
        # Create an empty list that will contain the collected tweets
        tweets_list = []
        # Collect tweets for the search terms, taking into account the maximum number of tweets (if supplied)
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(word).get_items()):
            # Stop the collection of tweets once the maximum number supplied is reach
            if i >= maxResults:
                break
            # Add all the data-points collected for the tweet to the previously created list
            tweets_list.append(
                [
                    tweet.date,
                    tweet.id,
                    tweet.content,
                    tweet.url,
                    tweet.user.username,
                    tweet.user.followersCount,
                    tweet.replyCount,
                    tweet.retweetCount,
                    tweet.likeCount,
                    tweet.quoteCount,
                    tweet.lang,
                    tweet.outlinks,
                    tweet.media,
                    tweet.retweetedTweet,
                    tweet.quotedTweet,
                    tweet.inReplyToTweetId,
                    tweet.inReplyToUser,
                    tweet.mentionedUsers,
                    tweet.coordinates,
                    tweet.place,
                    tweet.hashtags,
                    tweet.cashtags,
                ]
            )
            # Create a dataframe from the tweets list above, naming the columns with the provided human-readable labels
            tweets_df = pd.DataFrame(
                tweets_list,
                columns=[
                    "Datetime",
                    "Tweet Id",
                    "Text",
                    "URL",
                    "Username",
                    "N. followers",
                    "N. replies",
                    "N. retweets",
                    "N. likes",
                    "N. quote",
                    "Language",
                    "Outlink",
                    "Media",
                    "Retweeted tweet",
                    "Quoted tweet",
                    "In reply to tweet ID",
                    "In reply to user",
                    "Mentioned users",
                    "Geo coordinates",
                    "Place",
                    "Hashtags",
                    "Cashtags",
                ],
            )
            # Export the dataframe to a tab-delimited CSV whose filename is equivalent to the search term cleaned from characters that cannot be included in filenames
            tweets_df.to_csv(clean_word + ".csv", sep="\t", index=False, encoding="utf-8")