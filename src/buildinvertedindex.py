import json  # To load and save data
from collections import defaultdict  # To easily create and append to lists

# Define file paths
FORWARD_INDEX_FILE = "./data/forward_index.json"  # Path to forward index
INVERTED_INDEX_FILE = "./data/inverted_index.json"  # Output path for inverted index

# Load the forward index
with open(FORWARD_INDEX_FILE, "r") as file:
    forward_index_data = json.load(file)
    forward_index = forward_index_data["index"]

# Initialize the inverted index as a defaultdict of lists
inverted_index = defaultdict(list)

# Build the inverted index
for doc_id, words in forward_index.items():
    for word in words:
        inverted_index[word].append(doc_id)  # Map each word to the corresponding doc_id

# Convert defaultdict to a regular dict for saving
inverted_index = dict(inverted_index)

# Save the inverted index to a JSON file
with open(INVERTED_INDEX_FILE, "w") as file:
    json.dump(inverted_index, file, indent=4)

# Output statistics
print(f"Total unique terms in the inverted index: {len(inverted_index)}")
print(f"Sample inverted index entries: {list(inverted_index.items())[:5]}")
