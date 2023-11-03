import os
import json
import numpy as np
import PyPDF2
import tensorflow_hub as hub
import textwrap
from tqdm import tqdm

# Provided functions
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdffileobj:
        pdfreader = PyPDF2.PdfReader(pdffileobj)
        paper = ''
        for i in range(len(pdfreader.pages)):
            pageobj = pdfreader.pages[i]
            paper += pageobj.extract_text()
    return paper

# Load precomputed embeddings and their corresponding article metadata
def load_embeddings(directory):
    embeddings = []
    articles = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                article = json.load(f)
                articles.append(article)
                embeddings.append(article['embedding'])
    return articles, np.array(embeddings)

if __name__ == '__main__':
    # Load Universal Sentence Encoder
    embed = hub.load('https://tfhub.dev/google/universal-sentence-encoder-large/5')

    # Extract text from PDFs in the 'pdfs/' directory
    pdf_files = [f for f in os.listdir('pdfs/') if f.endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join('pdfs/', pdf_file)
        paper_text = extract_text_from_pdf(pdf_path)
        
        # Diagnostic print for paper_text
        print("Extracted Paper Text (first 500 chars):")
        print(textwrap.shorten(paper_text, 500))
        
        # Create an embedding for the extracted text
        paper_embedding = embed([paper_text]).numpy()

        # Load the precomputed embeddings
        articles, embeddings = load_embeddings('Data/embeddings')

        # Compute the cosine similarity 
        similarities = []
        for e in tqdm(embeddings):
            sim = cosine_similarity(paper_embedding[0], e) 
            similarities.append(sim)
        
        # Diagnostic prints for similarities
        print(f"Similarities Min: {np.min(similarities)}, Max: {np.max(similarities)}, Mean: {np.mean(similarities)}")
        
        # Compute the cosine similarity 
        similarities = []
        for e in tqdm(embeddings):
            sim = cosine_similarity(paper_embedding[0], e)
            similarities.append(sim)

        # Get the top 5 most similar articles
        top_indices = np.argsort(similarities)[-5:][::-1]
        top_articles = []
        top_similarities = []
        for idx in top_indices.tolist():
            top_articles.append(articles[idx])
            top_similarities.append(similarities[idx])

        # Display results
        print(f"Top 5 similar articles for {pdf_file}:")
        for article, similarity in zip(top_articles, top_similarities):
            print(f"ID: {article['id']}, Similarity: {similarity:.4f}, Title: {article['title']}")