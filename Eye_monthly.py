#NOTE THAT THE CODE IS THE SAME FOR EACH POI, ONLY THE PARAMETERS DIFFERS BUT CAN BE FOUND IN THE REPORT. 
###############################################   import packages  ################################################
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import r2_score
import random
random.seed(10)
#########################  import data and formulate train and test length ################################## 
df = pd.read_excel('/Users/nahomtsehaie/documents/attractiesnahom.xlsx', sheet_name = 'Eye Film monthly' , )
SD = 0.8 #split data in trainingdata and testdata 
df = df[['date', 'Count']]
df.replace("", float("NaN"), inplace=True)
df = df.dropna()
train = df[['Count']]
test = df[['Count']]
trainlength = int(np.round(SD*len(df)))
train=df[0:trainlength] 
test=df[trainlength:]

#change data in proper dataframe and plot timeseries model as well the train en test length
df.Timestamp = pd.to_datetime(df.date,format='%d-%m-%Y') 
df.index = df.Timestamp 
train.Timestamp = pd.to_datetime(train.date,format='%d-%m-%Y') 
train.index = train.Timestamp 
test.Timestamp = pd.to_datetime(test.date,format='%d-%m-%Y') 
test.index = test.Timestamp 

#df.Count.plot(figsize=(15,8), title= 'Visitors Eye filmmuseum 2017-2020', fontsize=14)
plt.figure(figsize=(16,8))
train.Count.plot(label= 'Train data', fontsize=14)
test.Count.plot(label= 'Test', fontsize=14) 
plt.ylabel('amount of visitors')
plt.xlabel ('date')
plt.legend(loc='best')
plt.title("Train and Test data monthly Eye filmmuseum 2017-2020 ")
plt.show()
#######################################  NAIVE MODEL  ###################################################
# naivemodel
dd= np.asarray(train.Count)
y_hat = test.copy()
y_hat['naive'] = dd[len(dd)-1]
plt.figure(figsize=(16,8))
plt.plot(train.index, train['Count'], label='Train')
plt.plot(test.index,test['Count'], label='Test')
plt.plot(y_hat.index,y_hat['naive'], label='Naive model Forecast')
plt.legend(loc='best')
plt.ylabel('amount of visitors')
plt.xlabel ('date')
plt.title("Naive Forecast Monthly Eye Film Museum")
plt.show()

rmse_NM = sqrt(mean_squared_error(test['Count'], y_hat['naive']))
mape_NM = np.round(np.mean(np.abs(test['Count']-y_hat['naive'])/test['Count'])*100,2)
print(rmse_NM)
print(mape_NM)
#######################################  SES MODEL   ####################################################
#SES (Simple Exponential Smoothing) #0.9 is parameter 
from statsmodels.tsa.api import SimpleExpSmoothing, Holt, ExponentialSmoothing
y_hat_avg = test.copy()
fit2 = SimpleExpSmoothing(np.asarray(train['Count'])).fit(smoothing_level=0.1,optimized=False)
y_hat_avg['SES'] = fit2.forecast(len(test))
plt.figure(figsize=(16,8))
plt.plot(train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['SES'], label='SES')
plt.legend(loc='best')
plt.ylabel('amount of visitors')
plt.xlabel ('date')
plt.title("Simple Exponential Smoothing Monthly Eye Film Museum")
plt.show()

rmse_SES = sqrt(mean_squared_error(test.Count, y_hat_avg.SES))
mape_SES = np.round(np.mean(np.abs(test['Count']-y_hat_avg['SES'])/test['Count'])*100,2)
print(rmse_SES)
print(mape_SES)
#######################################  HOLT Double MODEL   ####################################################
#HLTM (Holt???s Linear Trend method)
y_hat_avg = test.copy()
fit12 = Holt(np.asarray(train['Count'])).fit(smoothing_level = 0.1,smoothing_trend = 0.5 , optimized= False)
y_hat_avg['Holt_linear'] = fit12.forecast(len(test))
plt.figure(figsize=(16,8))
plt.plot(train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['Holt_linear'], label='Holt_linear')
plt.legend(loc='best')
plt.ylabel('amount of visitors')
plt.xlabel ('date')
plt.title("Holt's Linear Trend method Monthly Eye Film Museum")
plt.show() 

