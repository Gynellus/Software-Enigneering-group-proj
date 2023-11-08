import openai
from check import convert_input_to_string

openai.api_key = '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'

article = convert_input_to_string(input("Give either file location or website"))

def summarize(artikel):
    openai.api_key = openai.api_key
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You summarize papers"},
            {"role": "user", "content": f"Summarize the paper {artikel}"},
        ]
    )
    output = completion['choices'][0]['message']['content']
    return output

    return response.choices[0].text.strip()

file_path = "C:\\Users\\aleks\\OneDrive\\Dokumenty\\Internship_NC\\papers\\science.1239918.pdf"

summary = summarize(artikel = article)
print(summary)

