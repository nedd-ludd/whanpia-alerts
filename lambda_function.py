# telnyx_message

# STANDARD LIBRARY
import json
import os

# OWN MODULES
from ingest_email import email_in
from telnyx_service import notify
from helpers import CHECK_CONTENT
from helpers import EVENT_TYPE_REST

test = False
if test == True:
    customer = os.environ.get('TESTER')
else:
    customer = os.environ.get('CUSTOMER')


def lambda_handler(event, context):
    try:
        if EVENT_TYPE_REST(event):
            print("rest event received")
        else:
            print("email event received")

        msg_text = email_in(event)
        print(msg_text)

        if CHECK_CONTENT(msg_text):
            print("phrases detected, attempting to notify customer...")
            notify(customer)

    except Exception as e:
        # Send some context about this error to Lambda Logs
        print(e)
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
