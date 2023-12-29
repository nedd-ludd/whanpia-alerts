import telnyx
import os

def notify(customer):
    telnyx.api_key = os.environ.get('TEL_API_KEY')
    alert_service_number = os.environ.get('ALERT_SERVICE_NUMBER')
    
    # sending message
    alert_message = "***ALERT***\nThis is an automated message from Whanpia. We have detected an email from facebook where something has been accessed or changed in your account."

    resp = telnyx.Message.create(
        from_=alert_service_number,
        to=customer,
        text=alert_message,
    )
        
    # making call
    call_conn_id = os.environ.get('CALL_CONN_ID')
    telnyx.Call.create(
        connection_id=call_conn_id,
        from_=alert_service_number,
        to=customer,
        )
        
