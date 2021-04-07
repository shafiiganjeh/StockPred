#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

def split(A):  
    return A[:-1], A[1:]   

def Model(Hunits,Batchsize, uniq):
  model = tf.keras.Sequential([
    tf.keras.layers.LSTM(Hunits,return_sequences=False,batch_input_shape=[Batchsize, None,1],stateful=True,recurrent_initializer='glorot_uniform'),
    tf.keras.layers.Dense(uniq)
  ])
  return model


Liste = pd.read_csv("fListe.csv",index_col=False,header=None)
N=Liste.shape[1]
i=0

StockDT = pd.read_csv(Liste.iat[0, i][Liste.iat[0, i].find("=")+1:]+".csv",skip_blank_lines=False)[["Date","Volume","Open","Close"]]
Dates = StockDT["Date"]

TrainData = pd.concat([StockDT["Date"], (StockDT["Open"] - StockDT["Close"])/(StockDT["Open"]+StockDT["Close"] )], axis=1).set_index(StockDT.columns[0])
ADD=min(TrainData[0])*-1
TrainData = ((TrainData+ADD)*100).round(0)
uniques = TrainData[0].value_counts().shape[0]

workingDay=11
batchSize=4

Dset = tf.data.Dataset.from_tensor_slices(TrainData[0]).batch(workingDay+1, drop_remainder=True)
Dset = Dset.map(split)
Dset = Dset.batch(batchSize, drop_remainder=True)
#
model = Model(256,batchSize,uniques)
model.summary()

#todo
#loss function
#training the model
#adjusting parameters
#benchmarking with random walk as baseline
