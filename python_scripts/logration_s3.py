import os
import gzip
import boto3
from datetime import datetime, timedelta

# Config
LOG_DIR = "/var/log/myapp"
S3_BUCKET = "myapp-logs"
RETENTION_DAYS = 7

s3 = boto3.client('s3')

def rotate_and_upload():
 cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)
 for fname in os.listdir(LOG_DIR):
 path = os.path.join(LOG_DIR, fname)
 if not os.path.isfile(path):
 continue
 mtime = datetime.utcfromtimestamp(os.path.getmtime(path))
 if mtime < cutoff:
 # compress
 gz_path = f"{path}.gz"
 with open(path, 'rb') as f_in, gzip.open(gz_path, 'wb') as f_out:
 f_out.writelines(f_in)
 # upload
 s3.upload_file(gz_path, S3_BUCKET, f"{fname}.gz")
 # clean up
 os.remove(path)
 os.remove(gz_path)

if __name__ == "__main__":
 rotate_and_upload()
