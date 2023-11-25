from google.cloud import storage
import pandas as pd
import os
import io


def process_csv_file(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This function is triggered when a file is uploaded to the Cloud Storage bucket.
    """
    bucket_name = os.environ['BUCKET_NAME']
    raw_file_prefix = os.environ['RAW_FILE_PREFIX']
    cleaned_file_prefix = os.environ['CLEANED_FILE_PREFIX']
    expected_raw_file_name = os.environ['EXPECTED_RAW_FILE_NAME']
    
    # Initialize the client
    storage_client = storage.Client()

    # Get the bucket name and file name from the event
    event_bucket_name = data['bucket']
    event_file_name = data['name']

    if event_bucket_name == bucket_name and event_file_name == raw_file_prefix + expected_raw_file_name:
        # Access the file from GCP bucket
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(event_file_name)
        csv_data = blob.download_as_text()

        # Process the CSV data
        df = pd.read_csv(io.StringIO(csv_data))

        # Data cleaning and formatting as per your existing code
        df["height"] = df["height"].str.replace("' ",".").str.replace('"',"")
        df["weight"] = df["weight"].str.replace(" lbs.", "")
        df["reach"] = df["reach"].str.replace('"',"")

        cols = ["str_acc","str_def","td_acc","td_def"]
        for col in cols:
            df[col] = df[col].str.replace("%","")

        df["born"] = pd.to_datetime(df["born"], errors="coerce").dt.strftime("%m%d%Y")

        # Optionally, save the processed data back to the bucket or elsewhere
        # Get the bucket object

        processed_csv_data = df.to_csv(index=False)
        bucket = storage_client.get_bucket(bucket_name)

        # Specify the Blob name (this is the file name that will be saved in your bucket)
        blob = bucket.blob(cleaned_file_prefix + 'cleaned_fighters.csv')

        # Upload the CSV data
        blob.upload_from_string(processed_csv_data, content_type='text/csv')

    return 'File processed.'
