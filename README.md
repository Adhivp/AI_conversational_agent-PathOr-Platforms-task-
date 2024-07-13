# AI conversational bot

This project provides a set of utilities for data analysis, report generation, and email functionality. It includes modules for reading data from various file formats, generating PDF reports with visualizations, and sending emails with attachments.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Data Utilities](#data-utilities)
  - [Email Utilities](#email-utilities)
  - [Report Utilities](#report-utilities)
  - [Streamlit Application](#streamlit-application)
## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Adhivp/AI_conversational_agent-PathOr-Platforms-task-.git
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up environment variables by creating a `.env` file with the following content:
    ```env
    EMAIL_ADDRESS=your-email@example.com
    EMAIL_PASSWORD=your-email-password
    SMTP_SERVER=smtp.example.com
    SMTP_PORT=587
    ```

## Usage

### Data Utilities

The `data_utils.py` module provides functions to read data from Excel and CSV files and extract specific data.

```python
import pandas as pd
from data_utils import read_excel, read_csv, extract_data

# Read data from an Excel file
df_excel = read_excel('path_to_file.xlsx', sheet_name='Sheet1')

# Read data from a CSV file
df_csv = read_csv('path_to_file.csv')

# Extract specific data
data = extract_data(df_csv, row_index=0, column_name='column_name')
```

### Email Utilities

The `email_utils.py` module provides a function to send emails with a PDF attachment. 

```python
from email_utils import send_email
from datetime import datetime

# Send an email with an attachment
send_email(
    to_address='recipient@example.com',
    subject='Data Analysis Report',
    body='Please find attached the data analysis report.',
    attachment_path='path_to_attachment.pdf',
    attachment_name='data_analysis_report.pdf',
    send_datetime=datetime(2023, 7, 15, 10, 30)  # Optional: Schedule email for future
)
```

### Report Utilities

The `report_utils.py` module provides functions to generate a PDF report with data analysis and visualizations.

```python
import pandas as pd
from report_utils import generate_pdf_report

# Read data from a CSV file
df = pd.read_csv('path_to_file.csv')

# Generate a PDF report
pdf_buffer, pdf_path = generate_pdf_report(df)
```

### Streamlit Application

The `main.py` file contains a Streamlit application that allows users to upload a CSV file, generate a PDF report, and send the report via email.

1. Run the Streamlit application:
    ```sh
    streamlit run main.py
    ```

2. Use the web interface to upload a CSV file, generate a report, and send the report via email.