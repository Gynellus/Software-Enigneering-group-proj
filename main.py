import openai
from convert import convert_input_to_string
openai.api_key = 'XXX'

artikel = convert_input_to_string(input("Give either file location or website"))

def summarize(artikel):
    openai.api_key = openai.api_key
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {"role": "system", "content": "You summarize papers"},
            {"role": "user", "content": f"Summarize the paper {artikel}"},
        ]
    )
    output = completion['choices'][0]['message']['content']
    return output

    return response.choices[0].text.strip()

summary = summarize(artikel=artikel)
print(summary)