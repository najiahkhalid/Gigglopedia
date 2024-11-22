import pandas as pd
import re

# Load the dataset
file_name = 'jokes_dataset.csv'
df = pd.read_csv(file_name)

# Inspect the dataset
print("Dataset Information:")
print(df.info())
print("\nSample Data:")
print(df.head())

# Step 1: Handle Missing Values
df = df.dropna(subset=['text'])  # Drop rows with missing values in 'text' only

# Step 2: Remove Duplicates
df = df.drop_duplicates()

# Step 3: Clean Text Columns
def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)  # Remove anything within < >
    
    # Remove emojis and non-English characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    
    # Remove trailing commas and numbers at the end of sentences
    text = re.sub(r'[,\d]+\s*$', '', text)  # Remove trailing commas and numbers (with optional space)
    
    # Remove all commas globally
    text = re.sub(r',', '', text)  # Remove all commas in the text
    
    # Remove the letter 'Q' at the start of the text
    text = re.sub(r'^\s*Q\s*', '', text, flags=re.IGNORECASE)  # Remove 'Q' at the start
    
    # Fix joined words (camel case or words joined with numbers)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space before capital letters
    text = re.sub(r'([a-zA-Z])(\d+)', r'\1 \2', text)  # Separate words from numbers
    text = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', text)  # Separate numbers from words
    
    # Remove all other punctuation marks except for spaces
    text = re.sub(r'[^\w\s]', '', text)
    
    # Ensure no extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Capitalize the first letter of each sentence
    sentences = text.split('. ')
    sentences = [s.capitalize() for s in sentences]  # Capitalize first letter
    text = '. '.join(sentences)
    
    return text

# Apply the cleaning function to the 'text' column
if 'text' in df.columns:
    df['text'] = df['text'].apply(clean_text)
else:
    print("Error: 'text' column is missing in the dataset")

# Step 4: Remove Extreme Data Points (Optional: Based on Lengths)
df['lengths'] = df['text'].apply(len)  # Add a 'lengths' column
df = df[df['lengths'] < df['lengths'].quantile(0.95)]  # Keep rows below 95th percentile

# Step 5: Save the Cleaned Dataset
cleaned_file_name = 'cleaned_jokes_dataset.csv'
df.to_csv(cleaned_file_name, index=False)
print(f"Cleaned dataset saved as {cleaned_file_name}")
