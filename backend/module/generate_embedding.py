import openai

openai.api_key = "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"
EMBEDDING_MODEL = "text-embedding-ada-002"


def generate_embedding(question: str):
    # Create embeddings for the given 'question' using the specified EMBEDDING_MODEL
    response = openai.Embedding.create(model=EMBEDDING_MODEL, input=question)

    # Extract the embeddings from the API response
    return response["data"][0]["embedding"]
