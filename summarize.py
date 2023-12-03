import os

import openai

def summarize(article):
    if not article:
        raise ValueError("Input text cannot be empty.")
    # Load OpenAI API key
    if 'openai_API_key.txt' not in os.listdir():
        raise Exception("Please add your OpenAI API key to openai_API_key.txt to the main directory of this project.")
    with open('openai_API_key.txt', 'r') as f:
        openai.api_key = f.read()

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
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize academic papers or sections of papers"},
                {"role": "user", "content": f"Summarize the following: {section}"},
            ]
        )
        summary += completion.choices[0].message.content + "\n\n"

    # If there was more than one section, summarize the summary
    if len(sections) > 1:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize academic papers or sections of papers"},
                {"role": "user", "content": f"Summarize the paper: {summary}"},
            ]
        )
        summary = completion.choices[0].message.content

    return summary

print(summarize("pdfs/The_Role_of_Emotions_in_Reading_Literary.pdf"))