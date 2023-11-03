import requests
from io import BytesIO
from PyPDF2 import PdfReader
import pandas as pd
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.param import Param
from pdf_utils import (
    generate_embeddings,
    fetch_pdf_from_url,
    parse_pdf_with_pypdf,
    split_context_to_rows,
    parse_pdf_with_nougat,
)
import yaml
import openai
import os
from airflow.models import Variable
from google.cloud import storage
from airflow.hooks.base_hook import BaseHook

# Access the Google Cloud connection
dag_directory = os.path.dirname(os.path.abspath(__file__))
keyfile_path = os.path.join(dag_directory, 'deft-scout-403222-2fb0d39d8a65.json')

storage_client = storage.Client.from_service_account_json(keyfile_path)

# Define data and bucket details
bucket_name = 'damg7245_qa_bot'
object_name = 'embeddings.csv'

# Define the user input parameters
user_input = {
    "pdf_urls": Param(default="https://www.sec.gov/files/form1-e.pdf,https://www.sec.gov/files/form1-k.pdf,https://www.sec.gov/files/form1-n.pdf,https://www.sec.gov/files/form1-sa.pdf,https://www.sec.gov/files/form1-z.pdf", type="string"),
    "processing_library": Param(default="PyPdf", type="string"),
    "api_address": Param(default="", type="string"),
}

# Task to extract parameters
def extract_parameters(**kwargs):
    ti = kwargs["ti"]
    params = kwargs["dag_run"].conf
    pdf_urls = params["pdf_urls"].split(",")  # Split the string into a list of URLs
    processing_library = params["processing_library"]
    api_address = params["api_address"]
    ti.xcom_push(
        key="params", value={"pdf_urls": pdf_urls, "processing_library": processing_library, "api_address": api_address}
    )


def download_and_parse_pdfs(**kwargs):
    ti = kwargs["ti"]
    params = ti.xcom_pull(task_ids="extract_parameters", key="params")
    pdf_urls = params.get("pdf_urls", [])
    processing_library = params.get("processing_library", "")
    api_address = params.get("api_address", "")
    data_dict = {"context": [], "form_url": []}

    print("Processing library", processing_library)

    for url in pdf_urls:
        if processing_library == "PyPdf":
            # Use 'fetch_pdf_from_url' to fetch the PDF content from the provided URL and store in memory
            print("URLs", url)
            pdf_in_memory = fetch_pdf_from_url(url)
            # Use 'parse_pdf_with_pypdf' to parse the content of the PDF and store the parsed content in a string variable.
            pdf_content = parse_pdf_with_pypdf(pdf_in_memory)
            # Append the token count and the content of the current paragraph to the data dictionary
            data_dict["context"].append(pdf_content)
            data_dict["form_url"].append(url)
            print("Data Dict", data_dict["form_url"])
        elif processing_library == "Nougat":
            print("In here")
            print("API address", api_address)
            pdf_content = parse_pdf_with_nougat(url, api_address)
            print("Pdf content", len(pdf_content))
            data_dict["context"].append(pdf_content)
            data_dict["form_url"].append(url)
        else:
            print('Please provide valid parsing library')

    # Convert the parsed_texts_dict to a DataFrame
    df = pd.DataFrame(data_dict)
    df["form_title"] = df["form_url"].str.split("/").str[-1]

    df_sec = split_context_to_rows(df, 1000)

    # For testing, print the first few rows of the df_sec DataFrame
    print(df_sec.head())
    # ti.xcom_push(key="parsed_pdf_data", value=df_sec.to_dict(orient="records"))
    ti.xcom_push(key="parsed_pdf_data", value=df_sec)


def load_openai_api_key(**kwargs):
    openai_api_key = Variable.get("openai_api_key")
    return openai_api_key


def generate_embeddings_for_dataframe(**kwargs):
    openai.api_key = load_openai_api_key(**kwargs)

    # Fetch the parsed PDF data from the previous task
    ti = kwargs["ti"]

    # parsed_data = ti.xcom_pull(task_ids="download_and_parse_pdfs")
    df_sec = ti.xcom_pull(task_ids="download_and_parse_pdfs", key="parsed_pdf_data")

    # Apply the 'generate_embeddings' function to each row in the 'content' column of the DataFrame 'df'
    df_sec["embeddings"] = df_sec["context"].apply(generate_embeddings)

    # Push the dataframe with embeddings to XCom for further tasks or save it as needed
    ti.xcom_push(key="data_with_embeddings", value=df_sec.to_dict(orient="records"))


def save_to_csv(**kwargs):
    # Fetch the DataFrame with embeddings from XCom
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="generate_embeddings", key="data_with_embeddings")
    df_sec = pd.DataFrame(data)

    # Write DataFrame to Google Cloud Storage
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(df_sec.to_csv(index=False), content_type='text/csv')


# DAG definition
dag = DAG(
    "pdf_processing_dag",
    default_args={
        "owner": "you",
        "start_date": datetime(2023, 10, 28),
        "retries": 1,
    },
    description="A DAG to process PDFs and generate embeddings",
    schedule=None,  # No set schedule, will be triggered manually
    catchup=False,
    params=user_input,
)

with dag:
    extract_parameters_task = PythonOperator(
        task_id="extract_parameters",
        python_callable=extract_parameters,
        provide_context=True,
        dag=dag,
    )

    # Task to download, parse PDFs, and create DataFrame
    download_parse_task = PythonOperator(
        task_id="download_and_parse_pdfs",
        python_callable=download_and_parse_pdfs,
        provide_context=True,
        dag=dag,
    )

    generate_embeddings_task = PythonOperator(
        task_id="generate_embeddings",
        python_callable=generate_embeddings_for_dataframe,
        provide_context=True,
        dag=dag,
    )

    save_to_csv_task = PythonOperator(
        task_id="save_to_csv",
        python_callable=save_to_csv,
        provide_context=True,
        dag=dag,
    )


# Task dependencies
(
    extract_parameters_task
    >> download_parse_task
    >> generate_embeddings_task
    >> save_to_csv_task
)
