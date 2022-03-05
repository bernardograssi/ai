#----------------------------------------------------------------------------------# 
#  This file contains the class that is responsible for running the Dash server, 
#  which provides a dashboard for the user to look at stock/crypto data and look
#  at our recommendation based on our models works.
# 
#  Authors: Allen Westgate, Bernardo Santos, and Ryan Farrell.
#----------------------------------------------------------------------------------# 

# Import all libraries.
import json
import math
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
import numpy as np
import pandas_datareader as web
from bitcoin import Bitcoin
pd.options.mode.chained_assignment = None

# This class builds a dashboard for the user to interact with and see our 
# recommendations for some stocks/cryptocurrencies.
class Dashboard:

    # This is the constructor method, which receives a limit (date) as input.
    def __init__(self, limit, tickers, train_size):

        # Create and start Dash app.
        app = dash.Dash()
        server = app.server

        # Get the Bitcoin model's data before moving to any stock data.
        keys = {}
        btc_df, btc_train, btc_valid, btc_pred = Bitcoin(120, "./BTC-USD.csv").run_model(False)
        keys["BTC"] = {
            "df": btc_df, 
            "train": btc_train,
            "valid": btc_valid,
            "pred": btc_pred,
            "x": [0],
            "y": [0]
        }
        print()

        # Iterate over the companies' models and get the predictions results based on the models
        # saved and the clustering.
        # The process is quite similar to the lstm.py file, just makes predictions in the end so
        # that the values can be used to make our recommendations.
        for ticker in tickers:
            print("Loading model for", ticker)
            df = web.DataReader(ticker, data_source='yahoo', start='2010-01-01', end=limit)
            df['Stock'] = ticker

            close_df = df.filter(['Close'])
            dataset = close_df.values
            length_train = math.ceil(len(dataset) * .7)

            scaler = MinMaxScaler(feature_range=(0,1))
            scaled_data = scaler.fit_transform(dataset)

            train_data = scaled_data[0:length_train,:]
            x_train, y_train = [], []
            for i in range(train_size, len(train_data)):
                x_train.append(train_data[i-train_size:i, 0])
                y_train.append(train_data[i,0])

            x_train, y_train = np.array(x_train), np.array(y_train)
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

            # Load the model.
            model = load_model('./models/' + ticker + limit + '.h5')

            test_data = scaled_data[length_train - train_size:, :]
            x_test, y_test = [], dataset[length_train:, :]
            for i in range(train_size, len(test_data)):
                x_test.append(test_data[i-train_size:i,0])
            x_test = np.array(x_test)
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
            predictions = model.predict(x_test)
            predictions = scaler.inverse_transform(predictions)

            rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
            print(ticker, "RMSE: ", rmse)

            train = df[:length_train]
            valid = df[length_train:]
            valid['Predictions'] = predictions.copy()

            r2 = r2_score(valid['Close'].values , valid['Predictions'].values)
            print(ticker, "R^2: ", r2)
            print()

            quote = web.DataReader(ticker,data_source='yahoo', start='2010-01-01', end=limit)
            new_df = quote.filter(['Close'])
            last_60 = new_df[-train_size:].values
            last_60_scaled = scaler.transform(last_60)
            x_test = []
            x_test.append(last_60_scaled)
            x_test = np.array(x_test)
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
            pred_price = model.predict(x_test)
            pred_price = scaler.inverse_transform(pred_price)

            f = open('./clustering/clusteringdata' + ticker + ".txt", "r")
            x_cluster, y_cluster = [], []
            for r in f.readlines():
                line = r.split(",")
                x_cluster.append(line[0])
                y_cluster.append(line[1])
            f.close()

            # Create a dictionary with the data needed in the dashboard with the following items:
            # the dataframe with the historical data, the train and validation sets, the prediction,
            # and the cluster values.
            keys[ticker] = {
                "df": df, 
                "train": train,
                "valid": valid,
                "pred": pred_price[0][0],
                "x": x_cluster,
                "y": y_cluster
            }

        # Set up the layout for the graph of the clustering data.
        scatter = dcc.Graph(
            id = "scatterPlot",
            figure = {
                "data": {
                    "x": [1,2,3,4],
                    "y": [1,2,3,4],
                    "name": "Change in Price per Cluster"
                },
                "layout": {
                                "title": dict(text="News Clustering and Change in Price",
                                font=dict(size=20, color='black')),
                                "paper_bgcolor": "#ffffff",
                                "width": "2000",
                                "annotations": [
                                    {
                                        "font": {
                                            "size": 20
                                        },
                                        "showarrow": False,
                                        "text": "",
                                        "x": 0.2,
                                        "y": 0.2
                                    }
                                ],
                                "showlegend": False
                            }
            }
        )

        # Set up the layout for the Articles Sentiments graph.
        bar = dcc.Graph(
                id = "barGraph",
                figure ={
                        "data": [
                        {
                                'x':['Positive', 'Negative', 'Neutral'],
                                'y':[],
                                'name':'Sentiment',
                                'type':'bar',
                                'marker': dict(color=['#05C7F2','#D90416','#D9CB04']),
                        }],
                        "layout": {
                            "title" : dict(text ="Overall Articles Sentiments",
                                            font =dict(
                                            size=20,
                                            color = 'black')),
                            "xaxis" : dict(tickfont=dict(
                                color='black')),
                            "yaxis" : dict(tickfont=dict(
                                color='black')),
                            "paper_bgcolor":"#ffffff",
                            "plot_bgcolor":"#ffffff",
                            "width": "2000",
                            "annotations": [
                                {
                                    "font": {
                                        "size": 20
                                    },
                                    "showarrow": False,
                                    "text": "",
                                    "x": 0.2,
                                    "y": 0.2
                                }
                            ],
                            "showlegend": False
                        }
                    }
        )

        # Define layout of the Dash app.
        app.layout = html.Div(
        [
            html.H1("Stock/Crypto Price Prediction Dashboard", style={"textAlign": "center"}),
            dcc.Tabs(id="tabs", children=[

                # First tab: Stock Data.
                dcc.Tab(label="Stock Data", children=[
                    html.Div([
                        html.H1("Companies/Crypto Highs vs. Lows",style={'textAlign':'center'}),
                        dcc.Dropdown(id='my-dropdown',
                                    options=[{'label': 'JPMorgan', 'value': 'JPM'},
                                            {'label': 'Goldman Sachs', 'value': 'GS'},
                                            {'label': 'Microsoft', 'value': 'MSFT'},
                                            {'label': 'Amazon', 'value': 'AMZN'}, 
                                            {'label': 'Apple', 'value': 'AAPL'},
                                            {'label': 'Bitcoin/U.S. Dollar', 'value': 'BTC'}],
                                            style={"display":"block",
                                                    "margin-left":"auto",
                                                    "margin-right":"auto",
                                                    "width":"60%"}
                                            ),
                        dcc.Graph(id='highlow')
                                            
                    ], className="container"),
                ]),

                # Second tab: Predictions.
                dcc.Tab(label='Predictions', children=[
                    html.Div([
                        html.H1("LSTM Model: How It Performed",style={'textAlign':'center'}),
                        dcc.Dropdown(id='my-dropdown2',
                                    options=[{'label': 'JPMorgan', 'value': 'JPM'},
                                            {'label': 'Goldman Sachs', 'value': 'GS'},
                                            {'label': 'Microsoft', 'value': 'MSFT'},
                                            {'label': 'Amazon', 'value': 'AMZN'}, 
                                            {'label': 'Apple', 'value': 'AAPL'},
                                            {'label': 'Bitcoin/U.S. Dollar', 'value': 'BTC'}],
                                            style={"display":"block",
                                                    "margin-left":"auto",
                                                    "margin-right":"auto",
                                                    "width":"60%"}
                                            ),
                        dcc.Graph(id='highlow2'),
                        html.Div([
                            html.Div([scatter]),
                            html.Div([bar]),
                            html.Div([
                                html.H4( 
                                children='Recommendation: ',
                                style={
                                    'textAlign': 'center',
                                    'color': 'black',
                                }
                                ),

                                html.P(id="text",
                                children="---",
                                style={
                                    'textAlign': 'center',
                                    'color': 'black',
                                    'fontSize': 30
                                }
                                ),

                                html.P(id="sub-text",
                                    children="---",
                                        style={
                                            'textAlign': 'center',
                                            'color': 'black'
                                        }
                                )
                            ],style={'textAlign': 'center'})
                        ])
                    ],
                    
                    className="container"),
                ])
            ])
        ])

        # This is the evaluation function, used to evaluate the predicted result taking into account the 
        # result from the LSTM Model and the Clustering.
        # Input: ticker of the stock/crypto.
        # Output: a list containin the result of the prediction as a float, and the recommendation itself (either buy, hold, or sell). 
        def eval_function(ticker):
            last_real = float(keys[ticker]["df"]["Close"].iloc[-1:]) # Get the last real value for given stock.
            pred_ = keys[ticker]["pred"] # Predicted results for the given stock.
            result = []

            # Get the moving average of the last 7 days.
            predictions_mean = float(keys[ticker]["valid"]["Predictions"].rolling(window=7).mean()[-1:])

            # Get the clustering prediction from a .txt file.
            if ticker != "BTC":
                f = open("./clustering//" +  ticker + "-clustering.txt", "r", encoding="utf-8")
                f_value = (float(f.read()[1:5]))
                f.close()
                clustering_change = f_value / last_real
                final_pred = round(pred_ / predictions_mean * 100 - 100, 2) + clustering_change 
                if final_pred > 0:
                    result.append(f'Buy {ticker}')
                elif final_pred == 0:
                    result.append(f'Hold {ticker}')
                else:
                    result.append(f'Sell {ticker}')
                result.append(round(final_pred,2))
            else:
                if pred_ > predictions_mean:
                    result.append(f'Buy {ticker}')
                elif pred_ == predictions_mean:
                    result.append(f'Hold {ticker}')
                else:
                    result.append(f'Sell {ticker}')
                result.append(round(pred_ / predictions_mean * 100 - 100, 2))
            return result

        # This method updates the 'highlow' graph, which is the only graph of the first page.
        # Input: a selection of the dropdown section.
        # Output: the figure of the graph, updated.
        @app.callback(Output('highlow', 'figure'),
                    [Input('my-dropdown', 'value')])
        def update_graph(selected_dropdown):
            dropdown = {"JPM": "JPMorgan","GS": "Goldman Sachs","MSFT": "Microsoft", "AMZN": "Amazon",
                        "AAPL": "Apple", "BTC": "Bitcoin/U.S. Dollar"}
            trace1 = []
            trace2 = []
            stock = selected_dropdown
            name = "---"

            # If any value is selected in the dropdown.
            if selected_dropdown is not None:

                # Add the historical data to the graph.
                df = keys[stock]["df"]
                trace1.append(
                    go.Scatter(x=list(df[df["Stock"] == stock].index),
                                y=df[df["Stock"] == stock]["High"],
                                mode='lines', opacity=0.7, 
                                name=f'High {dropdown[stock]}',textposition='bottom center'))
                trace2.append(
                    go.Scatter(x=df[df["Stock"] == stock].index,
                                y=df[df["Stock"] == stock]["Low"],
                                mode='lines', opacity=0.6,
                                name=f'Low {dropdown[stock]}',textposition='bottom center'))
                name = selected_dropdown
            traces = [trace1, trace2]
            data = [val for sublist in traces for val in sublist]
            figure = {'data': data,
                        'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                                    '#FF7400', '#FFF400', '#FF0056'],
                    height=600,
                    title=f"High and Low Prices for " + name + " Over Time",
                    xaxis={"title":"Date",
                            'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                                'step': 'month', 
                                                                'stepmode': 'backward'},
                                                                {'count': 6, 'label': '6M', 
                                                                'step': 'month', 
                                                                'stepmode': 'backward'},
                                                                {'step': 'all'}])},
                            'rangeslider': {'visible': True}, 'type': 'date'},
                        yaxis={"title":"Price (USD)"})}
            return figure

        # This method updates the figures of the given graphs, based on input from the dropdown.
        # Input: dropdown selection from the page.
        # Output: the 3 figures (graphs) of page 2 and the recommendation to the user.
        @app.callback(Output('highlow2', 'figure'),
                    Output('scatterPlot', 'figure'),
                    Output('barGraph', 'figure'),
                    Output('text','children'),
                    Output('text', 'style'),
                    Output('sub-text', 'children'),
                    [Input('my-dropdown2', 'value')])
        def update_figure(selected_dropdown):
            trace1, trace2, values_bar = [], [], []
            recommendation, sub_r = "---", "---"
            
            # Style used on the bottom of the page for the recommendation section.
            style = {
                'textAlign': 'center',
                'color': 'black',
                'fontSize': 30
                    }

            # If any ticker value is selected in the dropdown.
            if selected_dropdown is not None:

                # Read the sentiments values from the sentiments text files: for articles and tweets.
                if selected_dropdown == "BTC":
                    cnbc_sentiments = [0,0,0]
                else:
                    with open('./sentiments/' + selected_dropdown + '-sentiments-cnbc.txt') as json_file:
                        json_cnbc = json.load(json_file)
                        cnbc_sentiments = list(list(json_cnbc.values())[0].values())

                with open('./sentiments/' + selected_dropdown + '-sentiments-tweets.txt') as json_file:
                    json_tweet = json.load(json_file)
                    tweets_sentiments = list(list(json_tweet.values())[0].values())

                # Set up the values used in the sentiments graph.
                values_bar = [cnbc_sentiments[i] + tweets_sentiments[i] for i in range(0,3)]

                train = keys[selected_dropdown]["train"]
                valid = keys[selected_dropdown]["valid"]

                # Add the data of the first graph to the lists.
                # This data is the Machine Learning model data: training, testing, and validation sets.
                trace1.append(
                go.Scatter(x=train.index,
                            y=train['Close'],
                            mode='lines', opacity=0.7, 
                            name=f'Train for {selected_dropdown}',textposition='bottom center'))
                trace2.append(
                go.Scatter(x=valid.index,
                            y=valid["Close"],
                            mode='lines', opacity=0.6,
                            name=f'Validation for {selected_dropdown}',textposition='bottom center'))

                trace2.append(
                go.Scatter(x=valid.index,
                            y=valid["Predictions"],
                            mode='lines', opacity=0.6,
                            name=f'Prediction for {selected_dropdown}',textposition='bottom center'))

                # Get the recommendation based on the eval function.
                recommendation = eval_function(selected_dropdown)[0]
                sub_r = eval_function(selected_dropdown)[1]

                # Define the recommendation output based on the value returned from the eval.
                if sub_r == 0:
                    sub_r = "The price will hold still for the next few days."
                    color = 'grey'
                elif sub_r > 0:
                    sub_r = "The price will increase by around " + str(sub_r) + r"% in the following days."
                    color = 'green'
                else:
                    sub_r = "The price will decrease by around " + str(sub_r) + r"% in the following days."
                    color = 'red'

                style = {
                'textAlign': 'center',
                'color': color,
                'fontSize': 30
                }

                # Set up the layout and the data of the 2nd graph of page 2: the clustering data.
                figure2 = go.Figure()

                # Add the regular markers.
                figure2.add_trace(
                go.Scatter(
                    mode='markers',
                    x=keys[selected_dropdown]["x"],
                    y=keys[selected_dropdown]["y"],
                    marker=dict(
                        color='LightSkyBlue',
                        size=10,
                        opacity=1,
                        line=dict(
                            color='MediumPurple',
                            width=2
                        )
                    ),
                    showlegend=False
                    )
                )

                # Add the star marker.
                figure2.add_trace(
                go.Scatter(
                    mode='markers',
                    x=[0],
                    y=[0],
                    marker=dict(
                        color='LightSkyBlue',
                        symbol='star',
                        size=20,
                        opacity=1,
                        line=dict(
                            color='MediumPurple',
                            width=2
                        )
                    ),
                    showlegend=False
                    )
                )

                # Update figure so that the axes have their labels ordered.
                figure2.update_yaxes(categoryorder='category ascending') 
                figure2.update_xaxes(categoryorder='category ascending') 
                figure2.update_layout(title="Price Change/Cluster")
                figure2.update_yaxes(title='Price Change')
                figure2.update_xaxes(title='Cluster')

                # Set up the layout and the data for the 3rd figure of page 2.
                figure3 ={
                        "data": [
                        {
                                'x': ['Positive', 'Negative', 'Neutral'],
                                'y': values_bar,
                                'name':'Sentiments Analysis',
                                'type':'bar',
                                'marker' :dict(color=['#05C7F2','#D90416','#D9CB04']),
                        }],
                        "layout": {
                            "title" : dict(text ="Overall Articles Sentiments",
                                            font =dict(
                                            size=20,
                                            color = 'black')),
                            "xaxis" : dict(tickfont=dict(
                                color='black')),
                            "yaxis" : dict(tickfont=dict(
                                color='black')),
                            "paper_bgcolor":"#ffffff",
                            "plot_bgcolor":"#ffffff",
                            "width": "1500",
                            "annotations": [
                                {
                                    "font": {
                                        "size": 20
                                    },
                                    "showarrow": False,
                                    "text": "",
                                    "x": 0.2,
                                    "y": 0.2
                                }
                            ],
                            "showlegend": False
                        }
                    }

            else:
                # If nothing has been selected, then set graph to default.
                figure2 = go.Scatter(
                    x = [0],
                    y = [0],
                    mode="markers"
                )

                # If nothing has been selected, then set graph to default.
                figure3 = {
                        "data": [
                        {
                                'x':['Positive', 'Negative', 'Neutral'],
                                'y':[],
                                'name':'Sentiment Analysis',
                                'type':'bar',
                                'marker' :dict(color=['#05C7F2','#D90416','#D9CB04']),
                        }],
                        "layout": {
                            "title" : dict(text ="Overall Articles Sentiments",
                                            font =dict(
                                            size=20,
                                            color = 'black')),
                            "xaxis" : dict(tickfont=dict(
                                color='black')),
                            "yaxis" : dict(tickfont=dict(
                                color='black')),
                            "paper_bgcolor":"#ffffff",
                            "plot_bgcolor":"#ffffff",
                            "width": "1500",
                            "annotations": [
                                {
                                    "font": {
                                        "size": 20
                                    },
                                    "showarrow": False,
                                    "text": "",
                                    "x": 0.2,
                                    "y": 0.2
                                }
                            ],
                            "showlegend": False
                        }
                    }
            
            # Show how the LSTM model performed, by plotting the graph with training, testing, 
            # and validation data.
            traces = [trace1, trace2]
            data = [val for sublist in traces for val in sublist]
            figure = {'data': data,
                    'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                                    '#FF7400', '#FFF400', '#FF0056'],
                    height=600,
                    title="Training and Testing Data",
                    xaxis={"title":"Date",
                        'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                            'step': 'month', 
                                                            'stepmode': 'backward'},
                                                            {'count': 6, 'label': '6M', 
                                                            'step': 'month', 
                                                            'stepmode': 'backward'},
                                                            {'step': 'all'}])},
                        'rangeslider': {'visible': True}, 'type': 'date'},
                    yaxis={"title":"Price (USD)"})}

            return figure, figure2, figure3, recommendation, style, sub_r
        
        app.run_server(debug=False) # Run the app.