rmse_HLTM = sqrt(mean_squared_error(test.Count, y_hat_avg.Holt_linear))
mape_HLTM = np.round(np.mean(np.abs(test['Count']-y_hat_avg['Holt_linear'])/test['Count'])*100,2)
print(rmse_HLTM)
print(mape_HLTM)
#######################################  HOLT Triple MODEL (HWES)   ####################################################
#HLTM (Holt???s Linear Trend method)
y_hat_avg = test.copy()
fit1 = ExponentialSmoothing(np.asarray(train['Count']) ,seasonal_periods=12 ,trend='mul', seasonal='mul',).fit()
y_hat_avg['Holt_Winter'] = fit1.forecast(len(test))
plt.figure(figsize=(16,8))
plt.plot( train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['Holt_Winter'], label='Holt_Winter')
plt.legend(loc='best')
plt.ylabel('amount of visitors')
plt.xlabel ('date')
plt.title("Holt Winter's Exponential Smoothing Monthly Eye Film Museum")
plt.show()

rmse_HWTM = sqrt(mean_squared_error(test.Count, y_hat_avg.Holt_Winter))
mape_HWTM = np.round(np.mean(np.abs(test['Count']-y_hat_avg['Holt_Winter'])/test['Count'])*100,2)
print(rmse_HWTM)
print(mape_HWTM)
################################## non stationarity check ADF & KPSS ##########################################
#non stationarity check ADF
from statsmodels.tsa.stattools import adfuller
from numpy import log
result = adfuller(df['Count'])
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])

#non stationarity check KPSS 
from statsmodels.tsa.stattools import kpss
def kpss_test(series, **kw):    
      statistic, p_value, n_lags, critical_values = kpss(series, **kw)
      # Format Output
      print(f'KPSS Statistic: {statistic}')
      print(f'p-value: {p_value}')
      print(f'num lags: {n_lags}')     
      print('Critial Values:')
      for key, value in critical_values.items():
          print(f'   {key} : {value}')
      print(f'Result: The series is {"not " if p_value < 0.05 else ""}stationary')

kpss_test(df['Count'])

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plot_acf(train['Count'])
plot_pacf(train['Count'])
#########################################   ARMA  ##################################################
##ARMA model
from statsmodels.tsa.arima.model import ARIMA
y_hat_avg = test.copy()
model = ARIMA(train['Count'], order=(5, 0, 1))
model_fit = model.fit()
#print(model_fit.summary())
y_hat_avg['ARMA'] =model_fit.forecast(len(test))

plt.figure(figsize=(16,8))
plt.plot(train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['ARMA'], label='ARMA')
plt.legend(loc='best')
plt.ylabel('amount of visitors')
plt.xlabel ('date')
plt.title("ARMA Monthly Eye Film Museum")
plt.show()

rmse_ARMA = sqrt(mean_squared_error(test.Count, y_hat_avg.ARMA))
mape_ARMA = np.round(np.mean(np.abs(test['Count']-y_hat_avg['ARMA'])/test['Count'])*100,2)
print(rmse_ARMA)
print(mape_ARMA)
######################################   ARIMA   ####################################################
#ARIMA
from statsmodels.tsa.arima.model import ARIMA
y_hat_avg = test.copy()
model = ARIMA(train['Count'], order=(5, 1, 1))
model_fit = model.fit()
#print(model_fit.summary())
y_hat_avg['ARIMA'] =model_fit.forecast(len(test))

plt.figure(figsize=(16,8))
plt.plot( train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['ARIMA'], label='ARIMA')
plt.legend(loc='best')
plt.ylabel('amount of visitors')
plt.xlabel ('date')
plt.title("ARIMA Monthly Eye Film Museum")
plt.show()

rmse_ARIMA = sqrt(mean_squared_error(test.Count, y_hat_avg.ARIMA))
mape_ARIMA = np.round(np.mean(np.abs(test['Count']-y_hat_avg['ARIMA'])/test['Count'])*100,2)
print(rmse_ARIMA)
print(mape_ARIMA)

