# StockPred 
Since dealing with LSTM networks I have noticed many example scripts trying to predict stock prices using a LSTM model.
A lot of these models seem to work perfectly on price predictions which gives a wrong idea about the usefulness of these models.
Predicting prices itself is already very problematic, but most of these examples lack any sort of real performance benchmark, that is, can they for example beat a naive forecast using a random walk Hypothesis.

In this script I will try out the performance of an LSTM neural network model on the stock market using cryptocurrencies as a target while trying to avoid most of the problems I have come across in other scripts.
Firstly, we are not going to predict prices, but sort of a generalized trend of the price change, this also allows us to use multiple different stocks 
that highly correlate as training data instead of using data from a single stock.
We will benchmark the performance of the model not by how well we predict the stock price, but by how much money we would have made (or lost) by using the model on actual test data.

