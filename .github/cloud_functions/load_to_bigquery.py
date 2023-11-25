import os
from google.cloud import bigquery
from google.cloud import storage

def load_csv_to_bigquery(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This function loads a CSV file from the bucket to BigQuery.

    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """

    bucket_name = os.environ['BUCKET_NAME']
    cleaned_file_prefix = os.environ['CLEANED_FILE_PREFIX']
    expected_cleaned_file_name = os.environ['EXPECTED_CLEANED_FILE_NAME']
    dataset_id = os.environ['DATASET_ID']
    table_id = os.environ['TABLE_ID']

    event_bucket_name = data['bucket']
    event_file_name = data['name']

    if event_bucket_name == bucket_name and event_file_name == cleaned_file_prefix + expected_cleaned_file_name:
      client = bigquery.Client()

      dataset_id = dataset_id  
      table_id = table_id      
      dataset_ref = client.dataset(dataset_id)
      table_ref = dataset_ref.table(table_id)

      job_config = bigquery.LoadJobConfig()
      job_config.source_format = bigquery.SourceFormat.CSV
      job_config.autodetect = True  # Automatically infer schema

      uri = f'gs://{bucket_name}/{cleaned_file_prefix + expected_cleaned_file_name}'

      load_job = client.load_table_from_uri(
          uri, table_ref, job_config=job_config
      )  

      print(f'Starting job {load_job.job_id}')
      load_job.result()  # Waits for the job to complete
      print(f'Job finished.')

      destination_table = client.get_table(table_ref)
      print(f'Loaded {destination_table.num_rows} rows.')