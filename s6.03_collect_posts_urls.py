# Import modules for: using regular expressions;  pausing the script ('sleep'); to collect data from the web;
# and to use BeautifulSoup
import re
from time import sleep
import requests
from bs4 import BeautifulSoup

# Compile the regular expression to capture heading tags (<h1>, <h2>, etc...)
heading_tags = re.compile("^h[1-6]$")
# Define the headers to be used for crawling the data, so that the script will be "seen" by the server
# as originating from a Chrome browser running on macOS
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}
# Create an empty list to store the collected URLs
links = []
# Initialise a counter to generate the incremental page numbers
start_page = 1
# Set the number of Wordpress pages to be collected
max_page_number = 2

while True:
    # Check if number of the page to be collected is greater than the total number of pages to be collected; if so, write the results to the output file and stop the collection
    if start_page > max_page_number:
        with open("links_list.txt", "w", encoding="utf-8") as output_file:
            output_file.write("\n".join(links))
        break
    # Check if the counter 'start_page' is set to the first page; if so the URL to crawl is the main page
    elif start_page == 1:
        url = "https://example.com/page/"
    # If the counter is set to 2 or more, then the URL follows a different format
    else:
        # Construct the URL by including (through the use of format and the {} notation) the number of the counter
        url = "https://example.com/page/{}/".format(start_page)
    # Get the content of the URL, using the headers defined in line 11
    r = requests.get(url, headers=headers)
    # Read the collected HTML content in BeautifulSoup using the 'lxml' parser
    soup = BeautifulSoup(r.content, "lxml")
    # Find the section that contains the list of articles; oftentimes it is included in the <main> element tag, but this may
    # change depending on the Wordpress theme adopted and on the organisation of the contents on the website
    main_section = soup.find("main")
    # Find all instances of the <article> tag, identifying the elements that contain the articles information; similar to the
    # <main> element tag, this may vary. A post/content may be labelled as e.g. 'article' or 'news', and may be identified by an
    # element tag such as <article> or <div class="news">. The script should therefore be adapted depending on the structure of the
    # website being scraped; if e.g. a <div class="news"> is employed, the syntax ("div", {"class": "news"}) should be used
    # instead of ("article")
    articles = main_section.find_all("article")
    # For each article found
    for article in articles:
        # Find the first heading tag
        article_title = article.find(heading_tags)
        # For each heading tag, find all the hyperlinks tags (<a>)
        for url in article_title.find_all("a"):
            print(url)
            # Extract the 'href' attribute containing the URL to the article, and add it to the 'links' list
            links.append(url["href"])
        # Wait two seconds before collecting the next article, to avoid making too many requests to the server
        sleep(2)
    # Increase the counter by 1
    start_page += 1