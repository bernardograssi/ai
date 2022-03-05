#----------------------------------------------------------------------------------# 
#  This file contains the Long Short-Term Memory (LSTM) Machine Learning model
#  that is used to predict future values of Bitcoin.
# 
#  Authors: Allen Westgate, Bernardo Santos, and Ryan Farrell.
#----------------------------------------------------------------------------------# 

# Import all libraries.
import numpy as np 
import pandas as pd
import math 
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Activation, Dropout
from sklearn.metrics import r2_score
import seaborn as sns
from keras.models import load_model
pd.options.mode.chained_assignment = None

# This is the Bitcoin class, which trains, tests, and saves the LSTM model to predict short term values for Bitcoin.
# It receives a train size and a path to a file containing the Bitcoin price data as input in the constructor.
class Bitcoin:

    # This is the constructor of the Bitcoin class.
    def __init__(self, train_size, path):
        self.train_size = train_size
        self.path = path

    # This method trains, tests, and saves the Bitcoin LSTM model.
    # The training parameter is a boolean value that determines if the model is to be trained and saved, or used to predict only.
    # If training, then the model will be created from scratch, trained, tested, and saved. If not training, then the model will be 
    # only used for making a prediction based on the model already saved.
    def run_model(self, training):

        # Read the data from the .csv file and make the necessary changes in columns' names and indeces.
        df = pd.read_csv(self.path)
        df.rename(columns={"Currency": "Stock", "24h High (USD)": "High", "24h Low (USD)": "Low", "Closing Price (USD)": "Close"}, inplace=True)
        df = df.set_index('Date')
        df['Stock'] = 'BTC'
        close_df = df.filter(['Close'])
        dataset = close_df.values
        length_train = math.ceil(len(dataset) * .9)

        # Scale the data.
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(dataset)

        # Separat the data into train and test sets.
        train_data = scaled_data[0:length_train,:]
        x_train, y_train = [], []
        for i in range(self.train_size, len(train_data)):
            x_train.append(train_data[i-self.train_size:i, 0])
            y_train.append(train_data[i,0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        print()
        # If training boolean is set to True, then create the model, train, test, and save it.
        if training:
            print("Training the BTC model...")
            # Initialize the LSTM model.
            model = Sequential()
            model.add(LSTM(256, return_sequences=True, input_shape=(x_train.shape[1], 1)))
            model.add(LSTM(256, return_sequences=False))
            model.add(Dropout(0.1))
            model.add(Dense(25))
            model.add(Dense(1))

            # Compiling the LSTM model.
            model.compile(optimizer='adam', loss='mean_squared_error')
            model.fit(
                x_train,
                y_train
            )
        else:
            # If not training, then load the model from the .h5 file.
            print("Loading BTC model...")
            model = load_model('./models/BTC.h5')

        # Test the model and make predictions.
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
        print("Bitcoin RMSE:", rmse)

        train = df[:length_train]
        valid = df[length_train:]
        valid['Predictions'] = predictions.copy()

        # Get the R-Squared value, which basically represents how certain the model is in the predictions that it is making.
        # The closest this value is to 1, the better.
        print("Bitcoin R^2:", r2_score(valid['Close'].values , valid['Predictions'].values))

        # Test the model again to predict for tomorrow.
        quote = df
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

        # If training value is set to True, then save the model. 
        # Otherwise, return the dataframe, the train model, the valid dataframe, and the predicted price for tomorrow.
        if training:
            model.save("./models/BTC.h5")
        else:
            return df, train, valid, pred_price[0][0]
