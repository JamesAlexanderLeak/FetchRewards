import boto3
from boto3.session import Session
import json
import psycopg2
import datetime
from psycopg2.extensions import AsIs, quote_ident

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
    response = 1
    #create python dict to hold PII
    piiDict = {
                "device_id":dict(),
                "ip":dict()
    }
    messages = 1
    while messages:
        #receive messages from sqs
        response = client.receive_message(
            QueueUrl = queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout = 60,
            WaitTimeSeconds=20
        )
        #get messages "receive_message"
        messages = response.get('Messages')
        #if not empty, 
        if messages is not None:
            for message in messages:
                #get message body
                message_body = message.get('Body')
                #print(message_body)
                #get message reciept handle to delete message after processing
                receipt_handle = message.get('ReceiptHandle')
                #pull from json
                jsonMessage = json.loads(message_body)
                #ensure keys are in message (deals with 'foo':'oops_wrong_msg_type' message)
                #use set 
                keys_to_check = {'user_id','device_type','ip','locale','app_version','device_id'}
                missing_keys = keys_to_check - set(jsonMessage.keys())
                if missing_keys:
                    client.delete_message(
                    QueueUrl = queue_url,
                    ReceiptHandle=receipt_handle
                    )
                    continue
                user_id = jsonMessage['user_id']
                device_type = jsonMessage['device_type']
                ip = jsonMessage['ip']
                masked_ip = hash(ip)
                piiDict['ip'][ip] = masked_ip
                #print(piiDict['ip'][ip])
                locale = jsonMessage['locale']
                device_id = jsonMessage['device_id']
                masked_device_id = hash(device_id)
                app_version = jsonMessage['app_version']
                app_version = app_version.split('.')
                app_version = app_version[0]
                piiDict['device_id'][device_id] = masked_device_id
                create_date = datetime.datetime.utcnow()
                #write to postgres
                cur.execute("""
                            INSERT INTO %s
                            VALUES (%s,%s,%s,%s,%s,%s,%s);
                    """,(
                        AsIs(quote_ident('user_logins',cur)),
                        user_id,
                        device_type,
                        masked_ip,
                        masked_device_id,
                        locale,
                        app_version,
                        create_date
                ))
                conn.commit()

                #delete message after processing
                client.delete_message(
                    QueueUrl = queue_url,
                    ReceiptHandle=receipt_handle
                )
    #dump python dict to "securedatabase.txt"
    #print(piiDict)
    with open('securedatabase.json','w') as outfile:
        json.dump(piiDict,outfile)
    

    #query database to show database
    print('Below is the entire postgresDB:')
    print('Schema shown below:')
    print("user_id,device_type,masked_ip,masked_device_id,locale,app_version,create_date")
    cur.execute("SELECT * FROM user_logins")
    records = cur.fetchall()
    print(records)

if __name__ == "__main__":
    main()