import  boto3
import  logging


class S3SDK:
    """
        Module for working with S3 bucket

        * s3 (boto3): Public static s3 object
    """
    def __init__(self, credentials={}, bucket_name=''):
        self.credentials = credentials
        self.s3 = S3SDK.init_s3_resource(credentials)
        self.bucket_name = bucket_name

    @staticmethod
    def init_s3_resource(credentials):
        if len(list(credentials.keys())) > 0:
            if 'aws_secret_access_key' in credentials and 'aws_access_key_id' in credentials:
                return boto3.resource('s3',**credentials)
            else:
                logging.error("Please, provide all credentials")
                raise  ValueError("Incomplete credentials")
        else:
            return boto3.resource('s3')

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

    def download_object():
        pass

    def upload_object(self, fpath_in_bucket, fpath_local):
        """
            Uploads file from local to bucket and

            Arguments:
                * fpath_in_bucket (str): File path in bucket
                * fpath_local (str): File path in local machine
        """
        self.s3.Object(self.bucket_name,
                       fpath_in_bucket).upload_file(Filename=fpath_local)

    def delete_object():
        pass
