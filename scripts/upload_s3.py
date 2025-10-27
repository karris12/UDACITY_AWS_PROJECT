import os
import boto3
from botocore.exceptions import ClientError

def upload_files_to_s3(folder_path, bucket_name, prefix=""):
    """
    Upload all files in a local folder to an S3 bucket, maintaining folder structure.
    
    :param folder_path: Local folder containing files to upload
    :param bucket_name: Target S3 bucket name
    :param prefix: Optional S3 folder prefix
    """
    # Initialize S3 client
    s3_client = boto3.client('s3')

    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # Walk through the folder and upload files
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            local_path = os.path.join(root, filename)
            
            # Calculate relative path for S3 key
            relative_path = os.path.relpath(local_path, folder_path)
            s3_key = os.path.join(prefix, relative_path).replace("\\", "/")

            try:
                s3_client.upload_file(local_path, bucket_name, s3_key)
                print(f"Successfully uploaded {relative_path} to s3://{bucket_name}/{s3_key}")
            except ClientError as e:
                print(f"Error uploading {relative_path}: {e}")

if __name__ == "__main__":
    # Path to the local folder containing your PDFs
    folder_path = os.path.join(os.path.dirname(__file__), "spec-sheets")
    
    # S3 bucket name from your Terraform output
    bucket_name = "bedrock-kb-635949072774"
    
    # Optional S3 prefix to maintain folder structure
    prefix = "spec-sheets"

    upload_files_to_s3(folder_path, bucket_name, prefix)
