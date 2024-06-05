import logging
import logging.handlers
import os
import requests
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import io
from googleapiclient.http import MediaIoBaseUpload
from config import USERNAME, TEMPLATE_ID, FOLDER_ID, CREDENTIALS_DICT, FULL_NAME

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)


def get_leetcode_profile_data(username):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}/"
    response = requests.get(url)
    if response.status_code == 200:
        response_content = response.content.decode('utf-8')
        profile_data = json.loads(response_content)
        return profile_data
    else:
        raise Exception("Failed to retrieve LeetCode profile data.")


def main():
    try:
        # Step 1: Get data from Leetcode
        profile_data = get_leetcode_profile_data(USERNAME)
        easy = profile_data["easySolved"]
        medium = profile_data["mediumSolved"]
        hard = profile_data["hardSolved"]

        # Step 2: Copy the template
        SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_info(CREDENTIALS_DICT)
        credentials = credentials.with_scopes(SCOPES)
        drive_service = build('drive', 'v3', credentials=credentials)
        docs_service = build('docs', 'v1', credentials=credentials)

        copy_title = 'tmp'
        body = {'name': copy_title}
        drive_response = drive_service.files().copy(fileId=TEMPLATE_ID, body=body).execute()
        document_copy_id = drive_response.get('id')

        # Step 3: Replace placeholders
        replacements = {
            '{easy_solved}': str(easy),
            '{medium_solved}': str(medium),
            '{hard_solved}': str(hard)
        }

        requests = []
        for placeholder, value in replacements.items():
            requests.append({
                'replaceAllText': {
                    'containsText': {
                        'text': placeholder,
                        'matchCase': True
                    },
                    'replaceText': value,
                }
            })

        requests.append({
            'replaceAllText': {
                'containsText': {
                    'text': '{date}',
                    'matchCase': True
                },
                'replaceText': datetime.datetime.now().strftime("%Y-%m-%d"),
            }
        })

        result = docs_service.documents().batchUpdate(documentId=document_copy_id, body={'requests': requests}).execute()

        # Step 4: Delete duplicate CV.pdf
        file_name = f'CV_{FULL_NAME}.pdf'
        query = f'"{FOLDER_ID}" in parents and trashed=false and name="{file_name}"'
        results = drive_service.files().list(q=query).execute()
        files = results.get('files', [])
        if files:
            file_id = files[0]['id']
            drive_service.files().delete(fileId=file_id).execute()

        # Step 5: Export to PDF
        pdf_file = drive_service.files().export(fileId=document_copy_id, mimeType='application/pdf').execute()

        # Step 6: Upload the PDF
        file_metadata = {
            'name': f'CV_{FULL_NAME}.pdf',
            'parents': [FOLDER_ID]
        }
        pdf_file_io = io.BytesIO(pdf_file)
        media = MediaIoBaseUpload(pdf_file_io, mimetype='application/pdf')
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        # Step 7: Delete the tmp file
        drive_service.files().delete(fileId=document_copy_id).execute()

        # Final status log
        logger.info("Script completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        logger.info("Script failed.")


if __name__ == "__main__":
    main()
