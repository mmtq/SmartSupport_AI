# SmartSupport_AI

**SmartSupport_AI** is an intelligent customer support system designed to automate email processing, extract key details from customer queries, categorize issues, and generate AI-powered responses. The system leverages the Gmail API for fetching and sending emails, the LangChain framework for orchestrating workflows, and ChatGroq for advanced natural language understanding and response generation.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Authentication with Google Cloud](#authentication-with-google-cloud)
5. [Usage](#usage)
6. [How It Works](#how-it-works)
   
---

## Features

- **Automated Email Processing**: Fetches unread emails from your Gmail inbox using the Gmail API.
- **Whitelist Filtering**: Processes only emails from whitelisted senders to ensure relevance.
- **AI-Powered Issue Categorization**: Uses LangChain and ChatGroq to analyze email content and categorize issues.
- **Response Generation**: Automatically generates context-aware responses to customer queries.
- **Email Marking as Read**: Marks processed emails as read to avoid duplication.
- **Customizable Whitelist**: Easily manage a list of approved sender email addresses via a YAML file.

---

## Prerequisites

Before running the project, ensure you have the following:

1. **Python 3.8+**: Install Python from [python.org](https://www.python.org/).
2. **Google Cloud Account**: Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
3. **Gmail API Enabled**: Enable the Gmail API for your project.
4. **OAuth 2.0 Credentials**: Generate OAuth 2.0 credentials for Gmail API access.
5. **Environment Variables**: Set up environment variables for sensitive data (e.g., `EMAIL_USER`).
6. **Dependencies**: Install required Python libraries using `pip`.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mmtq/SmartSupport_AI.git
   cd SmartSupport_AI
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Prepare the Whitelist**:
   Create a whitelist.yaml file in the root directory and add whitelisted email addresses:
   ```yaml
   whitelist:
    - sender1@example.com
    - sender2@example.com
5. **Download OAuth 2.0 Credentials**:
    * Go to the [Google Cloud Console](https://console.cloud.google.com/).
    * Navigate to **APIs & Services > Credentials**.
    * Download the `credentials.json` file.
    * Place the file in the root directory of your project.

## Authentication with Google Cloud

To use the Gmail API, you need to authenticate your application using OAuth 2.0. Follow these steps:

### Step 1: Enable the Gmail API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services > Library**.
4. Search for **"Gmail API"** and enable it.

### Step 2: Create OAuth 2.0 Credentials
1. In the Google Cloud Console, go to **APIs & Services > Credentials**.
2. Click **Create Credentials** and select **OAuth Client ID**.
3. Configure the consent screen if prompted.
4. Select **Desktop App** as the application type.
5. Download the `credentials.json` file and place it in the root directory of the project.

### Step 3: Authenticate Locally
1. Run the script for the first time:
   ```bash
   python main.py
2. A browser window will open, prompting you to log in to your Google account.
3. Grant the requested permissions (e.g., read, modify, and send emails).
4. After authentication, a ```token.json``` file will be created to store your credentials.

> **Note:** If you encounter a `redirect_uri_mismatch` error, ensure the redirect URI (`http://localhost:8080/`) is added to the **Authorized Redirect URIs** in the Google Cloud Console.

## Usage

### Run the Script:

```python main.py```

The script will fetch unread emails, process them, and display details such as the sender, subject, and body. It will then generate an AI-powered response and send it.  

### Example Output:
  ```plaintext
  Fetching unread emails...
  
  Sender: John Doe <john.doe@example.com>  
  Subject: Support Request  
  Body: I'm having trouble with my account login.  
  
  Generating AI response...  
  Reply: Hello John,  
  We understand your concern regarding login issues. Please try resetting your password using the "Forgot Password" option on the login page. If the issue persists, let us know, and we'll assist you further.  
  
  Sending response... ✅
  ```
## How It Works

1. **Fetch Emails**:
  The script uses the Gmail API to fetch unread emails from the primary inbox.  
  Only emails from whitelisted senders are processed.

2. **Parse Email Content**:
  It extracts the sender's name, email address, subject, and body using the `parse_email()` method.

3. **Categorize Issues**:
  Leverages LangChain and ChatGroq to analyze the email body and categorize the issue (e.g., billing, technical support).

4. **Generate Responses**:
  Uses ChatGroq's natural language capabilities to generate context-aware responses.

5. **Mark as Read**:
  Marks processed emails as read to prevent duplicate processing.

6. **Send Responses**:
  Sends AI-generated responses back to the sender using the Gmail API.

## Acknowledgments

- **Google Cloud Platform**: For providing the Gmail API.
- **LangChain**: For enabling seamless integration of AI workflows.
- **ChatGroq**: For advanced natural language understanding and response generation.

