# Import modules for: regular expressions and for working with local files; List to enforce the type of data collected
# (this is only required for Python < 3.9), and selected functions from Selenium
import re
import os
from typing import List
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Define the scraper as a class of objects
class ChatLogScraper(object):
    # Define the first function that sets the initial parameters: the starting URL, the regular expression to match the chatlog contents, as well as further options for Selenium
    def __init__(self):
        """Init function, defines some class variables."""
        self.home_url = "http://www.perverted-justice.com/?con=full"

        # Setup and compile the regular expression for later
        master_matcher = r"([\s\w\d]+)[:-]?\s(?:\(.*\s(\d+:\d+:\d+\s[AP]M)\))?:?((.*)(\s\d+:\d+\s[AP]M)|(.*))"
        self.chat_instance = re.compile(
            master_matcher, re.IGNORECASE
        )  # ignore case may not be necessary

        # Instantiate the firefox driver in headless mode, disable all css, images, etc
        here = os.path.dirname(os.path.realpath(__file__))
        executable = os.path.join(here, "chromedriver")
        # Set the headless command to run Firefox without a graphical interface
        options = Options()
        options.add_argument("--headless")
        self.driver = Chrome(executable_path=executable, chrome_options=options)

    # Define the 'start' function that searches and returns all the links found in the web pages and returns them as strings
    def start(self) -> List[str]:
        """Main function to be run, go to the home page, find the list of cases,
        then send a request to the scrape function to get the data from that page

        :return: list of links to scrap
        """
        print("loading main page")
        self.driver.get(self.home_url)

        main_pane = self.driver.find_element_by_id("mainbox")
        all_cases = main_pane.find_elements(
            By.TAG_NAME, "li"
        )  # every case is under an LI tag
        # We'll load the href links into an array to get later
        links = []
        for case in all_cases:
            a_tags = case.find_elements(By.TAG_NAME, "a")
            # The first a tag, is the link that we need
            links.append(a_tags[0].get_attribute("href"))
        return links

    # Define the 'scrape_page' function which, starting from the previously collected URLs, parses the content of each chatlog page and extracts the username, content (statement) and timestamp of each message
    def scrape_page(self, page_url: str) -> List[dict]:
        """Go to the page url, use the regular expression to extract the chatdata, store
        this into a temporary pandas data frame to be returned once the page is complete.

        :param page_url: (str) the page to scrap
        :return: pandas DataFrame of all chat instances on this page
        """
        self.driver.get(page_url)
        try:
            page_text = self.driver.find_element(By.CLASS_NAME, "chatLog").text
        except NoSuchElementException:
            print("could not get convo for", page_url)
            return []  # Some pages don't contain chats
        conversations = []

        # Next, we'll run the regex on the chat-log and extract the info into a formatted pandas DF
        matches = re.findall(self.chat_instance, page_text)
        for match in matches:
            # Clean up false negatives
            if (
                "com Conversation" not in match[0]
                and "Text Messaging" not in match[0]
                and "Yahoo Instant" not in match[0]
            ):
                username = match[0]
                if match[4]:
                    statement = match[3]
                    time = match[4]
                else:
                    statement = match[5]
                    time = match[1]
                conversations.append(
                    {"username": username, "statement": statement, "time": time}
                )
        return conversations


# The functions above are executed and the collected data is saved to a CSV file and a JSON file
if __name__ == "__main__":
    chatlogscrapper = ChatLogScraper()
    conversations = []
    links = chatlogscrapper.start()

    try:
        for index, link in enumerate(links):
            print("getting", link)
            conversations += chatlogscrapper.scrape_page(link)
    finally:
        conversations = pd.DataFrame(conversations)
        conversations.to_csv("output.csv", index=False)
        conversations.to_json("output.json")