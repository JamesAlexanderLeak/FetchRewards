import boto3
from boto3.session import Session
import json
session = boto3.Session()
queue_url = 'http://localhost:4566/000000000000/login-queue'
client = session.client('sqs',
                        endpoint_url='http://localhost:4566/000000000000/login-queue',
                        region_name='us-west-2',
                        aws_secret_access_key='x',
                        aws_access_key_id='x',
                        use_ssl=False)
response = client.receive_message(
    QueueUrl = queue_url,
    MaxNumberOfMessages=1,
    VisibilityTimeout = 60,
    WaitTimeSeconds=20
)
messages = response.get('Messages')
if messages is not None:
    for message in messages:
        message_body = message.get('Body')
        print(message_body)
        print(type(message_body))
        m = json.loads(message_body)
        print(m['user_id'])
        """
        receitp_handle = message.get('RecieptHandle')
        client.delete_message(
            QueueUrl = queue_url,

        )
        """
#print(messages)