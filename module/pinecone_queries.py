import pinecone

pinecone_api_key = ""
pinecone.init(api_key=pinecone_api_key)


def query_pinecone(query, top_k, selected_pdfs=None):
    pinecone_api_key = ""
    pinecone.init(api_key=pinecone_api_key, environment="gcp-starter")
    index = pinecone.Index(index_name="damg7245-qabot")

    # Prepare the filter condition
    if selected_pdfs:
        filter_condition = {"form_title": {"$eq": "form1-e.pdf"}}

        filter_conditions = [{"form_title": {"$eq": pdf}} for pdf in selected_pdfs]
        # Combine the filter condition dictionaries with an OR operation
        filter_condition = {"$or": filter_conditions}

        # Execute the query with the filter condition
        results = index.query(
            query, top_k=top_k, include_metadata=True, filter=filter_condition
        )
    else:
        # If no PDFs are selected, execute the query without a filter condition
        results = index.query(query, top_k=top_k, include_metadata=True)

    return results


def format_query(query, context):
    # extract passage_text from Pinecone search result and add the  tag
    context = [f" {m['metadata']['context']}" for m in context]
    # concatinate all context passages
    context = " ".join(context)
    # concatenate the query and context passages
    query = f"question: {query} context: {context}"
    return query
