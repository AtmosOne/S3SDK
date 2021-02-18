import time
import boto3
import logging


class SDKdecorators:
    """
        Decorators used to provide information about SDK state
    """
    @staticmethod
    def check_error(func):
        """
            Decorator to show errors if such present
            at execution bucket/object functionality.
        """
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as exc:
                logging.error(exc)
                return
        return inner

    @staticmethod
    def measure_time(func):
        def inner1(*args, **kwargs):
            begin = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            logging.info(f"Time taken: {end-begin}")
            return result
        return inner1


class S3SDK:
    """
        Module for working with S3 bucket

        * s3 (boto3): Public static s3 object
    """
    def __init__(self, bucket_name, credentials={}, region_name=None):
        self.credentials = credentials
        if region_name is not None:
            credentials['region_name'] = region_name
        self.region_name = region_name
        self.s3 = S3SDK.init_s3_resource(credentials)
        self.bucket_name = bucket_name

    @staticmethod
    @SDKdecorators.check_error
    def init_s3_resource(credentials):
        try:
            if len(list(credentials.keys())) > 0:
                if 'aws_secret_access_key' in credentials and \
                   'aws_access_key_id' in credentials:
                    return boto3.resource('s3', **credentials)
                else:
                    logging.error("Please, provide all credentials")
                    raise ValueError("Incomplete credentials")
            else:
                return boto3.resource('s3')
        except Exception as exc:
            logging.error(exc)

    @SDKdecorators.check_error
    def create_bucket(self):
        """
            Create an S3 bucket in a specified region

            If a region is not specified, the bucket is
            created in the S3 default region (us-east-1).

            :param bucket_name: Bucket to create
            :param region: String region to create bucket in, e.g., 'us-west-2'
            :return: True if bucket created, else False
        """
        if self.region_name is None:
            self.s3.create_bucket(Bucket=self.bucket_name)
        else:
            location = {'LocationConstraint': self.region_name}
            self.s3.create_bucket(Bucket=self.bucket_name,
                                  CreateBucketConfiguration=location)  

    @SDKdecorators.check_error
    def list_buckets(self):
        """
            Iterates all objects, extracts their names and returns back

            Returns:
                names (list<str>): List of bucket names
        """
        names = []
        for bucket in self.s3.buckets.all():
            names.append(bucket.name)
        return names

    @SDKdecorators.check_error
    def delete_bucket(self):
        return self.s3.Bucket(self.bucket_name).delete()

    @SDKdecorators.check_error
    def list_objects(self):
        """
            Connects to bucket and returns all file names present inside

            Returns:
                names (list<str>): List of bucket names
        """
        s3_objects = []

        # Connection to bucket
        s3_bucket = self.s3.Bucket(name=self.bucket_name)

        for s3_object in s3_bucket.objects.all():
            s3_objects.append(s3_object.key)
        return s3_objects

    @SDKdecorators.measure_time
    @SDKdecorators.check_error
    def download_object(self, fpath_in_bucket, fpath_local):
        try:
            self.s3.meta.client \
                .download_file(self.bucket_name, fpath_in_bucket, fpath_local)
            return True
        except Exception as exc:
            logging.error(exc)
            return True

    @SDKdecorators.measure_time
    @SDKdecorators.check_error
    def upload_object(self, fpath_in_bucket, fpath_local):
        """
            Uploads file from local to bucket and

            Arguments:
                * fpath_in_bucket (str): File path in bucket
                * fpath_local (str): File path in local machine
        """
        try:
            self.s3.Object(self.bucket_name,
                           fpath_in_bucket).upload_file(Filename=fpath_local)
            return True
        except Exception as exc:
            logging.error(exc)
            return False

    @SDKdecorators.check_error
    def delete_object(self, fpath: str):
        """
            Arguments:
                * fpath (str): Absolute fpath in buckets
                               (use list_obj)
        """
        try:
            self.s3.Object(self.bucket_name, fpath).delete()
            return True
        except Exception as exc:
            logging.error(exc)
            return False
