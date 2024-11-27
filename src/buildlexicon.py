import json #import the json library to use it for lexicon formation
from collections import Counter# import the collections to user library counter to use it for frequency counting
from nltk.corpus import stopwords#this library has all the stop words that ought to be removed from lexicon
from nltk.stem import WordNetLemmatizer#we used this library to add lemmatization

# Define file paths
LEXICON_FILE = "../data/lexicon.json"#declared a lexicon file so that if the file exists whenever the code is run 
#it just updates the code
cleaned_file_name = "../data/cleaned_jokes_dataset.csv"

#  Load existing lexicon if it exists
try:
    with open(LEXICON_FILE, "r") as file:
        lexicon_data = json.load(file)
        lexicon = set(lexicon_data["words"])
        word_frequencies = Counter(lexicon_data["frequencies"])
except FileNotFoundError:
    lexicon = set()
    word_frequencies = Counter()

#  Load your preprocessed dataset
with open(cleaned_file_name, "r") as file:
    data = file.readlines()

#  Initialize NLTK tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

#  Process the dataset and update the lexicon
for line in data:
    words = line.strip().split()
    for word in words:
        word = word.lower()  # Normalize to lowercase
        word = lemmatizer.lemmatize(word)  # Lemmatize the word
        if word not in stop_words:  # Exclude stop words
            lexicon.add(word)
            word_frequencies[word] += 1

#  Save updated lexicon to the JSON file
lexicon_data = {
    "words": list(lexicon),
    "frequencies": dict(word_frequencies)
}
with open(LEXICON_FILE, "w") as file:
    json.dump(lexicon_data, file, indent=4)

#  Output statistics
print(f"Total unique words in lexicon: {len(lexicon)}")
print(f"Sample lexicon entries: {list(lexicon)[:10]}")
print(f"Word frequencies sample: {dict(list(word_frequencies.items())[:10])}")
