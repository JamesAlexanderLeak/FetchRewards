# Fetch Rewards Data Engineering take home assessment.

Goal is to read from AWS SQS, mask pii and load data into Postgres DB.

Full PDF can be found [here](https://fetch-hiring.s3.amazonaws.com/data-engineer/pii-masking.pdf).

Fields to be masked are the device_id and the ip address and duplicate values must be able to be easily identifiable while still being masked.

Target table's schema is:
* user_id : varchar(128)
* device_type : varchar(32)
* masked_ip : varchar(256)
* maked_device_id : varchar(256)
* locale : varchar(32)
* app_version : integer (read from SQS as a version i.e. 2.3.0, 0.2.6 or 0.96 so just take first num)  
* create_date : date
    
## **To Run the Application**
1. Requires docker container localstack running local instances of [PostgreSQL](https://hub.docker.com/r/fetchdocker/data-takehome-postgres?) and [AWS SQS](https://hub.docker.com/r/fetchdocker/data-takehome-localstack?) so please ensure you have the appropriate docker images.
2. Requires python (my version is 3.10), AWS SDK for python boto3 (pip install boto3), and postgres db adapter psycopg2 (pip install psycopg2).
3. In order to run program, run 'docker-compose up' on command line to start containers and wait a little bit to allow them to spin up. Then run "python3 maskPII.py" in the terminal.
4. The program may take a little bit of time as it must wait 20 seconds to ensure no other AWS SQS messages are left.
5. After python program is run, postgres DB should have 'device_id' and 'ip' as masked values with other values the same as from AWS SQS.
6. Output of program to terminal is a query of the postgreSQL database, with the schema of the database at the top and each row delimited by parentheses.
7. Additionally, a "securedatabase.json" of the true ip to masked ip and true device id to masked device id is generated, with an expectation that if this were a real application, the "securedatabase.json" could be created to map the pii.

## **Questions to be answered**

**Note:** Since AWS SQS was utilized for reading data, most questions below will be answered with AWS products/services in mind.

1. How would you deploy this application to production?
   * Ensure testing and quality of code (unit testing, etc.) and ensure app is production ready.
   * Create deployment pipeline and deploy AWS utilizing AWS CodeDeploy or utilize Docker/Kubernetes for containerization of code (or deploy to AWS lambda for serverless architecture).
   * Utilize logging and monitoring for DevOps/SRE (AWS Cloudwatch/AWS Cloudtrail).

2. What other components would you want to add to make this production ready?
   * Create unit testing and data quality testing for SQS data.
   * Version database schema and migrations.
   * Ensure data encryption for protection of sensitive data.
   * Continuous Integration/Continuous Deployment pipeline for deployment.
   * If I had more time, I would also refactor code and make it cleaner.

3. How can this application scale with a growing dataset?
   * Utilize horizontal autoscaling in AWS Aurora or AWS RDS to host the postgres database.
   * Utilize AWS SQS and AWS Elastic Load Balancer to handle message volume and distribute workload to multiple application servers.
   * Depending on number of duplicate messages, possibly utilize distributed cache (memcache, redis or AWS elasticache).
   * Scale on AWS or on-prem servers to auto scale depending on workload (AWS EC2 or AWS Lambda (for serverless)).
   * If size of messages grow and more fields are recieved, add additional table(s) to postgres schema.
   * Add replication databases to add fault tolerance.

4. How can PII be recovered later on?
   * Currently, PII is hashed and stored in a python dict to ensure duplicate values are unchanged, but if additional time allowed,
PII could be stored to a restricted access database instead of a python dict (can be restricted based on IAM (Identity and Access Management)),
which could be recovered later on.
   * PII could also just not be stored in a database, instead could be encrypted with RSA with only certain restricted
    individuals having private keys.
   * Chose to go with python hash function since it was easier. In real scenario, would encrypt data.

5. What are the assumptions you made?
   * Assumed data quality from SQS.
   * Assumed no issues with postgres table.
   * Assumed amount of data is not going to be unreasonable.

