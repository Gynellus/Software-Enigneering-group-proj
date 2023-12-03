import os
import json
import numpy as np
import tensorflow_hub as hub

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

    # Load and compare each embedding
    for embedding, article in load_embeddings('Data/similarity_finder_Data/'):
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
        url = f"https://arxiv.org/pdf/{article['id']}.pdf"
        results.append(f"URL: {url}, Similarity: {similarity:.4f}, Title: {article['title']}")

    return results

# Example usage
# similar_papers = find_similar_papers("Ion acceleration from gaseous targets driven by relativistic-intensity lasers was demonstrated as early as the late 90s, yet most of the experiments conducted to date have involved picosecond-duration, Nd:glass lasers operating at low repetition rate. Here, we present measurements on the interaction of ultraintense (∼1020Wcm−2, 1 PW), ultrashort (∼70fs) Ti:Sa laser pulses with near-critical (∼1020cm−3) helium gas jets, a debris-free targetry compatible with high (∼1Hz) repetition rate operation. We provide evidence of α particles being forward accelerated up to ∼2.7MeV energy with a total flux of ∼1011sr−1 as integrated over >0.1MeV energies and detected within a 0.5mrad solid angle. We also report on on-axis emission of relativistic electrons with an exponentially decaying spectrum characterized by a ∼10MeV slope, i.e., five times larger than the standard ponderomotive scaling. The total charge of these electrons with energy above 2 MeV is estimated to be of ∼1nC, corresponding to ∼0.1% of the laser drive energy. In addition, we observe the formation of a plasma channel, extending longitudinally across the gas density maximum and expanding radially with time. These results are well captured by large-scale particle-in-cell simulations, which reveal that the detected fast ions most likely originate from reflection off the rapidly expanding channel walls. The latter process is predicted to yield ion energies in the MeV range, which compare well with the measurements. Finally, direct laser acceleration is shown to be the dominant mechanism behind the observed electron energization.")
# for paper in similar_papers:
#     print(paper)
