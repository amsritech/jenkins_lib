import os
import gzip
import logging
from datetime import datetime, timedelta

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

# -------------------- Config --------------------
LOG_DIR = os.getenv("LOG_DIR", "/var/log/myapp")
S3_BUCKET = os.getenv("S3_BUCKET", "myapp-logs")
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", "7"))
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# S3 client with retries
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    config=Config(
        retries={"max_attempts": 5, "mode": "standard"},
        connect_timeout=5,
        read_timeout=60
    )
)

# -------------------- Helpers --------------------
def file_is_eligible(path, cutoff):
    try:
        mtime = datetime.utcfromtimestamp(os.path.getmtime(path))
        return mtime < cutoff
    except Exception as e:
        logger.error(f"Failed to get mtime for {path}: {e}")
        return False


def compress_file(src_path, dest_path):
    try:
        with open(src_path, "rb") as f_in, gzip.open(dest_path, "wb") as f_out:
            while True:
                chunk = f_in.read(1024 * 1024)  # 1MB chunks
                if not chunk:
                    break
                f_out.write(chunk)
        return True
    except Exception as e:
        logger.error(f"Compression failed for {src_path}: {e}")
        return False


def upload_to_s3(file_path, s3_key):
    try:
        s3.upload_file(file_path, S3_BUCKET, s3_key)
        logger.info(f"Uploaded to s3://{S3_BUCKET}/{s3_key}")
        return True
    except (BotoCoreError, ClientError) as e:
        logger.error(f"S3 upload failed for {file_path}: {e}")
        return False


# -------------------- Main Logic --------------------
def rotate_and_upload():
    if not os.path.exists(LOG_DIR):
        logger.error(f"Log directory does not exist: {LOG_DIR}")
        return

    cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)

    for fname in os.listdir(LOG_DIR):
        path = os.path.join(LOG_DIR, fname)

        if not os.path.isfile(path):
            continue

        if not file_is_eligible(path, cutoff):
            continue

        gz_path = f"{path}.gz"
        s3_key = f"logs/{datetime.utcnow().strftime('%Y/%m/%d')}/{fname}.gz"

        logger.info(f"Processing file: {path}")

        # Compress
        if not compress_file(path, gz_path):
            continue

        # Upload
        if not upload_to_s3(gz_path, s3_key):
            logger.warning(f"Skipping delete due to upload failure: {path}")
            continue

        # Cleanup only after successful upload
        try:
            os.remove(path)
            os.remove(gz_path)
            logger.info(f"Deleted local files: {path}, {gz_path}")
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")


# -------------------- Entry --------------------
if __name__ == "__main__":
    try:
        rotate_and_upload()
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        raise