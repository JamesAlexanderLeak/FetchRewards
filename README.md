Fetch Rewards Data Engineering take home assessment.
Requires docker container localstack running local instances of PostgreSQL and AWS SQS.
Goal is to read from AWS SQS, mask pii and load data into Postgres DB.
Fields to be masked are the device_id and the ip address, and duplicate values must be able to be easily identifiable while still being masked.
Target table's DDL is:
    user_id             varchar(128),
    device_type         varchar(32),
    masked_ip           varchar(256),
    maked_device_id     varchar(256),
    locale              varchar(32),
    app_version         integer,
    create_date         date

Questions to be answered:
    How would you deploy this application to production?


    What other components would you want to add to make this production ready?


    How can this application scale with a growing dataset?


    How can PII be recovered later on?


    What are the assumptions you made?


