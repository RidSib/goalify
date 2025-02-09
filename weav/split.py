import pandas as pd

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=200, overlap=20):
    words = text.split()  # Split text into words
    chunks = []
    
    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]  # Take 200 words
        chunks.append(" ".join(chunk))  # Convert list back to string
        i += chunk_size - overlap  # Move ahead with overlap
    
    return chunks

# Read the file
with open("ah.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Split the text into chunks
chunks = split_text_into_chunks(text)

# Create a DataFrame
df = pd.DataFrame({"Chunk ID": range(1, len(chunks) + 1), "Text": chunks})

# Display first few rows
print(df.head())

# Save as CSV (optional)
df.to_csv("text_chunks.csv", index=False)
