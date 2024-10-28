import os
import requests
import pandas as pd
from sqlalchemy import create_engine

# URL to the data
url = "https://data.sfgov.org/resource/wr8u-xric.csv"

# Directory to save the database
output_dir = os.environ.get("OUTPUT_DIR", "/usr/src/app/data")

# Ensure directory exists
os.makedirs(output_dir, exist_ok=True)

# Send a GET request to fetch the data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Save data to a dataframe
    data = pd.read_csv(url, parse_dates=['incident_date', 'alarm_dttm',
                                         'arrival_dttm', 'close_dttm'])
    
    # Print the first few rows of the dataframe
    print(data.head())
    
    # Connection string pointing to the output directory
    database_file_path = os.path.join(output_dir, "fire_incidents.db")
    engine = create_engine(f'sqlite:///{database_file_path}')

    # Save the dataframe to an SQL table named 'fire_incidents'
    data.to_sql('fire_incidents', con=engine, if_exists='replace', index=False)
    print("Data saved to SQL database.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
