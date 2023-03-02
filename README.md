Fetch Rewards Data Engineering take home assessment.

Requires docker container localstack running local instances of PostgreSQL and AWS SQS.
Goal is to read from AWS SQS, mask pii and load data into Postgres DB.
Fields to be masked are the device_id and the ip address,
and duplicate values must be able to be easily identifiable while still being masked.

Target table's DDL is:
    user_id             varchar(128),
    device_type         varchar(32),
    masked_ip           varchar(256),
    maked_device_id     varchar(256),
    locale              varchar(32),
    app_version         integer,
    create_date         date

Questions to be answered:
    **Note:* Since AWS SQS was utilized for reading data, most questions below will be answered with AWS products/services in mind

    How would you deploy this application to production?
    *Ensure testing and quality of code (unit testing, etc.) and ensure app is production ready
    *Create deployment pipeline and deploy AWS utilizing AWS CodeDeploy or utilize Docker/Kubernetes for containerization of code 
        (or deploy to AWS lambda for serverless architecture)
    *Utilize logging and monitoring for DevOps/SRE (AWS Cloudwatch/AWS Cloudtrail)

    What other components would you want to add to make this production ready?
    *Create unit testing and data quality testing for SQS data
    *Version database schema and migrations
    *Ensure data encryption for protection of sensitive data
    *Continuous Integration/Continuous Deployment pipeline for deployment

    How can this application scale with a growing dataset?
    *Utilize horizontal autoscaling in AWS Aurora or AWS RDS to host the postgres database
    *Utilize AWS SQS and AWS Elastic Load Balancer to handle message volume and distribute workload to multiple application servers
    *Depending on number of duplicate messages, possibly utilize distributed cache (memcache, redis or AWS elasticache)
    *Scale on AWS or on-prem servers to auto scale depending on workload (AWS EC2 or AWS Lambda (for serverless))
    *If size of messages grow and more fields are recieved, add additional table(s) to postgres schema
    *Add replication databases to add fault tolerance

    How can PII be recovered later on?
    *Currently, PII is hashed and stored in a python dict to ensure duplicate values are unchanged, but if additional time allowed,
    PII could be stored to a restricted access database instead of a python dict (can be restricted based on IAM (Identity and Access Management)),
    which could be recovered later on.
    *PII could also just not be stored in a database, instead could be encrypted with RSA with only certain restricted
        individuals having private keys.
    *Chose to go with hashed keys since it was easier and faster

    What are the assumptions you made?
    *Assumed data quality from SQS
    *Assumed no issues with postgres table
    *Assumed amount of data is not going to be unreasonable

