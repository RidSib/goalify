import weaviate
import weaviate.classes.query as wq
import os


# Instantiate your client (not shown). e.g.:
headers = {"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}
client = weaviate.connect_to_local( headers=headers)

# Get the collection
movies = client.collections.get("Book")

# print(movies)
# Perform query
query = "What is the main character of the book?"
response = movies.query.near_text(
    query="dystopian future", limit=5, return_metadata=wq.MetadataQuery(distance=True)
)

# Inspect the response
for o in response.objects:
    print(
        o.properties["text"], o.properties["chunk_id"]
    )  # Print the title and release year (note the release date is a datetime object)
    print(
        f"Distance to query: {o.metadata.distance:.3f}\n"
    )  # Print the distance of the object from the query

client.close()