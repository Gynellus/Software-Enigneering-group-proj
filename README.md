# Text Summarization and Similarity Finder Tool

## Overview
This repository contains a Flask-based web application designed for text summarization and finding similar academic papers. The application provides functionalities to summarize academic papers, translate summaries to Dutch, and find papers similar to a given text. It leverages OpenAI's GPT-3.5 Turbo model for summarization and translation tasks.

### Similarity Finder
The similarity finder feature is built upon embeddings from [LiteratureReviewBot](https://github.com/daveshap/LiteratureReviewBot/tree/main). After downloading the embedded arXiv.org papers, this feature can be used to find papers similar to a specific input paper.

### Translation
Originally, an OpenNMT model was used for translation, but due to its slow performance and high computational requirements, it was replaced with OpenAI's ChatGPT 3.5 Turbo model. This model currently supports translation to Dutch.

## Setup and Installation

### Prerequisites
- Python 3.11
- Conda environment (recommended for isolating dependencies)

### Installation Steps
1. **Clone the Repository**: Start by cloning this repository to your local machine.

2. **OpenAI API Key**: To use the application, you must obtain an API key from OpenAI. Once obtained, create a file named `openai_API_key.txt` in the main directory of this project and paste your API key into this file.

3. **Install Dependencies**:
   - Set up a fresh conda environment.
   - Run `pip install -r requirements.txt` to install the required Python packages.

4. **Start the Application**: Run `application.py` to start the Flask server.

## Running the Application
Once the server is running, navigate to the hosted URL (typically `http://localhost:5000`) in your web browser to access the application.

## Unit Testing
Unit tests have been performed to ensure the reliability and accuracy of the application. These tests are available in a separate file named `unit_tests.py` in the repository.