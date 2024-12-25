from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import numpy as np
import pickle
from sklearn.metrics import mean_squared_error
# Load the pre-trained models and data
with open('models.pkl', 'rb') as f:
 models = pickle.load(f)
machine_details_df = pd.read_pickle('machine_details.pkl')
machine_data_df = pd.read_pickle('machine_data.pkl')
# Extract unique parameters and machines
unique_params = machine_data_df['param_name'].unique()
machines = machine_details_df['machine_id'].unique()
# Initialize the app
app = Dash(__name__)
# App layout
app.layout = html.Div([
 html.Div(children='Machine Data Analysis App'),
 html.Hr(),
 dcc.Dropdown(options=[{'label': machine, 'value': machine} for machine in machines], value=machines[0], id='machine-dropdown'),
 dash_table.DataTable(data=machine_details_df.to_dict('records'), page_size=6),
 html.Div(id='graphs-container') # Container for dynamically created graphs
])
# Add controls to build the interaction
@callback(
 Output(component_id='graphs-container', component_property='children'),
 Input(component_id='machine-dropdown', component_property='value')
)
def update_graphs(selected_machine):
 # Filter data for the selected machine
 filtered_df = machine_data_df[machine_data_df['machine_id'] == selected_machine]
 def create_dataset(data, time_step=1):
 X, Y = [], []
 for i in range(len(data) - time_step - 1):
 a = data[i:(i + time_step)]
 X.append(a)
 Y.append(data[i + time_step])
 return np.array(X), np.array(Y)
 def detect_anomalies(values, model, mean, std):
 values_norm = (values - mean) / std
 X, _ = create_dataset(values_norm, 10)
13
 X = X.reshape(X.shape[0], X.shape[1], 1)
 predict = model.predict(X) * std + mean
 rmse = np.sqrt(mean_squared_error(values[10:10+len(predict)], predict, multioutput='raw_values'))
 threshold = np.mean(rmse) + 2 * np.std(rmse)
 anomalies = np.abs(values[10:10+len(predict)] - predict.flatten()) > threshold
 return predict, anomalies
 graphs = []
 for param in unique_params:
 param_df = filtered_df[filtered_df['param_name'] == param]
 param_values = param_df['param_value'].values
 param_predict, param_anomalies = detect_anomalies(param_values, models[param][0], models[param][1], models[param][2])
 param_fig = px.line(param_df, x='update_ts', y='param_value', title=f'{param.capitalize()} for {selected_machine}',
 labels={'param_value': param.capitalize(), 'update_ts': 'Timestamp'})
 param_anomalous_indices = np.where(param_anomalies)[0]
 param_anomalous_timestamps = param_df['update_ts'].iloc[10:10+len(param_predict)].iloc[param_anomalous_indices]
 param_anomalous_values = param_values[10:10+len(param_predict)][param_anomalous_indices]
 param_fig.add_scatter(x=param_anomalous_timestamps, y=param_anomalous_values, mode='markers', marker=dict(color='red'),
name='Anomalies')
 param_fig.add_scatter(x=param_df['update_ts'].iloc[10:10+len(param_predict)], y=param_predict.flatten(), mode='lines',
 line=dict(color='green', dash='dash'), name='Predicted')
 graphs.append(dcc.Graph(figure=param_fig))
 return graphs
# Run the app
if __name__ == '__main__':
 app.run(debug=True)