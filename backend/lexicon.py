import pandas as pd
import numpy as np
from collections import Counter
import multiprocessing
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class LexiconGenerator:
    def __init__(self, input_file, output_lexicon_file):
        self.input_file = input_file
        self.output_lexicon_file = output_lexicon_file

    def _process_text_chunk(self, text_chunk):
        """
        Process a chunk of text to extract unique words.
        """
        word_counter = Counter()
        for text in text_chunk:
            if isinstance(text, str):
                tokens = text.split()  # Split words by whitespace
                word_counter.update(set(tokens))  # Use set to avoid duplicates
        return word_counter
    
    def create_lexicon(self, num_processes=None):
        """
        Create a lexicon with unique words and their IDs.
        """
        try:
            df = pd.read_csv(self.input_file)
            
            if 'cleaned_text' not in df.columns:
                raise ValueError("Dataset must contain 'cleaned_text' column")
            
            # Determine number of processes
            if num_processes is None:
                num_processes = max(1, multiprocessing.cpu_count() - 1)
            
            chunks = np.array_split(df['cleaned_text'], num_processes)
            
            # Parallel processing using multiple processes
            with multiprocessing.Pool(processes=num_processes) as pool:
                word_counters = pool.map(self._process_text_chunk, chunks)
            
            # Merge all word counters into one
            global_counter = Counter()
            for counter in word_counters:
                global_counter.update(counter)
            
            # Sort words by frequency
            sorted_words = sorted(global_counter.items(), key=lambda x: x[1], reverse=True)
            lexicon = {word: word_id + 1 for word_id, (word, _) in enumerate(sorted_words)}
            
            # Save lexicon
            lexicon_df = pd.DataFrame(list(lexicon.items()), columns=["word", "word_id"])
            lexicon_df.to_csv(self.output_lexicon_file, index=False)
            
            print(f"Lexicon saved to {self.output_lexicon_file}")
            return lexicon
        
        except Exception as e:
            print(f"Error creating lexicon: {e}")
            raise

def main():
    input_file = r"C:\Users\AT\CSV Dataset files\cleaned_articles_test.csv"  # Path to the cleaned dataset
    output_lexicon_file = r"C:\Users\AT\CSV Dataset files\lexicon.csv"  # Path where lexicon will be saved

    lexicon_generator = LexiconGenerator(input_file, output_lexicon_file)
    lexicon_generator.create_lexicon(num_processes=4)  # You can adjust the number of processes here if needed

if __name__ == "__main__":
    main()
