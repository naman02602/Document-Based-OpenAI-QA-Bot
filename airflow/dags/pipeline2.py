import os
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import timedelta
import pandas as pd
import time
import glob
import pinecone
from google.cloud import storage
import io
from airflow.models import Variable

index = None 

dag_directory = os.path.dirname(os.path.abspath(__file__))
keyfile_path = os.path.join(dag_directory, 'deft-scout-403222-2fb0d39d8a65.json')

storage_client = storage.Client.from_service_account_json(keyfile_path)

# Specify the GCS bucket and the object (file) path
bucket_name = 'damg7245_qa_bot'
object_name = 'embeddings.csv'

def convert_string_to_list(embedding_str):
    return [float(item) for item in embedding_str.strip("[]").split(",")]

def read_embeddings():
    # Get a reference to the bucket
    bucket = storage_client.get_bucket(bucket_name)
    # Get a reference to the object (file) you want to read
    blob = bucket.blob(object_name)
    data = blob.download_as_string()
    df = pd.read_csv(io.BytesIO(data))

    # Now you can work with the data in the DataFrame
    print(df.head())

    df['embeddings'] = df['embeddings'].apply(convert_string_to_list)
    df['id'] = df['form_title'] + '_' + df.index.astype(str)
    return df

def create_index(index_name = "damg7245-qabot"):
    global index  # Access the global index variable
    if index is None:
        pinecone.init(api_key=Variable.get('pinecone_api_key'), environment='gcp-starter')
        index = pinecone.Index(index_name='damg7245-qabot')
    
    # Delete index if exists
    if index_name in pinecone.list_indexes():
        pinecone.delete_index(index_name)

    # Create index
    pinecone.create_index(name=index_name, dimension=1536, metric="cosine")

    # wait for index to be ready before connecting
    while not pinecone.describe_index(index_name).status['ready']:
        time.sleep(1)

def validate_insert(df,index_status):
    total_vector_count = index_status["upserted_count"]
    if len(df) != total_vector_count:
        raise ValueError(f"Total Embeddings in data ({len(df)}) does not match the expected \
         vector count ({total_vector_count}) in Pinecone database.")



def insert_vectors(**kwargs):
    global index  # Access the global index variable
    if index is None:
        pinecone.init(api_key=Variable.get('pinecone_api_key'), environment='gcp-starter')
        index = pinecone.Index(index_name='damg7245-qabot')

    ti = kwargs["ti"]
    df = ti.xcom_pull(task_ids="embeddings_read")

    meta = [{
            'form_title': x[0],
            'form_url': x[1],
            'context': x[2]
        } for x in zip(
            df['form_title'],
            df['form_url'],
            df['context']
        )]

    print("Meta Data", meta)

    # Upsert the vectors
    index_status = index.upsert(vectors=zip(df["id"], df["embeddings"],meta))
    try:
        validate_insert(df,index_status)
        print("DataFrame length is valid.")
    except ValueError as e:
        print(f"Validation error: {e}")
        

dag = DAG(
    dag_id="store_embeddings_in_pinecone",
    schedule="0 0 * * *",   # https://crontab.guru/
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["embeddings", "pinecone"],
)

with dag:
    embeddings_read = PythonOperator(
        task_id='embeddings_read',
        python_callable=read_embeddings,
        provide_context=True,
        dag=dag,
    )

    index_creation = PythonOperator(
        task_id='index_creation',
        python_callable=create_index,
        provide_context=True,
        dag=dag,
    )

    vectors_insertion = PythonOperator(
        task_id='vectors_insertion',
        python_callable=insert_vectors,
        provide_context=True,
        dag=dag,
    )

    embeddings_read >> index_creation >> vectors_insertion