######################################   SARIMA  ##################################################
#SARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
y_hat_avg = test.copy()
model = SARIMAX(train['Count'], order=(5, 0, 1), seasonal_order=(7,0,1,12))
model_fit = model.fit(disp=False)
#print(model_fit.summary())
y_hat_avg['SARIMA'] = model_fit.forecast(len(test))

plt.figure(figsize=(16,8))
plt.plot( train['Count'], label='Train')
plt.plot(test['Count'], label='Test')
plt.plot(y_hat_avg['SARIMA'], label='SARIMA')
plt.legend(loc='best')
plt.ylabel('amount of visitors')
plt.xlabel ('date')
plt.title("SARIMA Monthly Eye Film Museum")
plt.show()

rmse_SARIMA = sqrt(mean_squared_error(test.Count, y_hat_avg.SARIMA))
mape_SARIMA = np.round(np.mean(np.abs(test['Count']-y_hat_avg['SARIMA'])/test['Count'])*100,2)
print(rmse_SARIMA)
print(mape_SARIMA)

######################################  AUTO ARIMA #####################################################
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm

model = pm.auto_arima(train['Count'], start_p=0, start_q=0,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=6, max_q=6, # maximum p and q
                      m=4,              # frequency of series
                      d=0,           # let model determine 'd'
                      seasonal=True,   # Seasonality
                      start_P=1, 
                      D=0, 
                      start_Q = 1,
                      max_Q = 6,
                      max_P = 6,
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)
print(model.summary())
########################################  Neural Network #######################################################################
#reshape input and outout   
def training_data(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)        
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)
time_steps = 4 #make prediction on the past months. This generates including lag differences. 
train = train[['Count']]
test = test[['Count']]
# reshape to [samples, time_steps, n_features]
X_train, y_train = training_data(train, train.Count, time_steps)
x_test, y_test = training_data(test, test.Count, time_steps)
print(X_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)
##########################################  LSTM model defined #########################################################
#vanilla lstm  (= Create LSTMs with 1 layer and input is units hidden neurons)
def model_vLSTM(units):
    model = keras.Sequential()
    #input
    model.add(keras.layers.LSTM(
        units=units,
        activation="relu",
        input_shape=(X_train.shape[1], X_train.shape[2])
        ))
    model.add(keras.layers.Dropout(0.2))  #dropout to prevent overfitting 
    model.add(keras.layers.Dense(1))
    model.compile(loss='mse', optimizer='adam')
    return model
###################################   Train network & Prediction #########################################
#train network 
def fit_model(model):
    early_stop = keras.callbacks.EarlyStopping(
        monitor = 'val_loss',
        min_delta = 0.0,
        patience = 10)
    history = model.fit(
        X_train, y_train, 
        epochs =1000, # number of complete passes through the training dataset.
        validation_split = 0.1,  #data amount for validation
        batch_size = 3, #number of samples taken for each training. 
        shuffle = False,  #order sequence is important
        callbacks = [early_stop])
    return history
  
def prediction(model, x_test, y_test):
    y_pred = model.predict(x_test)
    y_train_inv = y_train.reshape(1, -1)
    y_test_inv = y_test.reshape(1, -1)
    y_pred_inv = y_pred
    return y_pred, y_pred_inv, y_train_inv, y_test_inv  
##################################   plot loss & forecast & test vs prediction   ################################
def plot_loss (history, model_name):
    plt.figure(figsize = (8, 4))
    plt.plot(history.history['loss'], color = 'blue', label='Train Loss')
    plt.plot(history.history['val_loss'], color = 'red', label='Validation Loss')
    plt.title('Train vs. Validation Loss for ' + model_name)
    plt.ylabel('Loss')
    plt.xlabel('epoch')
    plt.legend(loc='upper right')
    plt.show()

def plot_forecast(prediction_model, y_test, model_name):
    y_pred, y_pred_inv, y_train_inv, y_test_inv = prediction_model
    plt.plot(np.arange(0, len(y_train)), y_train_inv.flatten(), 'g', label="history")
    plt.plot(np.arange(len(y_train), len(y_train) + len(y_test)), y_test_inv.flatten(), marker='.', label="Test data")
    plt.plot(np.arange(len(y_train), len(y_train) + len(y_test)), y_pred_inv.flatten(), 'r', label="Prediction "+model_name)
    plt.ylabel('Amount of Visitors')
    plt.xlabel('Time Step per month')
    plt.title('Forecast for '+ model_name)
    plt.legend()
    plt.show();

