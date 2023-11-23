import os
import pandas as pd
from google.cloud import storage
from scrape_to_csv import *

def upload_to_gcs(bucket_name, blob_name,GCP_KEY):
    # Get data and convert to CSV format
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_KEY
    fighters_data = scrape_data()  # Assuming this function returns the required data
    csv_data = fighters_data.to_csv(index=False)
    
    try:
        storage_client = storage.Client()
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
    SERVICE_ACCOUNT_KEY_PATH =  os.getenv('GCP_SA_KEY')
    upload_to_gcs(bucket_name, blob_name,SERVICE_ACCOUNT_KEY_PATH)
