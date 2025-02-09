import weaviate
from weaviate.classes.init import Auth
import os
from dotenv import load_dotenv

load_dotenv()

wcd_url = os.getenv("WCD_URL")
wcd_api_key = os.getenv("WCD_API_KEY")
cohere_api_key = os.getenv("COHERE_APIKEY")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,
    auth_credentials=Auth.api_key(wcd_api_key),
    headers={"X-Cohere-Api-Key": cohere_api_key},
)

# Delete the existing collection if it exists
try:
    client.collections.delete("Question")
    print("Deleted existing 'Question' collection.")
except Exception as e:
    print(f"Error deleting collection: {e}")

client.close()