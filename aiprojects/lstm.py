#----------------------------------------------------------------------------------# 
#  This file contains the Long Short-Term Memory (LSTM) Machine Learning model
#  that is used to predict future values of stocks.
# 
#  Authors: Allen Westgate, Bernardo Santos, and Ryan Farrell.
#----------------------------------------------------------------------------------# 

# Import all libraries.
import math
import torch
import numpy as np
import pandas as pd
import pandas_datareader as web
import yfinance as yf
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Activation
from sklearn.metrics import r2_score
pd.options.mode.chained_assignment = None

# This is the LSTM Model class, which receives a limit date for data retrieval from the Yahoo Finance API (i.e.: 2021-05-07);
# it also receives the train size as an input, and the tickers containing the stock market tickers for the companies (i.e.: JPM for JPMorgan).
class LSTMPredictor:

    # This is the constructor class.
    # Input: limit date for data retrieval, train size, and company tickers.
    def __init__(self, limit, train_size, tickers):
        self.train_size = train_size
        self.limit = limit
        self.tickers = tickers

    # This method trains, tests and saves the LSTM model.
    def run_model(self):

        # Train, test, and save a model for each of the tickers received as input in the constructor.
        for ticker in self.tickers:
            df = web.DataReader(ticker, data_source='yahoo', start='2010-01-01', end=self.limit) # Get stock historical data from Yahoo Finance API.

            # Get the column that is important to us, which is the 'Close' column.
            close_df = df.filter(['Close'])
            dataset = close_df.values
            length_train = math.ceil(len(dataset) * .7)

            # Scale the data.
            scaler = MinMaxScaler(feature_range=(0,1))
            scaled_data = scaler.fit_transform(dataset)

            # Separate the data into train and test sets.
            train_data = scaled_data[0:length_train,:]
            x_train, y_train = [], []
            for i in range(self.train_size, len(train_data)):
                x_train.append(train_data[i-self.train_size:i, 0])
                y_train.append(train_data[i,0])

            x_train, y_train = np.array(x_train), np.array(y_train)
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

            print("Training model for", ticker, "...") # Print ticker name to track progress.

            # Initialize the model and add the necessary layers to it.
            model = Sequential()
            model.add(LSTM(256, return_sequences=True, input_shape=(x_train.shape[1], 1)))
            model.add(LSTM(256, return_sequences=False))
            model.add(Dense(25))
            model.add(Dense(1))

            # Compile and fit the model to the train dataset.
            model.compile(optimizer='adam', loss='mean_squared_error')
            model.fit(x_train, y_train)

            # Test the model by making predictions.
            test_data = scaled_data[length_train - self.train_size:, :]
            x_test, y_test = [], dataset[length_train:, :]
            for i in range(self.train_size, len(test_data)):
                x_test.append(test_data[i-self.train_size:i,0])
            x_test = np.array(x_test)
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
            predictions = model.predict(x_test)
            predictions = scaler.inverse_transform(predictions)

            # Calculate the Root Mean Squared Error, which represents how off the predictions are from the real test data.
            rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
            print("RMSE:", rmse)

            valid = df[length_train:]
            valid['Predictions'] = predictions.copy()

            # Get the R-Squared value, which basically represents how certain the model is in the predictions that it is making.
            # The closest this value is to 1, the better.
            print("R^2:", r2_score(valid['Close'].values, valid['Predictions'].values))

            # Test the model again to predict for tomorrow.
            quote = web.DataReader(ticker,data_source='yahoo', start='2010-01-01', end=self.limit)
            new_df = quote.filter(['Close'])
            last_data = new_df[-self.train_size:].values
            last_data_scaled = scaler.transform(last_data)
            x_test = []
            x_test.append(last_data_scaled)
            x_test = np.array(x_test)
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

            # Predict the price for the short term.
            pred_price = model.predict(x_test)
            pred_price = scaler.inverse_transform(pred_price)

            # Save the model.
            model.save("./models/" + ticker + self.limit + ".h5")
            print("Model saved! ")
            print()