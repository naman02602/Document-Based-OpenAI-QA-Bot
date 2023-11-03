import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_answer(query):
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3.5 Turbo engine
        prompt=query,
        temperature=0,
        max_tokens=512, 
        frequency_penalty=0.1,
        presence_penalty=0.1,
        n=1,
        stop=None,  # You can set stop words to limit the response if desired
    )

    answer = response.choices[0].text.strip()
    return answer
