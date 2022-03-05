#----------------------------------------------------------------------------------# 
# This file contains the Scraper class, which is responsible for scraping the CNBC
# webpage and retrieving articles' links and headlines and storing them in text 
# files.
#
# Authors: Allen Westgate, Bernardo Santos, and Ryan Farrell.
#----------------------------------------------------------------------------------# 

# Import all libraries.
from bs4 import BeautifulSoup
from msedge.selenium_tools import EdgeOptions, Edge
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import requests
import yfinance as yf
import re
import pandas as pd

# This is the Scraper class. It receives only one parameter as input: a dictionary in which the keys
# are the companies tickers and the values are their names as they appear in the webpage header.
class Scraper:

    # Constructor method of the Scraper class.
    # Input: a dictionary with keys as tickers and values as names of the companies, i.e.: {"JPM": "jpmorgan"}.
    def __init__(self, data_in):
        self.data_in = data_in
    
    # This method scrapes the CNBC webpage, retrieving articles' links and headlines.
    def Scrape(self):
        # Scraping the CNBC page to retrieve news for each ticker received as input in the constructor.
        for ticker in self.data_in.keys():

            '''
            # If using Firefox as your webdriver, please use the following:

            firefox_options = webdriver.FirefoxOptions()
            firefox_options.headless = True
            driver = webdriver.Firefox(executable_path='geckodriver.exe', options=firefox_options)

            # And please comment lines 46-48.
            '''

            driver = webdriver.Edge(EdgeChromiumDriverManager().install()) # Use selenium webdriver in Microsoft Edge to scrape the web.
            options = EdgeOptions()
            options.use_chromium = True
            url = "https://www.cnbc.com/search/?query=" + self.data_in[ticker] +"&qsearchterm=" + self.data_in[ticker] # Build the URL.
            driver.get(url) # Get the elements of the webpage.
            time.sleep(5) # Sleep for 5 seconds.
            SCROLL_PAUSE_TIME = 2 # Time (in seconds) to pause in between scrolls.

            # Get scroll height.
            last_height = driver.execute_script("return document.body.scrollHeight")
            count = 0

            # Scroll 20 times over the page to get the news.
            while count < 20:
                count += 1
                # Scroll down to bottom.
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page.
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height.
                new_height = driver.execute_script("return document.body.scrollHeight")

                # If the end has been reached, break out of the loop.
                if new_height == last_height:
                    break
                last_height = new_height

            # Find the elements which contains the news blocks.
            container = driver.find_element_by_id("searchcontainer")
            news = container.find_elements_by_css_selector("*") # Get all the news.
            links = []
            added = ""

            # Iterate over the news found in the webpage and add the links found to a list.
            for n in news:
                if n.get_attribute("class") == "resultlink":
                    if n.get_attribute("href") != added and ("/video/" not in n.get_attribute("href")):
                        links.append(n.get_attribute("href"))
                        added = n.get_attribute("href")

            # Write the links to a text file.
            f = open("./links//" + ticker + ".txt", "w+", encoding="utf-8")
            for l in links:
                f.write(l + "\n")
            driver.close() # Close driver file.
        f.close() # Close articles' file.

        # For each ticker, get the link associated with each of the news and scrape the article webpage
        #  so that the whole body of the article can be scraped and stored in a text file.
        for ticker in self.data_in.keys():
            w = open("./articles//" + ticker + "-db.txt", "w+", encoding="utf-8") # Open file to write the articles at.
            f = open("./links//" + ticker + ".txt", "r", encoding="utf-8") # Open the file containing the links.
            lines = f.readlines()
            for l in lines:
                try:
                    date = re.findall("[0-9]{1,}/[0-9]{1,}/[0-9]{1,}", l)[0] # Get the date of the article.
                    page = requests.get(l.split(",")[0]) # Get the whole page.
                    soup = BeautifulSoup(page.text, 'html.parser') # Parse the page as a soup object.
                    article = soup.find_all("div", {"class": "ArticleBody-articleBody"})  # Find the body of the article.
                    
                # Write the article to the text file.
                    text = article[0].get_text()
                    w.write(date + ", " + text)
                    w.write("\n\n")
                except: pass
            
            # Close the files.
            f.close()
            w.close()
