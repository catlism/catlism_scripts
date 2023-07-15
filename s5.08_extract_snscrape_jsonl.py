# Import the required modules to read/write jsonl and xml files
import jsonlines
from lxml import etree

# Create the root element of the XML structure - named 'corpus' -, which will contain all the extracted tweets
# as elements defined by the 'text' tag (one tweet = one text)
corpus = etree.Element("corpus")

# Open the jsonl file
tweets = jsonlines.open("snscrape_output.jsonl")
# Read it line by line - i.e. one tweet at a time -, and for each line do:
for obj in tweets:
    # Read the selected data points and store each one in a separate variable
    tweet_id = obj["id"]
    tweet_date = obj["date"]
    tweet_username = obj["user"]["username"]
    tweet_user_realname = obj["user"]["displayname"]
    tweet_content = obj["content"]
    # The following variables should contain the value 0 if no urls are included or the tweet is not a retweet,
    # and the value 1 when links are present or the tweet is a retweet
    tweet_urls_present = 0 if obj["outlinks"] is None else 1
    tweet_isretweet = 0 if obj["retweetedTweet"] is None else 1
    # The extracted values are assigned as values to the arguments of a tag labelled 'text' - contained inside of the main
    # <corpus> element tag - separating one tweet from another. The actual content of the tweet is
    # then enclosed inside of the <text> element tag using the notation '.text'
    etree.SubElement(
        corpus,
        "text",
        id=str(tweet_id),
        date=str(tweet_date),
        username=str(tweet_username),
        user_realname=str(tweet_user_realname),
        urls_present=str(tweet_urls_present),
        isretweet=str(tweet_isretweet),
    ).text = str(tweet_content)
# The XML structure is created by adding all the extracted elements to the main 'corpus' tag
tree = etree.ElementTree(corpus)
# The resulting XML structure is written to the output.xml file using utf-8 encoding, adding the XML declaration
# at the beginning and graphically formatting the layout ('pretty_print')
tree.write("output.xml", pretty_print=True, xml_declaration=True, encoding="utf-8")