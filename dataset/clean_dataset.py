import pandas as pd
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem import WordNetLemmatizer

# File paths
input_file = r"C:\Users\AT\CSV Dataset files\test.csv"
output_file = r"C:\Users\AT\CSV Dataset files\cleaned_articles_test.csv"

# Load the dataset
df = pd.read_csv(input_file)

# Check for required columns
required_columns = ['title', 'text', 'tags']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Remove duplicates and NaN values
df = df.drop_duplicates().dropna()

# Process the 'tags' column
def process_tags(tags_text):
    tags = tags_text[1:-1].split(", ")
    tags = [w[1:-1] for w in tags]
    return " ".join(tags)

df['tags_text'] = df['tags'].apply(process_tags)

# Merge text data
df["merged_text"] = df["title"] + " " + df["text"] + " " + df["tags_text"]

# Keep only the merged text column
merged_text_df = df[["merged_text"]]

# Remove duplicates and reset index
merged_text_df.drop_duplicates(inplace=True)
merged_text_df.reset_index(drop=True, inplace=True)

# Clean special characters, numerics, and convert text to lowercase
def clean_characters(text):
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numerics
    text = text.lower()  # Convert to lowercase
    return text

merged_text_df["merged_text"] = merged_text_df["merged_text"].apply(clean_characters)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Clean text by removing stopwords, lemmatizing, and ensuring unique words
def clean_stop_words_and_make_unique(text):
    if not isinstance(text, str):
        return ""
    tokens = text.split()
    clean_list = {
        lemmatizer.lemmatize(word)  # Lemmatize each word
        for word in tokens
        if word not in ENGLISH_STOP_WORDS and word.isalpha()  # Remove stopwords and non-alphabetic tokens
    }
    return " ".join(sorted(clean_list))  # Join sorted unique words

# Apply text cleaning
merged_text_df["cleaned_text"] = merged_text_df["merged_text"].apply(clean_stop_words_and_make_unique)

# Save cleaned data to a CSV file
merged_text_df[["cleaned_text"]].to_csv(output_file, index=False)

print(f"Cleaned dataset saved to {output_file}")
