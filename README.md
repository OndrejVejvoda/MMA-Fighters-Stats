# UFC Fighter Statistics Project
![DALL·E 2023-12-01 15 13 08 - A modern and minimalistic illustration for a project on MMA fighters and sports analysis, featuring an animated style MMA fighter silhouette in a boxi (Small)](https://github.com/OndrejVejvoda/MMA-Fighters-Stats/assets/49439520/2b0111d6-fe12-4ee4-9576-f3c0b6065969)
## Description

This project is designed to automate the process of scraping, processing, and managing UFC fighter statistics data. It consists of several interconnected components that work together to ensure the data is not only regularly updated but also cleaned and stored efficiently in Google Cloud Storage. The project's workflow is as follows:

**Data Scraping:** A Python script (scrape_to_csv.py) scrapes UFC fighter statistics from a specified website. This script is scheduled to run weekly via GitHub Actions, ensuring that the data is consistently up-to-date.

**Initial Storage:** Once the data is scraped, it's converted into a CSV format and initially uploaded to a specified Google Cloud Storage bucket. This raw data serves as the basis for further processing.

**Data Cleaning with Google Cloud Function:** After the initial upload, a Google Cloud Function is triggered. This function is responsible for cleaning the data. It performs tasks such as removing duplicates, handling missing values, and any other data sanitization required to ensure data quality.

**Re-uploading Cleaned Data:** Post-cleaning, the processed data is then uploaded back to Google Cloud Storage, either replacing the original raw data file or as a new, cleaned data file. This ensures that downstream applications and services always have access to the latest, cleanest data.

**Automated Workflow with GitHub Actions:** The entire process, from scraping to the re-uploading of cleaned data, is automated using GitHub Actions. This setup provides a hands-off approach to data management, significantly reducing manual effort and the potential for human error.

## Features

- Data scraping of UFC fighter statistics.
- Data conversion to CSV format.
- Automated data upload to Google Cloud Storage.
- Weekly data updates using GitHub Actions.

## Prerequisites

- Python 3.x
- Google Cloud account with an active project and storage bucket.
- Service account in Google Cloud with permissions to access the storage bucket.


