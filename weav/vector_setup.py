import weaviate

import weaviate.classes.config as wc
import os
import pandas as pd
import requests
import tqdm
import json
from weaviate.util import generate_uuid5
from weaviate.classes.init import Auth
from dotenv import load_dotenv

load_dotenv()
# Best practice: store your credentials in environment variables
wcd_url = os.getenv("WCD_URL")
wcd_api_key = os.getenv("WCD_API_KEY")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,                                    # Replace with your Weaviate Cloud URL
    auth_credentials=Auth.api_key(wcd_api_key),             # Replace with your Weaviate Cloud key
    headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")},           # Replace with your Cohere API key
)
class_name = "Book"

client.collections.create(
    name=class_name,
    properties=[
        wc.Property(name="text", data_type=wc.DataType.TEXT),
        wc.Property(name="chunk_id", data_type=wc.DataType.INT),
    ],
    # Define the vectorizer module
    vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
    # Define the generative module
    generative_config=wc.Configure.Generative.openai()
)


df = pd.read_csv("text_chunks.csv")
ids = df["Chunk ID"].tolist()
content = df["Text"].tolist()
# Get the collection
books = client.collections.get(class_name)

# Enter context manager
with books.batch.dynamic() as batch:
    # Loop through the data
    for i in range(len(ids)):
 
        # Convert a JSON array to a list of integers
        # Build the object payload
        book_obj = {
            "text": content[i],
            "chunk_id": ids[i],
        }

        # Add object to batch queue
        batch.add_object(
            properties=book_obj,
            uuid=generate_uuid5(ids[i])
            # references=reference_obj  # You can add references here
        )
        # Batcher automatically sends batches

# Check for failed objects
if len(books.batch.failed_objects) > 0:
    print(f"Failed to import {len(books.batch.failed_objects)} objects")

client.close()