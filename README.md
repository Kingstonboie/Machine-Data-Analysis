# Machine-Data-Analysis
This project is focused on monitoring and analysing machine data in real-time using a webbased dashboard application. It leverages the Dash framework to visualize time series data
from various machines, enabling users to monitor parameters like temperature and
pressure. The project also integrates machine learning models, specifically LSTM (Long
Short-Term Memory) networks, for anomaly detection in time series data. By combining
real-time data processing with predictive analytics, this dashboard provides a robust tool for
maintaining machine efficiency and pre-emptively identifying potential issues.

The project is organized into several key components:

• Sample Data Generator (addmachines.py): For testing and demonstration purposes,
this script generates synthetic machine data. It populates the database with
randomized values for parameters like temperature and pressure, simulating the kind
of data that would be collected from real machines.

• Database to CSV Exporter (sqltocsv.py): This script connects to a MySQL database to
retrieve raw machine data and machine details, exporting them into CSV files. These
files are then used as input for the data preparation process. It ensures that the most
up-to-date data is available for analysis.

• Data Preparation (dataprep.py): This script is responsible for loading raw machine
data from CSV files and preparing it for analysis. It extracts unique parameters from
the dataset, normalizes the data, and trains an LSTM model for each parameter. The
trained models are then saved for future use in anomaly detection.

• Dashboard Application (dash_app.py): This is the core script that runs the web
application using the Dash framework. It loads the pre-trained models and processed
data, allowing users to select a machine and view interactive line charts of different
parameters. The app also highlights anomalies detected by the LSTM models, making
it easy to identify unusual patterns in the data.