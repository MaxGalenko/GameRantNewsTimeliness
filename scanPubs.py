import pandas as pd
import os
import json
from datetime import datetime
import pytz

# Read the Excel file into a pandas DataFrame
# Get the current working directory
current_directory = os.getcwd()

# Construct the full path to the Excel file
file_path = os.path.join(current_directory, "Gamerant_Mini_Challenge_Data.xlsx")

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(file_path)

# Convert the DataFrame to JSON with datetime values as strings
json_data = df.to_json(orient="records", date_format="iso")  # date_format="iso" keeps datetime values as strings

json_object = json.loads(json_data)

for x in json_object:
    article_title = x['These Are the Titles That You Will Have to Match with the first announcement']
    article_url = x['permalink']
    article_datetime_utc = x['articleDateOriginalPublished']

    # Define the datetime string in UTC
    datetime_str = article_datetime_utc

    # Parse the datetime string into a datetime object
    datetime_obj_utc = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f')

    # Convert the datetime object to the Eastern Time Zone (EST)
    eastern = pytz.timezone('US/Eastern')
    datetime_obj_est = datetime_obj_utc.replace(tzinfo=pytz.utc).astimezone(eastern)

    # Format the datetime object as a string in EST
    article_datetime = datetime_obj_est.strftime('%m-%d-%Y %H:%M:%S.%f')

    article = {
        "title": article_title,
        "url": article_url,
        "datetime": article_datetime
    }

    # now we send article to be processed into the db



