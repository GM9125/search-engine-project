import pandas as pd
import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import nltk

# Ensure NLTK resources are available
nltk.download('stopwords', quiet=True)

class SearchEngine:
    def __init__(self, lexicon_path, barrels_folder, cleaned_dataset_path):
        """
        Initialize the search engine with the provided paths.
        
        Args:
            lexicon_path (str): Path to the lexicon file.
            barrels_folder (str): Path to the folder containing the inverted index barrels.
            cleaned_dataset_path (str): Path to the cleaned dataset file.
        """
        if not os.path.exists(barrels_folder):
            raise FileNotFoundError(f"The barrels folder {barrels_folder} does not exist.")
        
        # Load lexicon (mapping of words to word IDs)
        self.lexicon = pd.read_csv(lexicon_path).set_index('word')['word_id'].to_dict()
        
        # Load cleaned dataset (contains document information such as title, URL, etc.)
        self.cleaned_dataset = pd.read_csv(cleaned_dataset_path).reset_index(drop=True)
        
        # Path to the folder containing the inverted index barrels
        self.barrels_folder = barrels_folder

    def _load_barrel(self, word_id):
        """
        Load a specific barrel based on the word_id.
        Efficiently access the barrel data for a word's results.

        Args:
            word_id (int): Word ID for the specific word we are searching for.
        
        Returns:
            dict: A dictionary of document IDs for the given word ID.
        """
        # Simple hashing to select the correct barrel based on word_id
        barrel_index = word_id % len(os.listdir(self.barrels_folder))
        barrel_filename = f'inverted_index_barrel_{barrel_index}.csv'
        barrel_path = os.path.join(self.barrels_folder, barrel_filename)

        # If barrel file doesn't exist, return an empty dictionary
        if not os.path.exists(barrel_path):
            print(f"Warning: Barrel file {barrel_filename} not found.")
            return {}

        # Read the barrel CSV file
        barrel_df = pd.read_csv(barrel_path)
        
        # Fix: Handle space-separated or comma-separated doc_ids and convert to list of integers
        barrel_dict = barrel_df.set_index('word_id')['doc_ids'].apply(
            lambda x: list(map(int, re.split(r'[ ,]+', x))) if isinstance(x, str) else [])
        
        return barrel_dict.to_dict()

    def _preprocess_query(self, query):
        """
        Preprocess the user's query by tokenizing and removing stop words.

        Args:
            query (str): The search query entered by the user.
        
        Returns:
            list: A list of processed query tokens.
        """
        stop_words = set(stopwords.words('english'))
        
        # Remove non-alphanumeric characters from the query
        query = re.sub(r'[^\w\s]', '', query)
        
        # Tokenize the query and convert to lowercase
        tokens = word_tokenize(query.lower())
        
        # Remove stop words and non-alphabetical tokens
        return [token for token in tokens if token not in stop_words and token.isalpha()]

    def _page_rank(self, word_results):
        """
        Sort documents based on frequency and return a ranked list.
        
        Args:
            word_results (dict): A dictionary of document IDs and their respective word frequency scores.
        
        Returns:
            list: Sorted document IDs based on their frequency and PageRank score.
        """
        # Sort documents based on word frequency in descending order
        sorted_docs = sorted(word_results.items(), key=lambda x: x[1], reverse=True)
        return [doc_id for doc_id, _ in sorted_docs]

    def search(self, query, max_results=25):
        """
        Search for the given query in the indexed dataset.
        
        Args:
            query (str): The search query entered by the user.
            max_results (int): Maximum number of search results to return.
        
        Returns:
            list: A list of search results containing document information (title, URL).
        """
        tokens = self._preprocess_query(query)
        
        if not tokens:
            return []

        word_results = {}  # This will store the frequency of each document that matches the query

        # For each token in the query, find the corresponding word ID from the lexicon
        for token in tokens:
            if token not in self.lexicon:
                continue
            
            word_id = self.lexicon[token]
            
            # Load the corresponding barrel for the word_id
            barrel = self._load_barrel(word_id)
            
            if word_id in barrel:
                doc_ids = barrel[word_id]
                for doc_id in doc_ids:
                    word_results[doc_id] = word_results.get(doc_id, 0) + 1

        # Sort documents by frequency and rank them
        sorted_doc_ids = self._page_rank(word_results)

        # Collect the top results
        results = []
        for rank, doc_id in enumerate(sorted_doc_ids[:max_results], 1):
            # Fetch the title and URL exactly as it appears in the original dataset
            try:
                title = self.cleaned_dataset.loc[doc_id, 'title']  # Ensure doc_id is valid
                url = self.cleaned_dataset.loc[doc_id, 'url']
                
                # Format the title based on sentence capitalization
                formatted_title = self._capitalize_title(title)
                
                # Append to results
                results.append({
                    'rank': rank,
                    'doc_id': doc_id,
                    'title': formatted_title,
                    'url': url
                })
            except KeyError:
                print(f"Warning: Document ID {doc_id} does not exist in the dataset.")
                continue

        return results

    def _capitalize_title(self, title):
        """
        Capitalize the title based on sentence case rules (only first word is capitalized).
        
        Args:
            title (str): The original title string.
        
        Returns:
            str: The title with sentence case formatting.
        """
        # Split the title into words
        words = title.split()

        # Capitalize the first word, keep the rest in lowercase
        if words:
            words[0] = words[0].capitalize()

        # Join words back into a string and return
        return " ".join(words)

    def display_results(self, results):
        """
        Display the search results to the user.
        
        Args:
            results (list): A list of search results to display.
        """
        if not results:
            print("No results found.")
            return
        
        # Display each result without word frequency
        for result in results:
            print(f"{result['rank']}) Title: {result['title']}")
            print(f"   URL: {result['url']}\n")


def main():
    """
    Main function to initialize the SearchEngine and handle user input for searching.
    """
    try:
        # Initialize the search engine with the necessary file paths
        search_engine = SearchEngine(
            lexicon_path=r"C:\Users\AT\CSV Dataset files\lexicon.csv",
            barrels_folder=r"C:\Users\AT\CSV Dataset files\barrels_inverted_index",
            cleaned_dataset_path=r"C:\Users\AT\CSV Dataset files\cleaned_articles_test.csv"
        )
        
        while True:
            # Prompt the user for a search query
            query = input("Enter search query (or 'exit' to quit): ").strip()
            
            if query.lower() == 'exit':
                break
            
            if not query:
                print("Please enter a valid search query.")
                continue

            try:
                # Perform the search and display the results
                results = search_engine.search(query)
                search_engine.display_results(results)
            
            except Exception as e:
                print(f"An error occurred during search: {e}")
    
    except Exception as e:
        print(f"Error initializing search engine: {e}")

if __name__ == "__main__":
    main()
