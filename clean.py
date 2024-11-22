import pandas as pd
import re
import os

# File names
raw_file_name = "jokes_dataset.csv"
cleaned_file_name = "cleaned_jokes_dataset.csv"

# Step 1: Load the raw dataset
raw_df = pd.read_csv(raw_file_name)

# Step 2: Check if the cleaned dataset already exists
if os.path.exists(cleaned_file_name):
    cleaned_df = pd.read_csv(cleaned_file_name)
    # Merge datasets, avoiding duplicates
    merged_df = pd.concat([cleaned_df, raw_df]).drop_duplicates()
else:
    merged_df = raw_df

# Step 3: Handle missing values
merged_df = merged_df.dropna(subset=["text"])  # Drop rows where 'text' is missing

# Step 4: Text cleaning function
def clean_text(text):
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    text = re.sub(r'[,\d]+\s*$', '', text)  # Remove trailing commas and numbers
    text = re.sub(r',', '', text)  # Remove all commas
    text = re.sub(r'^\s*Q\s*', '', text, flags=re.IGNORECASE)  # Remove leading 'Q'
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Split camel case
    text = re.sub(r'([a-zA-Z])(\d+)', r'\1 \2', text)  # Separate letters from numbers
    text = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', text)  # Separate numbers from letters
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation except spaces
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    # Capitalize sentences
    sentences = text.split('. ')
    sentences = [s.capitalize() for s in sentences]
    text = '. '.join(sentences)
    return text

# Step 5: Apply cleaning function
if "text" in merged_df.columns:
    merged_df["text"] = merged_df["text"].apply(clean_text)
else:
    raise ValueError("Error: 'text' column is missing in the dataset")

# Step 6: Remove extreme data points (optional, based on lengths)
merged_df["lengths"] = merged_df["text"].apply(len)
merged_df = merged_df[merged_df["lengths"] < merged_df["lengths"].quantile(0.95)]
merged_df = merged_df.drop(columns=["lengths"])  # Drop the temporary 'lengths' column

# Step 7: Save updated cleaned dataset
merged_df.to_csv(cleaned_file_name, index=False)
print(f"Cleaned dataset updated and saved as {cleaned_file_name}")
print(f"Total records in cleaned dataset: {len(merged_df)}")
