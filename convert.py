import os
import requests
from bs4 import BeautifulSoup
import fitz
from io import BytesIO

def convert_input_to_string(input_data):
    # Input is .pdf
    if isinstance(input_data, str) and os.path.isfile(input_data):
        _, file_extension = os.path.splitext(input_data)

        if file_extension.lower() == '.pdf':
            document = fitz.open(input_data)
            text = ''
            for page in document:
                text += page.get_text()
            return text
        else:
            return 'Unsupported file format'

    # Input is URL
    elif isinstance(input_data, str) and input_data.startswith(('http://', 'https://')):
        try:
            response = requests.get(input_data)
            response.raise_for_status()
            content_type = response.headers['Content-Type']
            if 'application/pdf' in content_type:
                document = fitz.open(stream=BytesIO(response.content), filetype="pdf")
                text = ''
                for page in document:
                    text+= page.get_text()
                return text
            else:
                soup = BeautifulSoup(response.content, 'html.parser')
                return soup.get_text()
        except Exception as e:
            return f'Failed to fetch content from URL: {e}'

    # Input is a string (not a file path or URL)
    elif isinstance(input_data, str):
        return input_data

    # Case 4: Other data types (e.g., numbers, lists, etc.)
    else:
        return "Unsupported data format"


