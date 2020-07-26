from LSTM_CNN import construct_lstm_cnn
from StockDataGenerator import StockDataGenerator
from ProcessData import get_indicators

from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import TensorBoard

import numpy as np
import pandas as pd

import time, datetime

# import tensorflow
# if tensorflow.test.gpu_device_name():
#     print('Default GPU Device: {}'.format(tensorflow.test.gpu_device_name()))
# else:
#     print("Please install GPU version of TF")
#  
# exit()

model = construct_lstm_cnn(5, 30, single_output=True)

checkpoint = ModelCheckpoint("LSTM_CNN.h5", monitor="val_loss", save_best_only=True)
early_stopping = EarlyStopping(monitor="val_loss")
tensorboard = TensorBoard("logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

chart_indicators = ["bbands", "macd"]
ts_indicators = ["price_logreturn", "volume_logreturn"]

df = pd.read_csv("StockData/SPY.csv")
df.columns = [column.lower() for column in df.columns]
df = df.iloc[::-1]
df.reset_index(inplace=True, drop=True)
df = get_indicators(df, (chart_indicators + ts_indicators))

# print(df)

test = len(df) - np.ceil(0.2*len(df))

dfTrain = df.loc[0:test].copy()
dfTrain.reset_index(inplace=True, drop=True)
dfValid = df.loc[test:len(df)].copy()
dfValid.reset_index(inplace=True, drop=True)

# print(dfTrain)
# print(dfValid)

datagen_train = StockDataGenerator(dfTrain, "SPY", chart_indicators, ts_indicators, 5, 30, 128, single_output=True)
datagen_valid = StockDataGenerator(dfValid, "SPY", chart_indicators, ts_indicators, 5, 30, 128, single_output=True)

model.fit_generator(datagen_train, steps_per_epoch=len(datagen_train), epochs=1, validation_data=datagen_valid, callbacks=[checkpoint, tensorboard])

print("this is dfValid")
print(dfValid)

y_pred1 = model.predict_generator(datagen_valid)
print("this is prediction generator")
print(y_pred1)
print(len(y_pred1))
print(len(y_pred1[0]))

y_pred2 = model.evaluate_generator(datagen_valid)
print("this is evaluate generate")
print(y_pred2)
print(len(y_pred2))
print(len(y_pred2[0]))