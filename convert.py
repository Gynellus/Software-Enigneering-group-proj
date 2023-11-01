import os
import requests
from bs4 import BeautifulSoup
import fitz

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
        response = requests.get(input_data)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text()
        else:
            return 'Failed to fetch content from URL'

    # Input is a string (not a file path or URL)
    elif isinstance(input_data, str):
        return input_data

    # Case 4: Other data types (e.g., numbers, lists, etc.)
    else:
        return "Not one of the supported data formats (URL, .PDF. string)"
