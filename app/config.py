import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class Config:
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
    YOUTUBE_CHANNEL_HANDLE = os.environ.get('YOUTUBE_CHANNEL_HANDLE')
    TASK_TO_BE_COMPLETED = os.environ.get('TASK_TO_BE_COMPLETED')
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.environ.get('TWILIO_WHATSAPP_NUMBER')
    TARGET_WHATSAPP_NUMBER = os.environ.get('TARGET_WHATSAPP_NUMBER')
    SEND_WHATSAPP_MESSAGES = os.environ.get(
        'SEND_WHATSAPP_MESSAGES', False) == "True"
