# Leetcode CV Automatic Stats

This project automates updating a CV with the latest LeetCode statistics and generating a PDF document. The entire workflow runs automatically using GitHub Actions.

## Overview

1. **LeetCode Stats Retrieval**: Fetch LeetCode statistics from a user's profile using the [leetcode-stats-api](https://github.com/JeremyTsaii/leetcode-stats-api).
2. **Google Docs Template Update**: Copy a Google Docs template and replace placeholders with retrieved statistics.
3. **PDF Export and Cleanup**: Export the updated document as a PDF using the Google Drive API and delete temporary files.

The process runs automatically using GitHub Actions at midnight UTC.

## Setup
1. Clone the repository
2. Install required packages: `pip install -r requirements.txt`
3. Create a folder and add your own Google Docs template with these placeholders:
    - `{date}`	
    - `{easy_solved}`
    - `{medium_solved}`
    - `{hard_solved}`
4. Create a Google Cloud Platform project, enable the Google Drive API and Google Docs API, and share both the folder and the template with the service account email.
5. Create your own `.env` file with variables as shown in the `.env.example` file.
6. Run the script locally: `python main.py`
