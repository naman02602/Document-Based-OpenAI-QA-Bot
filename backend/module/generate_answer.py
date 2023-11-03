import openai

openai.api_key = "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"


def generate_answer(query):
    prompt = f"{query}\n\nYou should answer questions based on the context provided. If the question is completely irrelevant to the context, answer with I don't know and if the question is similar to the context, then try to answer it with the provided context only. The answer should be limited to 80 tokens only with making the answer complete."
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3.5 Turbo engine
        prompt=prompt,
        temperature=0.7,
        n=1,
        stop=None,  # You can set stop words to limit the response if desired
    )

    answer = response.choices[0].text.strip()
    return answer
