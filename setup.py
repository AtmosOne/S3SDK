from setuptools import setup


def readme():
    with open("README.md", 'r') as f:
        return f.read()


setup(
   name='S3SDK',
   version='0.0.1',
   description='SDK for working with S3 bucket',
   long_description=readme(),
   long_description_content_type='text/markdown',
   author='Adil Rashitov',
   author_email='adil.rashitov.98@gmail.com',
   packages=['S3SDK'],
   install_requires=['boto3'])