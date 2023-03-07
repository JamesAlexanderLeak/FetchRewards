import boto3
from boto3.session import Session
import json
import psycopg2
import datetime
from psycopg2.extensions import AsIs, quote_ident
import os

#queue_url
queue_url = 'http://localhost:4566/000000000000/login-queue'
DB_HOST = os.environ.get('DB_HOST','localhost')
DB_NAME = os.environ.get('DB_NAME','postgres')
DB_USER = os.environ.get('POSTGRES_USER','postgres')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD','postgres')
AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME','us-west-2')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY','x')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID','x')

def connect_to_postgres():
    """
    Connects to postgres DB returns database cursor
    """
    #connect to postgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    #establish database cursor
    cur = conn.cursor()
    return conn,cur

def connect_to_sqs():
    """
    Creates AWS SQS client, returns client variable
    """
    #establish SQS session
    session = boto3.Session()

    #create SQS client
    client = session.client('sqs',
                            endpoint_url=queue_url,
                            region_name=AWS_REGION_NAME,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            use_ssl=False)
    return client
    
def create_pii_dict():
    """
    Creates the pii dictionary that maps real values to hashed values
    """
    return {
            "device_id":dict(),
               "ip":dict()
    }
def get_response(client):
    """
    Receives message from sqs. 'client' is SQS connection
    """
    return client.receive_message(
        QueueUrl = queue_url,
        MaxNumberOfMessages=1,
        VisibilityTimeout = 60,
        WaitTimeSeconds=20
        )

def send_to_secure_database(piiDict: dict):
    """
    Sends a piiDict to a "secure database", dumps piiDict to a file as a json
    """
    with open('securedatabase.json','w') as outfile:
        json.dump(piiDict,outfile)

def main():
    
    #create postgres connection
    conn,cur = connect_to_postgres()
    #create client connection to sqs
    client = connect_to_sqs()
    #response = 1
    #create python dict to hold PII
    piiDict = create_pii_dict()
    messages = 1
    while messages:
        #receive messages from sqs
        response = get_response(client)
        #get messages "receive_message"
        messages = response.get('Messages')
        #if not empty, 
        if messages is not None:
            for message in messages:
                #get message body
                message_body = message.get('Body')
                #get message reciept handle to delete message after processing
                receipt_handle = message.get('ReceiptHandle')
                #pull from json
                jsonMessage = json.loads(message_body)
                #ensure keys are in message (deals with 'foo':'oops_wrong_msg_type' message)
                #use set 
                try:
                    masked_ip = hash(jsonMessage['ip'])
                    piiDict['ip'][jsonMessage['ip']] = masked_ip
                    masked_device_id = hash(jsonMessage['device_id'])
                    piiDict['device_id'][jsonMessage['device_id']] = masked_device_id
                    app_version = jsonMessage['app_version']
                    app_version = app_version.split('.')
                    app_version = app_version[0]
                    cur.execute(f"""
                            INSERT INTO {AsIs(quote_ident('user_logins',cur))}
                            VALUES ('{jsonMessage['user_id']}','{jsonMessage['device_type']}','{masked_ip}','{masked_device_id}','{jsonMessage['locale']}','{app_version}','{datetime.datetime.utcnow()}');
                    """,)
                    conn.commit()

                    #delete message after processing
                    client.delete_message(
                        QueueUrl = queue_url,
                        ReceiptHandle=receipt_handle
                    )
                except KeyError:
                    print(f"Key Error on message {receipt_handle}, deleting message and continuing")
                    client.delete_message(
                        QueueUrl = queue_url,
                        ReceiptHandle=receipt_handle
                    )
                    continue
    #dump python dict to "securedatabase.txt"
    send_to_secure_database(piiDict)
    
    #query database to show database
    print('Below is the entire postgresDB:')
    print('Schema shown below:')
    print("user_id,device_type,masked_ip,masked_device_id,locale,app_version,create_date")
    cur.execute("SELECT * FROM user_logins")
    records = cur.fetchall()
    print(records)

if __name__ == "__main__":
    main()