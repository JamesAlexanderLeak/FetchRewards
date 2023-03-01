import subprocess

result = subprocess.run([r'C:\Python310\Lib\site-packages\awscli','sqs','receive-message','--queue-url','http://localhost:4566/000000000000/login-queue'])
result.stdout






"""
import boto3
from boto3.session import Session

#sqs_endpoint = '4566:4566'
sqs_client = boto3.client('sqs',endpoint_url='http://localhost:4566/000000000000/login-queue')
"""
"""
sqs = boto3.client('sqs',region_name='us-west-2')
queue_url = 'http://localhost:4566/000000000000/login-queue'
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10
)
messages = response.get('Messages')
print(messages)
"""