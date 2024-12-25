import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import unicodedata
from joblib import Parallel, delayed

# Ensure necessary NLTK resources are available
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

class DatasetCleaner:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.lemmatizer = WordNetLemmatizer()

    def _normalize_text(self, text):
        # Normalize text (e.g., remove non-ASCII characters)
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').lower().strip()

    def _remove_urls_and_special_chars(self, text):
        # Remove URLs, special characters, and numbers
        text = re.sub(r'http[s]?://\S+', '', text)  # Remove URLs
        text = re.sub(r'[^\w\s]', '', text)        # Remove special characters
        text = re.sub(r'\d+', '', text)            # Remove numbers
        text = re.sub(r'\s+', ' ', text).strip()    # Remove extra whitespace
        return text

    def _preprocess_text(self, text):
        # Tokenize, remove stop words, and lemmatize
        tokens = word_tokenize(text)
        return ' '.join(
            sorted(set(self.lemmatizer.lemmatize(word.lower()) for word in tokens 
                        if word.isalpha() and word.lower() not in ENGLISH_STOP_WORDS))  # Only keep alphabetic words
        )

    def clean_chunk(self, df_chunk):
        # Apply text cleaning steps to each chunk of data
        df_chunk['title'] = df_chunk['title'].apply(self._normalize_text)
        df_chunk['text'] = df_chunk['text'].apply(self._remove_urls_and_special_chars)
        df_chunk['tags_text'] = df_chunk['tags'].apply(self._normalize_text)
        # Combine title, text, and tags and apply preprocessing
        df_chunk['cleaned_text'] = (df_chunk['title'] + " " + df_chunk['text'] + " " + df_chunk['tags_text']).apply(self._preprocess_text)
        return df_chunk[['title', 'url', 'tags', 'cleaned_text']]  # Only retain essential columns

    def clean_dataset(self):
        try:
            # Load dataset in chunks to avoid high memory usage
            chunk_size = 50000  # Adjust as necessary
            chunks = pd.read_csv(self.input_file, chunksize=chunk_size)

            # Process the dataset in parallel using multiple jobs
            processed_chunks = Parallel(n_jobs=-1)(delayed(self.clean_chunk)(chunk) for chunk in chunks)

            # Concatenate all processed chunks into one DataFrame
            df_cleaned = pd.concat(processed_chunks, ignore_index=True)

            # Save the cleaned dataset
            df_cleaned.to_csv(self.output_file, index=False)

            print(f"Cleaned dataset saved to {self.output_file}")
            return df_cleaned
        except Exception as e:
            print(f"Error cleaning dataset: {e}")
            return None

def main():
    input_file = r"C:\Users\AT\CSV Dataset files\test_100k.csv"  # Provide the correct path to your raw dataset
    output_file = r"C:\Users\AT\CSV Dataset files\cleaned_articles_test.csv"  # Specify the cleaned dataset path
    cleaner = DatasetCleaner(input_file, output_file)
    cleaner.clean_dataset()

if __name__ == "__main__":
    main()
