import boto3
from moto import mock_aws

BUCKET_NAME = "crawling"


class _S3:
    @mock_aws()
    def __init__(self):
        super().__init__()
        self.s3_client = boto3.client("s3", region_name="us-east-1")

    @mock_aws()
    def upload_file(self, file_name: str, file: bytes) -> None:
        self.s3_client.create_bucket(Bucket=BUCKET_NAME)
        self.s3_client.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file)

    # def list_files(self, limit=100) -> list[str]:
    #     objects = self.s3_client.list_objects_v2(Bucket=BUCKET_NAME, MaxKeys=limit)
    #     return [f['Key'] for f in objects['Contents']]


S3 = _S3()
