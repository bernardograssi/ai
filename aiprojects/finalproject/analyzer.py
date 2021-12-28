#----------------------------------------------------------------------------------# 
#  This file contains the class that is responsible for analyzing the articles 
#  sentiments and outputting them to a text file to be used in the dashboard.
# 
#  Authors: Allen Westgate, Bernardo Santos, and Ryan Farrell.
#----------------------------------------------------------------------------------# 

# Import all libraries.
import json
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from autocorrect import Speller

# Download NLTK components.
nltk.download([
    'wordnet',
    'stopwords',
    'words',
    'punkt',
    'vader_lexicon'
])

# This class is the Analyzer, which receives a list of tickers and analyzes the articles of the given 
# tickers found in the database.
class Analyzer:

    # This is the constructor, which receives a dictionary of tickers as input (i.e.: {'GS':['goldman sachs', 'goldman', 'sachs', 'gs']}).
    def __init__(self, tickers):
        self.tickers = tickers
        self.stop_words = set(stopwords.words('english'))
        self.vocab = set(w.lower() for w in nltk.corpus.words.words())

    # This method returns True if a given word contains the keywords from the tickers dictionary.
    def match(self, word, ticker):
        for t in self.tickers[ticker]:
            if t in word:
                return True
        return False

    # This method analyzes the CNBC articles and the tweets from the companies passed as parameter.
    def analyze_cnbc_and_twitter(self):

        # Iterate over the companies names.
        for ticker in self.tickers.keys():
            print("Starting tweets analysis for", ticker)
            f = open("./tweets//" + ticker + "-tweets.txt", "r", encoding="utf-8")
            r = {
                "positive": 0,
                "negative": 0,
                "neutral": 0
                }
 
            sia = SentimentIntensityAnalyzer() # Create sentiment analysis model.
            text = ""
            counter = 0
            # Make the analysis for each tweet.
            for line in f: 
                counter += 1
                if counter % 1000 == 0:
                    print("Additional 1000 tweets analyzed!")
                text = re.sub(r'@[^\s]+',' ', line)
                text = text.lower().translate(str.maketrans("","", string.punctuation)).strip()
                words = text.split(" ")[1:]
                result = re.sub(r'\s{2,}', ' ', ' '.join(words))
                if self.match(result, ticker):
                    analysis = sia.polarity_scores(result)['compound']
                    if analysis >= 0.1:
                        r["positive"] += 1
                    elif analysis < 0.1 and analysis > -0.1:
                        r["neutral"] += 1
                    else:
                        r["negative"] += 1
                text = ""
            print()
            # Output the results to a .txt file.
            data = {ticker: r}
            with open("./sentiments/" + ticker + '-sentiments-tweets.txt', 'w+') as outfile:
                json.dump(data, outfile)


        # Iterate over the companies names.
        for ticker in self.tickers.keys():
            
            # Do not attempt to analyze bitcoin news.
            if "BTC" not in ticker:
                print("Starting news analysis for", ticker)
                r = {
                    "positive": 0,
                    "negative": 0,
                    "neutral": 0
                    }
                f = open("./articles//" + ticker +"-db.txt", "r", encoding="utf-8")
                lines = f.readlines()
                text = ""

                # Analyze articles' sentiments.
                for line in lines:
                    if line != "\n":
                        text += line
                    else:
                        analysis = sia.polarity_scores(text)['compound']
                        if analysis >= 0.1:
                            r["positive"] += 1
                        elif analysis < 0.1 and analysis > -0.1:
                            r["neutral"] += 1
                        else:
                            r["negative"] += 1
                        text = ""
                print()
                
                # Output results to .txt file.
                data = {ticker: r}
                with open("./sentiments//" + ticker + '-sentiments-cnbc.txt', 'w+') as outfile:
                    json.dump(data, outfile)
                print("Done with news analysis for", ticker)
