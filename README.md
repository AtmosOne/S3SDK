# S3SDK

This SDK is created to reduce amount of code with AWS S3 bucket

## **Prerequisites**

Before using S3 SDK **credentials** are required. It can be provided by next 2 ways:

1. Preconfiguration AWS CLI:
    * Install AWS CLI
    * hit next command in terminal:

```bash
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE # YOUR IAM ACCESS ID
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY # YOUR IAM SECRET KEY
Default region name [None]: us-west-2
Default output format [None]: json
```

2. Providing `dict` of credentials to `S3SDK` constructor:

```Python
import S3SDK

credentials = {
    'aws_access_key_id': 'AKIAIOSFODNN7EXAMPLE',
    'aws_secret_access_key_': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',  # YOUR IAM SECRET
}

s3 = S3SDK(credentials=credentials)
```

*NOTE*: In case of the second way don't spot your credentials & store them as your environment variables