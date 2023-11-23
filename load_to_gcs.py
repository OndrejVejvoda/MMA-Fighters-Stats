import os
import pandas as pd
from google.cloud import storage
from scrape_to_csv import *

def upload_to_gcs(bucket_name, blob_name):
    # Configuration (better to move this to environment variables or a config file)
<<<<<<< HEAD
    bucket_name = 'fight_stats_data'
    blob_name = 'raw/test_raw_fighters.csv'
    service_account_key_path = r'D:\Credentials\fightstats-404410-cf30b6b920d1.json'
=======
    #bucket_name = 'fight_stats_data'
    #blob_name = 'raw/raw_fighters.csv'
    #service_account_key_path = 'fightstats-404410-cf30b6b920d1.json'
>>>>>>> ce74578af7e3352bec326710253adb361178594b

     # Get data and convert to CSV format
    fighters_data = scrape_data()  # Assuming this function returns the required data
    csv_data = fighters_data.to_csv(index=False)


    try:
        # Authenticate and initialize the client
        #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_key_path
        storage_client = storage.Client()

        # Get the bucket object and upload the data
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(csv_data, content_type='text/csv')

        print(f"File uploaded to {bucket_name}/{blob_name}")
    except Exception as e:
        print(f"Failed to upload the file: {str(e)}")

if __name__ == "__main__":
<<<<<<< HEAD
    upload_to_gcs()
=======
    bucket_name = os.getenv('BUCKET_NAME')
    blob_name = os.getenv('BLOB_NAME')
    upload_to_gcs(bucket_name, blob_name)
>>>>>>> ce74578af7e3352bec326710253adb361178594b
