#----------------------------------------------------------------------------------# 
#  This file is the driver for the whole project. 
#  It calls the necessary scripts to start the program by scraping tweets and news; 
#  it then moves on to train the 
#  Machine Learning models and use them to predict future values.
# 
#  Authors: Allen Westgate, Bernardo Santos, and Ryan Farrell.
#----------------------------------------------------------------------------------# 

# Import all files created for this program.
from scraper import Scraper
from twitter import TwitterAPI
from lstm import LSTMPredictor
from clustering import Cluster
from bitcoin import Bitcoin
from analyzer import Analyzer
from webdashboard import Dashboard

# This is the main class of the driver file, responsible for calling each of the files used to scrape news/tweets,
# analyze articles/tweets, train the Machine Learning models, and predict future values.
if __name__ == "__main__":

  # Scrape the CNBC page for articles.
  # Tip: use the data already saved in the project folder instead of running everything again,
  # otherwise it will take a long time!!!
  '''
  print("Starting scraping...")
  scraper = Scraper(
    {
      "JPM": "JPMorgan",
      "GS": "Goldman Sachs",
      "MSFT": "Microsoft",
      "AMZN": "Amazon",
      "AAPL": "Apple"
      }
    )
  scraper.Scrape()
  print("Scraping finished...") 
  '''

  # Retrieve tweets from the Twitter API.
  # Tip: use the data already saved in the project folder instead of running everything again,
  # otherwise it will take a long time!!!
  '''
  tt_tickers = { 'JPM': 'jpmorgan',
                  'GS': 'goldman sachs',
                  'MSFT': 'microsoft',
                  'AMZN': 'amazon',
                  'AAPL': 'apple',
                  'BTC': 'bitcoin' 
              }
  tt = TwitterAPI()
  tt.Connect(tt_tickers)
  '''

  # Train the LSMT Model for stock predictions.
  '''
  print("Start to train the models...")
  lstm = LSTMPredictor("2021-05-07", 60, ['JPM', 'GS', 'MSFT', 'AMZN', 'AAPL'])
  lstm.run_model()
  '''

  # Train the clustering model (K-means).
  '''
  print("Training clustering...")
  company_names = ["jpmorgan", "goldman%20sachs", "microsoft", "amazon", "apple"]
  ticker_names=["JPM","GS", "MSFT","AMZN","AAPL"]
  ticker_dict = {"jpmorgan": "JPM", "goldman%20sachs": "GS", "microsoft": "MSFT", "amazon": "AMZN", "apple": "AAPL"}
  cluster = Cluster(company_names, ticker_names, ticker_dict)
  '''

  # Analyze tweets and articles.
  '''
  print("Analzying tweets/articles...")
  analysis_tickers = {
    'JPM': ['jpmorgan', 'jpm', 'jp'],
    'GS': ['goldman sachs', 'goldman', 'sachs', 'gs'],
    'MSFT': ['microsoft', 'msft'], 
    'AMZN': ['amazon', 'amzn'],
    'AAPL': ['apple', 'aapl']
    }
  analyzer = Analyzer(analysis_tickers)
  analyzer.analyze_cnbc_and_twitter()
  '''

  #Finally, display dashboard to user.
  dashboard = Dashboard("2021-05-07",['JPM', 'GS', 'MSFT', 'AMZN', 'AAPL'], 60)