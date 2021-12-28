#----------------------------------------------------------------------------------# 
#  This file contains the Cluster class, which is responsible for getting the news
#  articles and clustering them based on the price change for the company that is
#  talked about in the news.
# 
#  Authors: Allen Westgate, Bernardo Santos, and Ryan Farrell.
#----------------------------------------------------------------------------------#

# Import all libraries.
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import datetime
from scraper import Scraper
from datetime import timedelta
from os import path
from msedge.selenium_tools import EdgeOptions, Edge
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import json
import sys

# This is the Cluster class, which contains attributes such as companies names, ticker names, 
# and a ticker dictionary containing both the ticker and the name of the company to be used
# in the URL for data retrieval.
class Cluster:

    # This is the constructor class, which receives the companies names, tickers
    # names and ticker dictionary as input.
    def __init__(self, company_names, ticker_names, ticker_dict):
        self.company_names = company_names
        self.ticker_names = ticker_names
        self.ticker_dict = ticker_dict
        self.date = []
        self.news_list = []
        self.title = []
        self.news_dict = {}

    # This method performs the clustering (K-means) and outputs the result to a text file.
    # Input: 
    def Clustering(self, company, ticker):
        # Clear all lists/dictionaries.
        self.date.clear()
        self.news_list.clear()
        self.news_dict.clear()
        self.title.clear()

        # Check if database and content files already exist. If so, then just keep going and
        # get the most recent news, which is going to be used in the clustering model.
        if path.exists("./articles//" + ticker + "-db.txt")==False:
            inv_dict = {v: k for k, v in self.ticker_dict.iteritems()}
            scraper = Scraper(inv_dict)
            scraper.Scrape()

        '''
        # If using Firefox as your webdriver, please use the following:

        firefox_options = webdriver.FirefoxOptions()
        firefox_options.headless = True
        driver = webdriver.Firefox(executable_path='geckodriver.exe', options=firefox_options)

        # And please comment lines 70-72.
        '''

        # Scrape the CNBC page to get the most recent news article.
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        options = EdgeOptions()
        options.use_chromium = True
        
        url = "https://www.cnbc.com/search/?query=" + str(company) + "&qsearchterm=" + str(company)
        driver.get(url)
        time.sleep(5)

        container = driver.find_element_by_id("searchcontainer")
        time.sleep(5)

        news = container.find_elements_by_css_selector("*")
        time.sleep(5)

        link = ''
        loop_count = 0

        while link == '' and loop_count < 1000:
            loop_count += 1 
            for n in news:
                if n.get_attribute("class") == "resultlink":
                    if "/video/" not in n.get_attribute("href") and \
                        ("/amazon-rising/" not in n.get_attribute("href")) \
                            and ("id" not in n.get_attribute("href")) and ("/select/" not in n.get_attribute("href")) and \
                                ("jpmorgan-ceo-jamie-dimon-shares-success-advice-to-college-graduates" not in n.get_attribute("href")) and\
                                    ("china-stock-picks-goldman-sachs-likes" not in n.get_attribute("href")):
                        link=n.get_attribute("href")
                        print(link)
                        break

        driver.close() # Close the driver.

        # Get the article page and parse it using BeautifulSoup.
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        article = soup.find_all("div", {"class": "ArticleBody-articleBody"})
        newTitle=soup.find("h1", {"class": "ArticleHeader-headline"})
        newTitle=str(newTitle).replace("<h1 class=\"ArticleHeader-headline\">","")
        self.date.append(soup.find("", {"class": ""}))

        try:
            self.news_dict[newTitle]=article[0].get_text()
        except:
            print(newTitle)
        stock_ticker=yf.Ticker(ticker)
        startDate=datetime.datetime.strptime("2017/01/01","%Y/%m/%d")
        hist = stock_ticker.history(start=startDate)
        change_list= [0]

        # Read the content file for the given company.
        counter=0
        r=open("./articles//" + ticker + "-db.txt","r",encoding="utf-8")
        lines = r.readlines()

        # Iterate over all articles bodies.
        for l in lines:

            # Check if line is not empty.
            if l != "\n":
                parts=l.split(",",1)
                if counter==100:
                    break
                openPrice=0
                closePrice=0

                # Find date of the article.
                dateObj=datetime.datetime.strptime(parts[0].rstrip(),"%Y/%m/%d")

                # Find the next day of the article date.
                nextDay=dateObj+timedelta(days=2)

                # Check if the date is in our historical dataset (check if article was not published on a weekend, or holiday).
                if str(dateObj).removesuffix(" 00:00:00") in hist.index:

                    # Get the open price on the day the article was created.
                    openPrice=hist.loc[str(dateObj).removesuffix(" 00:00:00"),"Open"]

                    # Get the close price on the day after the article was created.
                    closePrice = hist.loc[str(dateObj).removesuffix(" 00:00:00"), "Close"]

                    # Check if the next day is in our stock values historical data.
                    if str(nextDay).removesuffix(" 00:00:00") in hist.index:
                        closePrice=hist.loc[str(nextDay).removesuffix(" 00:00:00"),"Close"]

                # Add the change for each article to a list.
                change_list.append(closePrice-openPrice)
                self.news_dict[counter] = parts[1] 
                counter+=1

            try:
                if parts[0] not in self.news_dict.keys():
                    self.news_dict[parts[0]] = parts[2]
            except:
                pass

            counter+=1

        for link in self.news_dict:
            self.news_list.append(self.news_dict[link])
            self.title.append(link)

        # Initialize the TfidVectorizer model.
        vectorizer = TfidfVectorizer(stop_words={'english'})
        X = vectorizer.fit_transform(self.news_list) # Fit the news list to the model.

        true_k = 10 # Define the k value.

        # Create and fit the K-means model.
        model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=10)
        model.fit(X)
        labels=model.labels_
        news_cl=pd.DataFrame(list(zip(self.title,labels)),columns=['title','cluster'])
        news_cl['change']=change_list

        clusterholder=[]
        changeholder=[]

        # Append cluster info (data points) to lists clusterholder and changeholder (x and y, respectively).
        for index, row in news_cl.iterrows():
            clusterholder.append(int(row['cluster']))
            changeholder.append(int(row['change']))
        
        # Write the clustering data to the <companyname>clusteringdata.txt file.
        f = open("./clustering/clusteringdata" + self.ticker_dict[company] + ".txt", "w+")
        for i, j in zip(clusterholder, changeholder):
            f.write(str(i) + "," + str(j) + "\n") 
        f.close()

        # Return the change in price prediction to the caller.
        try:
            cluster=news_cl.loc[news_cl['title'] == newTitle].iloc[0]['cluster']
            change_prediction=news_cl.groupby(['cluster']).mean().iloc[cluster]['change']
            return change_prediction
        except:
            return 0

    # This is the driver of the class, which performs clustering for each of the companies passed as parameter
    # in the constructor.
    def Driver(self):
        result = {}
        for i in range(len(self.company_names)):
            ticker = self.ticker_dict[str(self.company_names[i])]
            result[ticker] = str(self.Clustering(self.company_names[i],self.ticker_names[i]))
            with open("./clustering/" + ticker + '-clustering.txt', 'w+') as outfile:
                json.dump(result[ticker], outfile)
