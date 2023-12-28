# STANDARD LIBRARY
from email.message import Message
import email

# LAMBDA LAYERS
# from flask import Flask, request
import boto3

def email_in(event):
    # first code will fetch fromaddress, subject and messageId
    # then it will call workmail API to fetch actual message using this messageId
    # and then it will parse the message properly to convert it into text message

    workmail = boto3.client('workmailmessageflow')

    # from_addr = event['envelope']['mailFrom']['address']
    # subject = event['subject']
    # flowDirection = event['flowDirection']
    msg_id = event['messageId']

    # calling workmail API to fetch message body
    raw_msg = workmail.get_raw_message_content(messageId=msg_id)
    t = raw_msg['messageContent'].read()
    parsed_msg = email.message_from_bytes(t)

    if parsed_msg.is_multipart():
        for part in parsed_msg.walk():
            # returns a bytes object
            payload = part.get_payload(decode=True)
            if type(payload) is bytes:
                msg_text = payload.decode('utf-8')  # utf-8 is default
                print('*** Multipart payload ****', msg_text)
                break
    else:
        payload = parsed_msg.get_payload(decode=True)
        if type(payload) is bytes:
            msg_text = payload.decode('utf-8')  # utf-8 is default
            print('*** Single payload ****', msg_text)
            
    return msg_text
