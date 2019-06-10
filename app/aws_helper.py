import boto3
import botocore

from config import S3_KEY, S3_SECRET, S3_BUCKET

s3 = boto3.client(
    service_name="s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def upload_file_to_s3(file, bucket_name=S3_BUCKET, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type,
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e

    return build_s3_url(file.filename, bucket_name)


def build_s3_url(filename, bucket_name=S3_BUCKET):
    return "https://{}.s3.amazonaws.com/{}".format(bucket_name, filename)
