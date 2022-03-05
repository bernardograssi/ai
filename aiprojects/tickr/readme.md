# General Overview
This project was developed by me, Bernardo Grassi, alongside fellow classmates Allen Westgate and Ryan Farrell for our Final Project Assignment in our Artificial Intelligence Class in the Spring of 2021.

## Goal
The goal of the project is to produce a simple buy/hold/sell recommendation for the user, given the stock chosen.

Through the program dashboard, the user can pick a few stocks or a cryptocurrency to make predictions for. Of course, the predictions are short-term only, and do not tend to be accurate in terms of getting the exact value of the future prices, but has been reliable in our tests to find out the trend of the price (going up or down, or remaining still).

### Retrieving Data
A Machine Learning/A.I. project certainly needs some source for its data, and ours is no different. The Bitcoin data was downloaded manually from [CoinDesk.com](https://www.coindesk.com/price/bitcoin), a media outlet that focuses on sharing content about cryptocurrencies and blockchain.

The other source of data is the CNBC News page, which is used in the scraper.py file. Such file scrapes the CNBC page and retrieves the necessary information (articles' links and articles contents) given a specific company. Such information is exported to a text file.

Lastly, in the twitter.py file, the Twitter API is used in order to retrieve tweets about certain companies or about Bitcoin. The tweets are retrieved and exported to a text file. Of course, the API's keys have been deleted from the code and if the reader is eager to use the program, we would recommend getting your own API keys from [Twitter](https://developer.twitter.com/en/apply-for-access).

### Analyzing the Data
All the articles and tweets are analyzed using Natural Language Toolkit, with the results exported to text files. The goal of this analysis is to share with the user how that company/cryptocurrency is currently viewed by the public in general.

### Creating Machine Learning Models
Retrieving historical data using Yahoo Finance API (yfinance), we focused on creating Long Short-Term Memory models, which are simply Recurrent Neural Networks (RNN). Through Reinforcement Learning, the model created was able to fit well the data (daily stock prices since 01-01-2010) and make reliable short-term predictions. Root Mean Squared Error and R^2 Value metrics were used to check the models' performance in training/testing. 

Each company has a model created for its data, which is then saved and used when the dashboard is launched.

### Clustering
The program also relies on its clustering (K-means) model. The clustering.py file is responsible for clustering news articles retrieved from CNBC based on the relative frequency of words in each article. The cluster the latest article belonged to was used to predict the change in price over the following 24 hours.

### Dashboard
The dashboard contains two tabs: the stock data tab and the predictions tab. The former contains a simple graph with the historical data from a stock/cryptocurrency, which can be chosen through a dropdown. The latter contains 3 graphs:

1. The LSTM model training, testing, and validating data, which shows how the model has behaved throughout these three stages.
2. The clustering graph, showing which cluster each article belongs to.
3. The articles/tweets sentiments analysis, containing the number of positive/neutral/negative articles/tweets for a given company/cryptocurrency.

At the bottom, the user can see the recommendation: buy/hold/sell the stock/cryptocurrency based on an evaluation function developed by us, which consists of getting the moving average of the last 7 days' predictions of the LSTM model added to the clustering price prediction and divide that sum by 2. The result, then, is the prediction of the change in the price for the next 24-48 hours.

Please see Slides-Presentation.pdf for further explanation:
[Slides-Presentation.pdf](https://github.com/bernardograssi/ai/files/8191068/Santos-Farrell-Westgate-Slides.Presentation.pdf)
