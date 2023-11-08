import os
import json
import numpy as np
import PyPDF2
import tensorflow_hub as hub

# Function to open a file and read its content
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Function to calculate cosine similarity between two vectors
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdffileobj:
        pdfreader = PyPDF2.PdfReader(pdffileobj)
        paper = ''
        for i in range(len(pdfreader.pages)):
            pageobj = pdfreader.pages[i]
            paper += pageobj.extract_text()
    return paper

# Generator function to load embeddings one by one to save memory
def load_embeddings(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                article = json.load(f)
                yield article['embedding'], article

if __name__ == '__main__':
    # Load Universal Sentence Encoder
    embed = hub.load('https://tfhub.dev/google/universal-sentence-encoder-large/5')

    # Extract text from PDFs in the 'pdfs/' directory
    pdf_files = [f for f in os.listdir('pdfs/') if f.endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join('pdfs/', pdf_file)
        paper_text = extract_text_from_pdf(pdf_path)
        
        # Embedding for the extracted text
        paper_embedding = embed([paper_text]).numpy()

        # Initialize list to store similarities and corresponding articles
        similarities = []
        articles = []

        # Load and compare each embedding
        for embedding, article in load_embeddings('Data/similarity_finder_Data/'):
            sim = cosine_similarity(paper_embedding[0], embedding)
            similarities.append(sim)
            articles.append(article)

        # Get the top 5 most similar articles
        top_indices = np.argsort(similarities)[-5:][::-1]
        top_articles = [articles[idx] for idx in top_indices]
        top_similarities = [similarities[idx] for idx in top_indices]

        # Display results
        print(f"Top 5 similar articles for {pdf_file}:")
        for article, similarity in zip(top_articles, top_similarities):
            print(f"ID: {article['id']}, Similarity: {similarity:.4f}, Title: {article['title']}")