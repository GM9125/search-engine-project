import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import unicodedata

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
        text = re.sub(r'http[s]?://\S+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _preprocess_text(self, text):
        # Tokenize, remove stop words, and lemmatize
        tokens = word_tokenize(text)
        return ' '.join(
            sorted(set(self.lemmatizer.lemmatize(word.lower()) for word in tokens if word.isalpha() and word.lower() not in ENGLISH_STOP_WORDS))
        )

    def clean_dataset(self):
        try:
            # Load dataset in chunks to avoid high memory usage
            df = pd.read_csv(self.input_file)

            # Check column names before applying transformations
            print("Columns before cleaning:", df.columns.tolist())

            # Apply transformations only once and avoid multiple passes over the data
            df['title'] = df['title'].apply(self._normalize_text)
            df['text'] = df['text'].apply(self._remove_urls_and_special_chars)
            df['tags_text'] = df['tags'].apply(self._normalize_text)
            df['cleaned_text'] = (df['title'] + " " + df['text'] + " " + df['tags_text']).apply(self._preprocess_text)

            # Check column names after transformations
            print("Columns after cleaning:", df.columns.tolist())

            # Save the cleaned dataset
            df[['title', 'url', 'tags', 'cleaned_text']].to_csv(self.output_file, index=False)

            print(f"Cleaned dataset saved to {self.output_file}")
            return df[['title', 'url', 'tags', 'cleaned_text']]

        except Exception as e:
            print(f"Error cleaning dataset: {e}")
            return None

def main():
    input_file = r"C:\Users\AT\CSV Dataset files\test_50k.csv"  # Provide the correct path to your raw dataset
    output_file = r"C:\Users\AT\CSV Dataset files\cleaned_articles_test.csv"  # Specify the cleaned dataset path
    cleaner = DatasetCleaner(input_file, output_file)
    cleaner.clean_dataset()

if __name__ == "__main__":
    main()
