import pandas as pd
import numpy as np
import multiprocessing
from nltk.tokenize import word_tokenize
from collections import defaultdict
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class ForwardIndexGenerator:
    def __init__(self, input_cleaned_file, input_lexicon_file, output_forward_index_file):
        self.input_cleaned_file = input_cleaned_file
        self.input_lexicon_file = input_lexicon_file
        self.output_forward_index_file = output_forward_index_file

    def _process_document_chunk(self, chunk_data):
        """
        Process a chunk of documents to create forward index.
        """
        df_chunk, lexicon = chunk_data
        forward_index = defaultdict(list)
        missed_words = set()

        for idx, row in df_chunk.iterrows():
            if isinstance(row['cleaned_text'], str):
                tokens = word_tokenize(row['cleaned_text'].lower())
                word_ids = [lexicon.get(word) for word in tokens if lexicon.get(word)]

                if word_ids:
                    forward_index[idx] = word_ids
                else:
                    missed_words.add(row['cleaned_text'])

        return forward_index, missed_words

    def create_forward_index(self, num_processes=None):
        """
        Create forward index with parallel processing.
        """
        try:
            df = pd.read_csv(self.input_cleaned_file)
            lexicon = pd.read_csv(self.input_lexicon_file).set_index("word")['word_id'].to_dict()
            
            if num_processes is None:
                num_processes = max(1, multiprocessing.cpu_count() - 1)
            
            # Split dataset into chunks for parallel processing
            df_chunks = np.array_split(df, num_processes)
            chunk_data = [(chunk, lexicon) for chunk in df_chunks]

            with multiprocessing.Pool(processes=num_processes) as pool:
                results = pool.map(self._process_document_chunk, chunk_data)
            
            # Merge results
            forward_index = {}
            global_missed_words = set()

            for chunk_forward_index, missed_words in results:
                forward_index.update(chunk_forward_index)
                global_missed_words.update(missed_words)

            if global_missed_words:
                print(f"Missed words: {global_missed_words}")

            # Convert forward index to DataFrame
            forward_index_df = pd.DataFrame(
                [{"doc_id": doc_id, "word_ids": " ".join(map(str, word_ids))} 
                 for doc_id, word_ids in forward_index.items()]
            )

            # Save to CSV
            forward_index_df.to_csv(self.output_forward_index_file, index=False)
            print(f"Forward index saved to {self.output_forward_index_file}")
            return forward_index
        
        except Exception as e:
            print(f"Error creating forward index: {e}")
            raise

# Example usage:
def main():
    # Define file paths
    input_cleaned_file = r"C:\Users\AT\CSV Dataset files\cleaned_articles_test.csv"  # Path to cleaned dataset
    input_lexicon_file = r"C:\Users\AT\CSV Dataset files\lexicon.csv"  # Path to lexicon file
    output_forward_index_file = r"C:\Users\AT\CSV Dataset files\forward_indexing.csv"  # Output path for forward index

    # Create an instance of ForwardIndexGenerator and generate the forward index
    forward_index_generator = ForwardIndexGenerator(input_cleaned_file, input_lexicon_file, output_forward_index_file)
    forward_index_generator.create_forward_index(num_processes=4)  # Adjust number of processes as needed

if __name__ == "__main__":
    main()
