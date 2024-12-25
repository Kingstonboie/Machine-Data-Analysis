import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
# Load the data from the CSV files
machine_details_df = pd.read_csv('ogmachine_details.csv')
machine_data_df = pd.read_csv('ogmachine_data.csv')
# Extract unique parameters
unique_params = machine_data_df['param_name'].unique()
# Normalize data and train LSTM model
def create_dataset(data, time_step=1):
 X, Y = [], []
 for i in range(len(data) - time_step - 1):
 a = data[i:(i + time_step)]
 X.append(a)
 Y.append(data[i + time_step])
 return np.array(X), np.array(Y)
def train_lstm_model(data, param_name):
 time_series = data[data['param_name'] == param_name]['param_value'].values
 mean = np.mean(time_series)
 std = np.std(time_series)
 time_series = (time_series - mean) / std
 time_step = 10
 X, Y = create_dataset(time_series, time_step)
 X = X.reshape(X.shape[0], X.shape[1], 1)
 model = Sequential()
 model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
 model.add(LSTM(50, return_sequences=False))
 model.add(Dense(1))
 model.compile(optimizer='adam', loss='mean_squared_error')
 model.fit(X, Y, epochs=100, batch_size=64, validation_split=0.2, verbose=1)
 return model, mean, std
# Train models for each parameter
models = {}
for param in unique_params:
 models[param] = train_lstm_model(machine_data_df, param)
# Save the models and parameters
with open('models.pkl', 'wb') as f:
 pickle.dump(models, f)
machine_details_df.to_pickle('machine_details.pkl')
machine_data_df.to_pickle('machine_data.pkl')
