import boto3
from boto3.session import Session
import json
import psycopg2

def main():

    #establish SQS session
    session = boto3.Session()
    queue_url = 'http://localhost:4566/000000000000/login-queue'

    #create SQS client
    client = session.client('sqs',
                            endpoint_url='http://localhost:4566/000000000000/login-queue',
                            region_name='us-west-2',
                            aws_secret_access_key='x',
                            aws_access_key_id='x',
                            use_ssl=False)

    #connect to postgreSQL database
    conn = psycopg2.connect(
        host='localhost',
        dbname='postgres',
        user='postgres',
        password='postgres'
    )
    
    #establish database cursor
    cur = conn.cursor()

    #receive messages from sqs
    response = client.receive_message(
        QueueUrl = queue_url,
        MaxNumberOfMessages=1,
        VisibilityTimeout = 60,
        WaitTimeSeconds=20
    )
    
    #get messages "receive_message"
    messages = response.get('Messages')
    if messages is not None:
        for message in messages:
            message_body = message.get('Body')
            print(message_body)
            print(type(message_body))
            jsonMessage = json.loads(message_body)
            print(jsonMessage['user_id'])
            cur.execute("INSERT INTO user_logins (user_id) VALUES (\'%s\')" % str(jsonMessage['user_id']))
            conn.commit()
            cur.execute("SELECT * FROM user_logins")
            records = cur.fetchall()
            print(records)
            """
            receipt_handle = message.get('RecieptHandle')
            client.delete_message(
                QueueUrl = queue_url,

            )
            """

if __name__ == "__main__":
    main()