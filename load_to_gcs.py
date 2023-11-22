import os
import pandas as pd
from google.cloud import storage
from scrape_to_csv import *

def upload_to_gcs():
    # Configuration (better to move this to environment variables or a config file)
    bucket_name = 'fight_stats_data'
    blob_name = 'raw/raw_fighters.csv'
    service_account_key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

     # Get data and convert to CSV format
    fighters_data = scrape_data()  # Assuming this function returns the required data
    csv_data = fighters_data.to_csv(index=False)
    
    try:
        # Authenticate and initialize the client
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_key_path
        storage_client = storage.Client()
        
        storage_client.list_buckets()
        # Get the bucket object and upload the data
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(csv_data, content_type='text/csv')

        print(f"File uploaded to {bucket_name}/{blob_name}")
    except Exception as e:
        print(f"Failed to upload the file: {str(e)}")

if __name__ == "__main__":
    bucket_name = os.getenv('BUCKET_NAME')
    blob_name = os.getenv('BLOB_NAME')
    upload_to_gcs()
