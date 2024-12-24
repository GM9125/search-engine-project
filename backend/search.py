import pandas as pd
import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Ensure NLTK resources are available
nltk.download('stopwords', quiet=True)

class SearchEngine:
    def __init__(self, lexicon_path, barrels_folder, cleaned_dataset_path):
        if not os.path.exists(barrels_folder):
            raise FileNotFoundError(f"The barrels folder {barrels_folder} does not exist.")
        
        self.lexicon = pd.read_csv(lexicon_path).set_index('word')['word_id'].to_dict()
        self.cleaned_dataset = pd.read_csv(cleaned_dataset_path).reset_index(drop=True)
        self.barrels_folder = barrels_folder

    def _load_barrel(self, word_id):
        barrel_index = word_id % len(os.listdir(self.barrels_folder))
        barrel_filename = f'inverted_index_barrel_{barrel_index}.csv'
        barrel_path = os.path.join(self.barrels_folder, barrel_filename)

        if not os.path.exists(barrel_path):
            return {}

        barrel_df = pd.read_csv(barrel_path)
        return barrel_df.set_index('word_id')['doc_ids'].apply(
            lambda x: list(map(int, re.split(r'[ ,]+', x))) if isinstance(x, str) else []
        ).to_dict()

    def _preprocess_query(self, query):
        stop_words = set(stopwords.words('english'))
        query = re.sub(r'[^\w\s]', '', query)
        tokens = word_tokenize(query.lower())
        return [token for token in tokens if token not in stop_words and token.isalpha()]

    def _page_rank(self, word_results):
        return sorted(word_results.items(), key=lambda x: x[1], reverse=True)

    def search(self, query, max_results=25):
        tokens = self._preprocess_query(query)
        if not tokens:
            return []

        word_results = {}
        for token in tokens:
            if token not in self.lexicon:
                continue
            word_id = self.lexicon[token]
            barrel = self._load_barrel(word_id)
            if word_id in barrel:
                for doc_id in barrel[word_id]:
                    word_results[doc_id] = word_results.get(doc_id, 0) + 1

        sorted_doc_ids = [doc_id for doc_id, _ in self._page_rank(word_results)]

        results = []
        for rank, doc_id in enumerate(sorted_doc_ids[:max_results], 1):
            if doc_id in self.cleaned_dataset.index:
                title = self.cleaned_dataset.loc[doc_id, 'title']
                url = self.cleaned_dataset.loc[doc_id, 'url']
                results.append({
                    'rank': rank,
                    'doc_id': doc_id,
                    'title': title.capitalize(),
                    'url': url
                })

        return results
