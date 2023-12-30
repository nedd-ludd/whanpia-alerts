# AWS

## Lambda

### Environment Variables

#### Main lambda function

```
ALERT_SERVICE_NUMBER = +44XXXXXXXXX
CALL_CONN_ID = 0000000000000000000
CUSTOMER = +44XXXXXXXXX
TEL_API_KEY = KEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TESTER = +44XXXXXXXXX
```

#### Webhook lambda function

```
TEL_API_KEY = KEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Testing

#### Main lambda function

Replace messageID with real messsage.

```json
{
  "summaryVersion": "2019-07-28",
  "envelope": {
    "mailFrom": {
      "address": "from@domain.test"
    },
    "recipients": [
      {
        "address": "recipient1@domain.test"
      },
      {
        "address": "recipient2@domain.test"
      }
    ]
  },
  "sender": {
    "address": "sender@domain.test"
  },
  "subject": "Hello From Amazon WorkMail!",
  "messageId": "REPLACE_MSG_ID_HERE",
  "invocationId": "0000000000000000000000000000000000000000",
  "flowDirection": "OUTBOUND",
  "truncated": false
}
```

#### Webhok lambda function

```
Not created
```

## S3 Bucket

### Permissions

To allow public access, set the Bucket Policy to the following JSON, replacing "XXXXXXXXXXXXXXXX" with bucket name to get ARN.

````json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::XXXXXXXXXXXXXXXX/*"
        }
    ]
}```

````

## WorkMail

### Configure permissions for WorkMail

```bash
aws --region REGION lambda add-permission --function-name MY_FUNCTION_NAME
--statement-id AllowWorkMail
--action "lambda:InvokeFunction"
--principal workmail.REGION.amazonaws.com
--source-arn arn:aws:workmail:REGION:AWS_ACCOUNT_ID:organization/WORKMAIL_ORGANIZATION_ID
```

### IAM Policies - AWSLambdaBasicExecutionRole

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "logs:CreateLogGroup",
      "Resource": "arn:aws:logs:us-east-1:XXXXXXXXXXXX:*"
    },
    {
      "Effect": "Allow",
      "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
      "Resource": [
        "arn:aws:logs:us-east-1:XXXXXXXXXXXX:log-group:/aws/lambda/XXXXXX:*"
      ]
    },
    {
      "Action": ["workmailmessageflow:GetRawMessageContent"],
      "Resource": "arn:aws:workmailmessageflow:us-east-1:XXXXXXXXXXXX:message/*",
      "Effect": "Allow"
    }
  ]
}
```

# Python

## Python Packaging for Lambda Layer

Required directory structure:

```
python/lib/python3.x/site-packages
```

To install package in current directory:

```bash
pip install --platform manylinux2014_x86_64 --target=package --implementation cp --python-version 3.12 --only-binary=:all: --upgrade telnyx
```

To package a virtual env from linux machine:

```bash
#!/bin/bash

# this is b/c pipenv stores the virtual env in a different
# directory so we need to get the path to it
SITE_PACKAGES=$(pipenv --venv)/lib/python3.10/site-packages
echo "Library Location: $SITE_PACKAGES"
DIR=$(pwd)

# Make sure pipenv is good to go
echo "Do fresh install to make sure everything is there"
pipenv install

cd $SITE_PACKAGES
zip -r9 $DIR/package.zip *
```