def plot_compare(prediction_model ,y_test, model_name):    
    y_pred, y_pred_inv, y_train_inv, y_test_inv = prediction_model
    plt.plot(y_test_inv.flatten(), marker='.', label="Test data")
    plt.plot(y_pred_inv.flatten(), 'r', label="Prediction "+model_name)
    plt.ylabel('Amount of Visitors')
    plt.xlabel('Time Step per week')
    plt.title('Test data vs Prediction data for '+model_name)
    plt.legend()
    plt.show(); 

def evaluate_performance(prediction_model, y_test, model_name):
    y_pred, y_pred_inv, y_train_inv, y_test_inv = prediction_model
    y_test_inv = y_test_inv.reshape(-1,1)
    errors = y_pred_inv - y_test_inv
    
    mape = round(np.abs(errors/y_test_inv).mean()*100,2)
    mse = round(np.square(errors).mean(),2)
    rmse = round(np.sqrt(mse),2)
    r_sq = round(r2_score(y_test, y_pred),2)
    
    print('Performance of '+model_name+ ':')
    print('MAPE:\t', mape)
    print('RMSE:\t', rmse)
    print('R^2:\t', r_sq)
    return mape, mse, rmse, r_sq

############# Generating en Train model  en forceast en plot en evaluate  #########################################
#generate model    
vLSTM_n4 = model_vLSTM(4)
history_vLSTM_n4 = fit_model(vLSTM_n4)
prediction_vLSTM_n4 = prediction(vLSTM_n4, x_test, y_test)
plot_loss(history_vLSTM_n4, 'vLSTM_n4')
plot_forecast(prediction_vLSTM_n4, y_test, 'vLSTM_n4')
plot_compare(prediction_vLSTM_n4, y_test, 'vLSTM_n4')
evaluate_performance(prediction_vLSTM_n4, y_test, 'vLSTM_n4')

vLSTM_n8 = model_vLSTM(8)
history_vLSTM_n8 = fit_model(vLSTM_n8)
prediction_vLSTM_n8 = prediction(vLSTM_n8, x_test, y_test)
plot_loss(history_vLSTM_n8, 'vLSTM_n8')
plot_forecast(prediction_vLSTM_n8, y_test, 'vLSTM_n8')
plot_compare(prediction_vLSTM_n8, y_test, 'vLSTM_n8')
evaluate_performance(prediction_vLSTM_n8, y_test, 'vLSTM_n8')

vLSTM_n16 = model_vLSTM(16)
history_vLSTM_n16 = fit_model(vLSTM_n16)
prediction_vLSTM_n16 = prediction(vLSTM_n16, x_test, y_test)
plot_loss(history_vLSTM_n16, 'vLSTM_n16')
plot_forecast(prediction_vLSTM_n16, y_test, 'vLSTM_n16')
plot_compare(prediction_vLSTM_n16, y_test, 'vLSTM_n16')
evaluate_performance(prediction_vLSTM_n16, y_test, 'vLSTM_n16')

vLSTM_n32 = model_vLSTM(32)
history_vLSTM_n32 = fit_model(vLSTM_n32)
prediction_vLSTM_n32 = prediction(vLSTM_n32, x_test, y_test)
plot_loss(history_vLSTM_n32, 'vLSTM_n32')
plot_forecast(prediction_vLSTM_n32, y_test, 'vLSTM_n32')
plot_compare(prediction_vLSTM_n32, y_test, 'vLSTM_n32')
evaluate_performance(prediction_vLSTM_n32, y_test, 'vLSTM_n32')

vLSTM_n64 = model_vLSTM(64)
history_vLSTM_n64 = fit_model(vLSTM_n64)
prediction_vLSTM_n64 = prediction(vLSTM_n64, x_test, y_test)
plot_loss(history_vLSTM_n64, 'vLSTM_n64')
plot_forecast(prediction_vLSTM_n64, y_test, 'vLSTM_n64')
plot_compare(prediction_vLSTM_n64, y_test, 'vLSTM_n64')
evaluate_performance(prediction_vLSTM_n64, y_test, 'vLSTM_n64')
#######################################################  END #################################################################
