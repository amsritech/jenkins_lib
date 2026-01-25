import boto3

def copy_file_in_s3(source_bucket, source_object, dest_bucket, dest_object):
    s3 = boto3.client('s3')

    copy_source = {'Bucket': source_bucket, 'Key': source_object}

    try:
        s3.copy_object(CopySource=copy_source, Bucket=dest_bucket, Key=dest_object)
        print(f"Copied '{source_object}' from '{source_bucket}' to '{dest_object}' in '{dest_bucket}'")
    except Exception as e:
        print(f"Error copying file: {e}")

# Example usage
copy_file_in_s3('source-bucket-name', 'source-file.txt', 'destination-bucket-name', 'copied-file.txt')
