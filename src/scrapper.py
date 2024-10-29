import os
import pandas as pd
from sodapy import Socrata
from sqlalchemy import create_engine


# Limit of data to be loaded
LIMIT = 2000
url = "data.sfgov.org"
resource = "wr8u-xric"
OUTPUT_DIR = "/usr/src/app/data"
DB_FILE_NAME = "fire_incidents.db"
DB_NAME = 'fire_incidents'


def main(output_dir):
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata(url, None)

    if client:
        # Save data to a dataframe
        results = client.get(resource, limit=LIMIT)
        data = pd.DataFrame.from_records(results)

        # Connection string pointing to the output directory
        database_file_path = os.path.join(output_dir, DB_FILE_NAME)
        engine = create_engine(f'sqlite:///{database_file_path}')

        data = add_lat_long(data)
        data = fix_data_types(data)

        # Save the dataframe to an SQL table named 'fire_incidents'
        data.to_sql(DB_NAME, con=engine, if_exists='replace', index=False)
        print("Data saved to SQL database.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

def output_dir():
    # Directory to save the database
    output_dir = os.environ.get("OUTPUT_DIR", OUTPUT_DIR)

    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)

    return output_dir

def add_lat_long(data):
    data['latitude'] = data['point'].apply(lambda x: x['coordinates'][0] if isinstance(x, dict) else None)
    data['longitude'] = data['point'].apply(lambda x: x['coordinates'][1] if isinstance(x, dict) else None)

    return data.drop(columns=['point'])

def fix_data_types(data):
    datetime_columns = ['incident_date', 'alarm_dttm', 'arrival_dttm', 'close_dttm']
    number_columns = ['incident_number', 'suppression_personnel', 'ems_units',
                      'ems_personnel', 'other_units', 'other_personnel',
                      'estimated_property_loss', 'estimated_contents_loss',
                      'fire_fatalities', 'fire_injuries', 'civilian_fatalities',
                      'civilian_injuries', 'number_of_alarms',
                      'floor_of_fire_origin', 'number_of_sprinkler_heads_operating']

    for col in datetime_columns:
        data[col] = pd.to_datetime(data[col])

    for col in number_columns:
        data[col] = pd.to_numeric(data[col])

    return data


if __name__ == "__main__":
    main(output_dir())
