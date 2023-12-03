import os
import requests
from bs4 import BeautifulSoup
import fitz
from io import BytesIO
import json
import numpy as np
import tensorflow_hub as hub
from openai import OpenAI

# Process the paper data to find summary and similar papers.
def process_paper_data(paper_text):
    
    similar_papers = find_similar_papers(paper_text)
    similar_papers = summarize_similar_papers(similar_papers)
    return similar_papers

# Summarize the similar papers.
def summarize_similar_papers(similar_papers):
    """ Summarize similar papers. """
    for paper in similar_papers:
        paper_text = convert_input_to_string(paper['url'])
        paper['summary'] = summarize(paper_text)
    return similar_papers



# Function to calculate cosine similarity between two vectors
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

# Generator function to load embeddings one by one to save memory
def load_embeddings(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                article = json.load(f)
                yield article['embedding'], article

# Function to find similar papers based on input text
def find_similar_papers(input_text):
    # Load Universal Sentence Encoder
    embed = hub.load('https://tfhub.dev/google/universal-sentence-encoder-large/5')
    
    # Embedding for the input text
    input_embedding = embed([input_text]).numpy()

    # Initialize list to store similarities and corresponding articles
    similarities = []
    articles = []

    path = 'Data/similarity_finder_Data'
    if not os.path.isdir(path):
        path = 'Data/DataSample_SimilarityChecker' # Small data sample included in this repo. Full data can be downloaded at https://www.kaggle.com/datasets/ltcmdrdata/arxiv-embeddings

    # Load and compare each embedding
    for embedding, article in load_embeddings(path):
        sim = cosine_similarity(input_embedding[0], embedding)
        similarities.append(sim)
        articles.append(article)

    # Get the top 5 most similar articles
    top_indices = np.argsort(similarities)[-5:][::-1]
    top_articles = [articles[idx] for idx in top_indices]
    top_similarities = [similarities[idx] for idx in top_indices]

    # Prepare the list of results
    results = []
    for article, similarity in zip(top_articles, top_similarities):
        sim_2_decimals = f"{similarity:.2f}"
        url = f"https://arxiv.org/pdf/{article['id']}.pdf"
        paper_info = {"url": url, "similarity": sim_2_decimals, "title": article['title']}
        results.append(paper_info)

    return results


# Function to convert html, pdf or string input to string
def convert_input_to_string(input_data):
    # If input is .pdf
    if isinstance(input_data, str) and os.path.isfile(input_data):
        _, file_extension = os.path.splitext(input_data)

        if file_extension.lower() == '.pdf':
            try:
                document = fitz.open(input_data) # Open PDF file with fitz
                text = ''
                for page in document:
                    text += page.get_text()
                return text
            except Exception as e:
                return f'Failed to open PDF file: {e}'
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
                    text += page.get_text()
                return text
            else:
                soup = BeautifulSoup(response.content, 'html.parser')
                return soup.get_text()
        except Exception as e:
            return f'Failed to fetch content from URL: {e}'

    # Input is a string (not a file path or URL)
    elif isinstance(input_data, str):
        return input_data

    # Other
    else:
        return "Unsupported data format"
    

    
def summarize(article):
    if not article:
        raise ValueError("Input text cannot be empty.")
    # Load OpenAI API key
    if 'openai_API_key.txt' not in os.listdir():
        raise Exception("Please add your OpenAI API key to openai_API_key.txt to the main directory of this project.")
    with open('openai_API_key.txt', 'r') as f:
        key = f.read().strip()

    client = OpenAI(api_key=key)

    summary = ""
    sections = []
    
    # # Split the article into sections of 8000 characters or less
    # while len(article) > 8000:
    #     # Find the last period before the 8000th character
    #     last_period = article[:8000].rfind('.')
    #     # If there is no period, split at the 8000th character
    #     if last_period == -1:
    #         last_period = 8000
    #     # Add the section to the list of sections
    #     sections.append(article[:last_period])
    #     # Remove the section from the article
    #     article = article[last_period:]

    # Add the last section to the list of sections
    try:
        sections.append(article[:5000])
    except IndexError:
        sections.append(article)

    # Call OpenAI API to summarize the sections
    for section in sections:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize academic papers or sections of papers"},
                {"role": "user", "content": f"Summarize the following: {section}"},
            ]
        )
        summary += completion.choices[0].message.content + "\n\n"

    # If there was more than one section, summarize the summary
    if len(sections) > 1:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize academic papers or sections of papers"},
                {"role": "user", "content": f"Summarize the paper: {summary}"},
            ]
        )
        summary = completion.choices[0].message.content

    return summary



def translate_to_dutch(text):
    if not text:
        raise ValueError("Input text cannot be empty.")

    # Load OpenAI API key
    if 'openai_API_key.txt' not in os.listdir():
        raise Exception("Please add your OpenAI API key to openai_API_key.txt in the main directory of this project.")
    with open('openai_API_key.txt', 'r') as f:
        key = f.read().strip()

    client = OpenAI(api_key=key)

    # Call OpenAI API to translate the text to Dutch
    prompt = f"Translate the following English text to Dutch:\n\n{text}"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a translator. You provide only the translation, with no additional context. You format the translation between [[ and ]]."},
            {"role": "user", "content": prompt},
        ]
    )

    # Extract the translated text from the response
    translated_text = completion.choices[0].message.content

    translated_text = translated_text[translated_text.find("[[") + 1:translated_text.find("]]")]

    return translated_text
