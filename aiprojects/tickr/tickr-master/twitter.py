#----------------------------------------------------------------------------------# 
# This file contains the TwitterAPI class, which handles Twitter API calls
#
# Authors: Allen Westgate, Bernardo Santos, and Ryan Farrell.
#----------------------------------------------------------------------------------# 

# Import all libraries.
import tweepy
import pandas as pd
import time
import re

# This class handles Twitter API calls, retrieving tweets containing the specified keywords.
# It only receives input in the Connect method, where the tickers used to search are passed
# (i.e.: ["Bitcoin", "BTC"]).
class TwitterAPI:

    # This is the constructor class, where the connection to the API is established.
    def __init__(self):
        self.consumer_key = "<key>"
        self.consumer_secret = "<key>"
        self.access_token = "<key>"
        self.access_token_secret = "<key>"
        self.auth = tweepy.AppAuthHandler("<key>", 
                                    "<key>")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # This method sends queries to the Twitter API in order to retrieve the tweets containing the 
    # keywords that we are looking for.
    def Connect(self, tickers):

        # Iterate over the tickers (i.e.: ["JPM", "GS", "MSFT"...])
        for ticker in tickers.keys():
            query = "('$" + ticker + " OR " + tickers[ticker] + "') -filter:retweets"
            language = "en"
            count = 12000
            curr = 0
            max_id = -1
            sinceId = None
            tweets_list = []

            # Retrieve data as much as possible before hitting the rate limit.
            # If the rate limit is reached, it will output a warning saying that it was reached.
            while curr < count:

                # When it retrieves a bunch of tweets, make sure the following tweets will not be duplicates
                # by using the max_id parameter.
                try:
                    if max_id <= 0:
                        if (not sinceId):
                            tweets = self.api.search(q=query, count=1000, lang=language, tweet_mode="extended")
                        else:
                            tweets = self.api.search(q=query, count=1000, lang=language,
                                                tweet_mode="extended", since_id=sinceId)
                    else:
                        if (not sinceId):
                            tweets = self.api.search(q=query, count=1000, lang=language,
                                                tweet_mode="extended", max_id=str(max_id-1))
                        else:
                            tweets = self.api.search(q=query, count=1000, lang=language,
                                                tweet_mode="extended", 
                                                since_id=sinceId,
                                                max_id=str(max_id-1))
                    
                    # If there are no more tweets available, break out of the loop.
                    if (not tweets):
                        print("No more tweets!")
                        break

                    # Add tweets to a list.
                    tweets_list += [[tweet.created_at, tweet.user.screen_name, tweet.full_text.encode('utf-8')] for tweet in tweets]
                    curr = len(tweets_list)
                    max_id = tweets[-1].id
                    print("Tweets retrieved so far: ", curr)
        
                # If there is any exception, break out.
                except BaseException as e:
                    print('Failed while retrieving tweets...', str(e))
                    time.sleep(3)
            
            # Write tweets to files.
            f = open("./tweets/" + ticker + "-tweets.txt", "w+", encoding="utf-8")
            for t in tweets_list:
                text = re.sub(r'https://t.*', '', t[2].decode("utf-8"), flags=re.MULTILINE)
                text = re.sub(r'\n', '', text, flags=re.MULTILINE)
                f.write((str(t[0]).split(" ")[0]) + " " + str(text))
                f.write("\n")
            f.close()
