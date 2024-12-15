import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
import multiprocessing
import os

class ForwardIndexGenerator:
    def __init__(self, 
                 input_cleaned_file, 
                 input_lexicon_file, 
                 output_forward_index_file):
        """
        Initialize the forward index generator.
        
        Args:
            input_cleaned_file (str): Path to cleaned dataset
            input_lexicon_file (str): Path to lexicon file
            output_forward_index_file (str): Path to save forward index
        """
        self.input_cleaned_file = input_cleaned_file
        self.input_lexicon_file = input_lexicon_file
        self.output_forward_index_file = output_forward_index_file

    def _process_document_chunk(self, chunk_data):
        """
        Process a chunk of documents to create forward index.
        
        Args:
            chunk_data (tuple): Chunk of documents and lexicon
        
        Returns:
            dict: Forward index for the chunk
        """
        df_chunk, lexicon = chunk_data
        forward_index = {}
        missed_words = set()
        
        for idx, row in df_chunk.iterrows():
            if not isinstance(row['cleaned_text'], str):
                continue

            # Tokenize and get word IDs
            tokens = word_tokenize(row['cleaned_text'].lower())
            word_ids = []

            for word in tokens:
                word_id = lexicon.get(word)
                if word_id is not None:
                    word_ids.append(word_id)
                else:
                    missed_words.add(word)

            forward_index[idx] = word_ids
        
        return forward_index, missed_words

    def create_forward_index(self, num_processes=None):
        """
        Create forward index with parallel processing.
        
        Args:
            num_processes (int, optional): Number of processes for parallel processing
        
        Returns:
            dict: Complete forward index
        """
        try:
            # Load cleaned dataset and lexicon
            df = pd.read_csv(self.input_cleaned_file)
            lexicon = pd.read_csv(self.input_lexicon_file).set_index("word")['word_id'].to_dict()
            
            # Determine number of processes
            if num_processes is None:
                num_processes = max(1, multiprocessing.cpu_count() - 1)
            
            # Split dataset into chunks
            df_chunks = np.array_split(df, num_processes)
            chunk_data = [(chunk, lexicon) for chunk in df_chunks]
            
            # Parallel processing
            with multiprocessing.Pool(processes=num_processes) as pool:
                results = pool.map(self._process_document_chunk, chunk_data)
            
            # Combine results
            forward_index = {}
            global_missed_words = set()

            for chunk_index, (chunk_forward_index, missed_words) in enumerate(results):
                forward_index.update(chunk_forward_index)
                global_missed_words.update(missed_words)

            # Log missed words (if any)
            if global_missed_words:
                print(f"Unique missed words: {global_missed_words}")

            # Convert forward index to DataFrame
            forward_index_df = pd.DataFrame([
                {"doc_id": doc_id, "word_ids": " ".join(map(str, word_ids))}
                for doc_id, word_ids in forward_index.items()
            ])

            # Save to CSV
            forward_index_df.to_csv(self.output_forward_index_file, index=False)

            print(f"Forward index saved to {self.output_forward_index_file}")
            print(f"Total documents indexed: {len(forward_index_df)}")

            return forward_index
        
        except Exception as e:
            print(f"Error creating forward index: {e}")
            raise

def main():
    # File paths
    input_cleaned_file = r"C:\Users\AT\CSV Dataset files\cleaned_articles_test.csv"
    input_lexicon_file = r"C:\Users\AT\CSV Dataset files\lexicon.csv"
    output_forward_index_file = r"C:\Users\AT\CSV Dataset files\forward_index.csv"
    
    try:
        # Initialize and run forward index generator
        forward_index_generator = ForwardIndexGenerator(
            input_cleaned_file, 
            input_lexicon_file, 
            output_forward_index_file
        )
        forward_index_generator.create_forward_index()
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
