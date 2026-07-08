from datetime import datetime
import boto3

s3 = boto3.client('s3')

bucket = "alireza-data-pipeline-123-271504343399-eu-north-1-an"
file_name = "data/users_cleaned.csv"

now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")

s3_key = f"processed/year={year}/month={month}/users_cleaned.csv"

s3.upload_file(file_name, bucket, s3_key)

print(f"Uploaded to {s3_key}")