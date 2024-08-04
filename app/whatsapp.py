import logging
from twilio.rest import Client
from .config import Config

def send_whatsapp_message(msg):
    if not Config.SEND_WHATSAPP_MESSAGES:
        # Return early if sending messages is disabled in the config
        return 0

    try:
        client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=msg,
            from_=f'whatsapp:{Config.TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{Config.TARGET_WHATSAPP_NUMBER}'
        )
        return message.sid
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None