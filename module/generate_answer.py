import openai

openai.api_key = ""


def generate_answer(query):
    prompt = f"{query}\n\nIf the answer to the above question is not contained within the provided context, please respond with 'I don't know'."
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3.5 Turbo engine
        prompt=prompt,
        temperature=0.3,
        max_tokens=70,  # Adjust max_tokens as needed
        n=1,
        stop=None,  # You can set stop words to limit the response if desired
    )

    answer = response.choices[0].text.strip()
    return answer
