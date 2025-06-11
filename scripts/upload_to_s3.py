import boto3
import os

s3 = boto3.client('s3')

def upload_file(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)
    s3.upload_file(file_path, bucket_name, object_name)

# Example usage:
upload_file('data/ecommerce_customers.csv', 'ecommercesalesdata9', 'customers/ecommerce_customers.csv')
