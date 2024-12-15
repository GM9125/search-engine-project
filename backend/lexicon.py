import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
import multiprocessing
from collections import Counter

class LexiconGenerator:
    def __init__(self, input_file, output_lexicon_file):
        """
        Initialize the lexicon generator.
        
        Args:
            input_file (str): Path to the cleaned dataset
            output_lexicon_file (str): Path to save the lexicon
        """
        self.input_file = input_file
        self.output_lexicon_file = output_lexicon_file
    
    def _process_text_chunk(self, text_chunk):
        """
        Process a chunk of text to extract unique words.
        
        Args:
            text_chunk (pd.Series): Series of text to process
        
        Returns:
            Counter: Unique words in the chunk
        """
        word_counter = Counter()
        
        for text in text_chunk:
            if not isinstance(text, str):
                continue
            
            # Tokenize and count unique words (simple split instead of word_tokenize for speed)
            tokens = text.split()
            word_counter.update(set(tokens))  # Use set to avoid duplicates in the same document
        
        return word_counter
    
    def create_lexicon(self, num_processes=None):
        """
        Create a lexicon with unique words and their IDs.
        
        Args:
            num_processes (int, optional): Number of processes for parallel processing
        
        Returns:
            dict: Lexicon mapping words to unique IDs
        """
        try:
            # Load the cleaned dataset
            df = pd.read_csv(self.input_file)
            
            # Validate input
            if 'cleaned_text' not in df.columns:
                raise ValueError("Dataset must contain 'cleaned_text' column")
            
            # Determine number of processes
            if num_processes is None:
                num_processes = max(1, multiprocessing.cpu_count() - 1)
            
            # Split dataset into chunks for parallel processing
            chunks = np.array_split(df['cleaned_text'], num_processes)
            
            # Parallel word counting
            with multiprocessing.Pool(processes=num_processes) as pool:
                word_counters = pool.map(self._process_text_chunk, chunks)
            
            # Combine word counters
            global_counter = Counter()
            for counter in word_counters:
                global_counter.update(counter)
            
            # Create lexicon with unique word IDs
            # Sort words by frequency to give more frequent words lower IDs
            sorted_words = sorted(global_counter.items(), key=lambda x: x[1], reverse=True)
            lexicon = {word: word_id + 1 for word_id, (word, _) in enumerate(sorted_words)}
            
            # Save lexicon to CSV
            lexicon_df = pd.DataFrame(
                list(lexicon.items()), 
                columns=["word", "word_id"]
            )
            lexicon_df.to_csv(self.output_lexicon_file, index=False)
            
            print(f"Lexicon saved to {self.output_lexicon_file}")
            print(f"Total unique words in lexicon: {len(lexicon)}")
            
            return lexicon
        
        except Exception as e:
            print(f"Error creating lexicon: {e}")
            raise

def main():
    # File paths
    input_file = r"C:\Users\AT\CSV Dataset files\cleaned_articles_test.csv"  # Correct the path if needed
    output_lexicon_file = r"C:\Users\AT\CSV Dataset files\lexicon.csv"  # Path to save lexicon
    
    try:
        # Initialize and run lexicon generator
        lexicon_generator = LexiconGenerator(input_file, output_lexicon_file)
        lexicon_generator.create_lexicon()
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
