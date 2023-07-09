import logging
import time

import boto3 as boto3
from botocore.exceptions import ClientError


class AwsS3Service:

    def __init__(self) -> None:
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client('s3')

    def create_bucket(self, bucket_name, region=None):
        try:
            if region is None:
                self.s3_resource.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3_resource.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

        except ClientError as e:
            print(e)
            logging.error(e)
            return False

        return True

    def print_content(self, region_name=None):
        bucket_names = []
        if region_name:
            for bucket in self.s3_client.list_buckets()["Buckets"]:
                if self.s3_client.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'] == region_name:
                    bucket_names.append(bucket["Name"])
        else:
            for bucket in self.s3_client.list_buckets()["Buckets"]:
                bucket_names.append(bucket["Name"])
        return bucket_names

    def get_all_keys_in_bucket(self, bucket_name):
        result = []
        objects_metadata = self.s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in objects_metadata:
            for key in objects_metadata['Contents']:
                result.append(key['Key'])
        return result

    def download_file(self, bucket_name, file_name):
        try:
            return self.get_object(self.get_total_bytes(bucket_name, file_name), bucket_name, file_name)

        except ClientError as e:
            print(e)
            logging.error(e)
            return 0

    def get_total_bytes(self, bucket_name, item_name):
        result = self.s3_client.list_objects(Bucket=bucket_name)
        for item in result['Contents']:
            if item['Key'] == item_name:
                return item['Size']

    def get_object_range(self, total_bytes, bucket_name, item_name):
        offset = 0
        while total_bytes > 0:
            end = offset + 999999 if total_bytes > 1000000 else ""
            total_bytes -= 1000000
            byte_range = 'bytes={offset}-{end}'.format(offset=offset, end=end)
            offset = end + 1 if not isinstance(end, str) else None
            yield self.s3_client.get_object(Bucket=bucket_name, Key=item_name, Range=byte_range)['Body'].read()

    def get_object(self, total_bytes, bucket_name, item_name):
        if total_bytes > 1000000:
            return self.get_object_range(total_bytes, bucket_name, item_name)
        return self.s3_client.get_object(Bucket=bucket_name, Key=item_name)['Body'].read()

    def delete_file(self, bucket_name, file_name):
        try:
            self.s3_resource.Object(bucket_name, file_name).delete()

        except ClientError as e:
            print(e)
            logging.error(e)
            return False

        return True

    def upload_file(self, bucket_name, file_path, file_name):
        try:
            data = open(file_path, 'rb')
            start = time.time()
            self.s3_resource.Bucket(bucket_name).put_object(Key=file_name, Body=data)
            end = time.time()

        except ClientError as e:
            print(e)
            logging.error(e)
            return 0

        return end - start

    def upload_file_object(self, file, bucket_name, acl="public-read"):
        try:
            self.s3_client.upload_fileobj(
                file,
                bucket_name,
                file.filename,
                ExtraArgs={
                    "ACL": acl,
                    "ContentType": file.content_type
                }
            )

        except Exception as e:
            logging.error("Something Happened: ", e)
            return ""

        return "{}{}".format('http://{}.s3.amazonaws.com/'.format(bucket_name), file.filename)

