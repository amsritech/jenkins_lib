import boto3
from datetime import datetime, timedelta

def delete_old_files(bucket_name, days_threshold):
    s3 = boto3.client('s3')
    threshold_time = datetime.now() - timedelta(days=days_threshold)

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in response:
            for obj in response['Contents']:
                last_modified = obj['LastModified']
                if last_modified < threshold_time:
                    s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                    print(f"Deleted {obj['Key']} (Last Modified: {last_modified})")
                else:
                    print(f"Keeping {obj['Key']} (Last Modified: {last_modified})")
        else:
            print("No objects found in the bucket.")
    except Exception as e:
        print(f"Error deleting old files: {e}")

# Example usage
delete_old_files('your-bucket-name', 30)  # Deletes files older than 30 days
