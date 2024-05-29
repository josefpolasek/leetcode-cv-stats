from dotenv import load_dotenv
import os

# Load environmental variables
load_dotenv()

# Leetcode username to fetch the data
USERNAME = os.environ['USERNAME']

# Google service account credentials dictionary
credentials_dict = {
    "type": os.environ['GOOGLE_TYPE'],
    "project_id": os.environ['GOOGLE_PROJECT_ID'],
    "private_key_id": os.environ['GOOGLE_PRIVATE_KEY_ID'],
    "private_key": os.environ['GOOGLE_PRIVATE_KEY'].replace('\\n', '\n'),
    "client_email": os.environ['GOOGLE_CLIENT_EMAIL'],
    "client_id": os.environ['GOOGLE_CLIENT_ID'],
    "auth_uri": os.environ['GOOGLE_AUTH_URI'],
    "token_uri": os.environ['GOOGLE_TOKEN_URI'],
    "auth_provider_x509_cert_url": os.environ['GOOGLE_AUTH_PROVIDER_X509_CERT_URL'],
    "client_x509_cert_url": os.environ['GOOGLE_CLIENT_X509_CERT_URL'],
    "universe_domain": os.environ['GOOGLE_UNIVERSE_DOMAIN']
}

# Documents and folders in GDrive
TEMPLATE_ID = os.environ['TEMPLATE_ID']
FOLDER_ID = os.environ['FOLDER_ID']
