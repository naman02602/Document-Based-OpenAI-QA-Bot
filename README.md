# Assignment_03

Link to the application:

[Codelab](https://codelabs-preview.appspot.com/?file_id=1lr0TH95fZP92NavnkxypWGXS7bmKC_0a4mSmTC1rKjw#0)

[Demo](https://youtu.be/64ymF6XK77U)

# Problem Statement:

This project's primary challenge is to automate the creation of embeddings and populate a vector database using Airflow pipelines. It involves data acquisition, processing, and insertion into Pinecone's vector database. Additionally, the development of a client-facing application using FastAPI and Streamlit is crucial, featuring user registration, secure login, a Question Answering interface, and the ability to select and search preprocessed forms. The goal is to deploy all microservices to a public cloud platform for public accessibility, offering a comprehensive and user-friendly solution. We also tested multiple scenarios of users experimenting Q/A with the OpenAI bot on Streamlit. 



# Architecture Diagram:

![Architecture diagram](https://github.com/BigDataIA-Fall2023-Team4/Assignment_03/assets/50952018/c22f84a6-5f3b-401b-a169-ae0f5949ea3e)



# Technologies Used:

1. GitHub
2. Python
3. Fast API
4. Google Cloud Storage
5. Google Cloud SQL
6. Google Compute Engine
7. Docker
8. Airflow
9. Streamlit
10. Pinecone

# Major Libraries Used:

1. Pypdf
2. Nougat
3. Open AI
4. TikToken
5. Local Tunnel
6. Diagrams
7. Uvicorn
8. JWT Tokens
9. Python-Jose

# Data Source:

SEC forms: [https://www.sec.gov/forms](https://www.sec.gov/forms)

# Project Structure:



# Team Contribution:

| Name            | Contribution % | Contributions |
|-----------------|----------------|---------------|
| Naman Gupta     |     33.3%      |    Q/A Bot, Embeddings Generation, Pinecone, Readme.md, Codelab, Pipeline 1, Google Cloud Storage         |
| Jagruti Agrawal |     33.3%      |     Docker containers for each microservices, Pipeline 2, Diagram, Codelab         |
| Divyesh Rajput  |     33.3%      |    Streamlit Application, FastAPI, JWT Tokens, Pipeline 1, Logging, VM Instance           |
