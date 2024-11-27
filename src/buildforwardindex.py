import json  # Import the json library to use it for storing the forward index
import csv
import nltk
from nltk.corpus import stopwords  # This library has all the stop words that ought to be removed from the index
from nltk.stem import WordNetLemmatizer  # Used for lemmatization of words

# Initialize NLTK tools
nltk.download('stopwords')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Define file paths
FORWARD_INDEX_FILE = "../data/forward_index.json"  # Forward index file path
cleaned_file_name = "../data/cleaned_jokes_dataset.csv"  # File path for preprocessed dataset

#  Load the existing forward index if it exists
try:
    with open(FORWARD_INDEX_FILE, "r") as file:
        forward_index_data = json.load(file)
        forward_index = forward_index_data["index"]
except (FileNotFoundError, KeyError):
    forward_index = {}  # If the file does not exist or the key is missing, start with an empty index

#  Load your preprocessed dataset
with open(cleaned_file_name, "r") as file:
    data = file.readlines()

#  Process the dataset and create the forward index
for doc_id, line in enumerate(data, start=len(forward_index)):
    words = line.strip().split()  # Split the line into words
    processed_words = set()  # To store unique words for the current document

    for word in words:
        word = word.lower()  # Normalize to lowercase
        word = lemmatizer.lemmatize(word)  # Lemmatize the word
        if word not in stop_words:  # Exclude stop words
            processed_words.add(word)  # Add the word to the set for this document

    # Add the processed words for this document to the forward index
    forward_index[doc_id] = list(processed_words)

#  Save the forward index to a JSON file
forward_index_data = {
    "index": forward_index  # The forward index with doc IDs as keys and word lists as values
}

with open(FORWARD_INDEX_FILE, "w") as file:
    json.dump(forward_index_data, file, indent=4)

#  Output statistics
print(f"Total documents indexed: {len(forward_index)}")
print(f"Sample forward index entries: {list(forward_index.items())[:5]}")