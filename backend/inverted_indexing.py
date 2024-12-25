import pandas as pd
import os
import numpy as np
import multiprocessing
from collections import defaultdict
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

class InvertedIndexGenerator:
    def __init__(self, 
                 input_forward_index_file, 
                 output_inverted_index_file, 
                 output_barrels_folder):
        """
        Initialize the inverted index generator.

        Args:
            input_forward_index_file (str): Path to forward index file
            output_inverted_index_file (str): Path to save full inverted index
            output_barrels_folder (str): Folder to save inverted index barrels
        """
        self.input_forward_index_file = input_forward_index_file
        self.output_inverted_index_file = output_inverted_index_file
        self.output_barrels_folder = output_barrels_folder
        
        # Ensure output directory exists
        os.makedirs(output_barrels_folder, exist_ok=True)

    def _process_forward_index_chunk(self, chunk):
        """
        Process a chunk of forward index to create inverted index.

        Args:
            chunk (pd.DataFrame): Chunk of forward index data

        Returns:
            dict: Partial inverted index for the chunk
        """
        inverted_index = defaultdict(set)
        
        for _, row in chunk.iterrows():
            doc_id = row['doc_id']
            word_ids = [int(word_id) for word_id in row['word_ids'].split()]
            
            # Create inverted index for this chunk
            for word_id in word_ids:
                inverted_index[word_id].add(doc_id)
        
        return dict(inverted_index)

    def _distribute_to_barrels(self, inverted_index, num_barrels=10):
        """
        Distribute inverted index to multiple barrels.

        Args:
            inverted_index (dict): Full inverted index
            num_barrels (int): Number of barrels to distribute

        Returns:
            list: Barrels with distributed word IDs
        """
        barrels = [{} for _ in range(num_barrels)]
        
        for word_id, doc_ids in inverted_index.items():
            # Distribute to barrel based on word_id modulo
            barrel_id = word_id % num_barrels
            barrels[barrel_id][word_id] = sorted(list(doc_ids))
        
        return barrels

    def create_inverted_index(self, num_processes=None, num_barrels=10):
        """
        Create inverted index with parallel processing and barrel distribution.

        Args:
            num_processes (int, optional): Number of processes
            num_barrels (int): Number of inverted index barrels

        Returns:
            dict: Complete inverted index
        """
        try:
            # Load forward index
            forward_index_df = pd.read_csv(self.input_forward_index_file)
            
            # Determine number of processes
            if num_processes is None:
                num_processes = max(1, multiprocessing.cpu_count() - 1)
            
            # Split forward index into chunks
            chunks = np.array_split(forward_index_df, num_processes)
            
            # Parallel processing of forward index chunks
            with multiprocessing.Pool(processes=num_processes) as pool:
                partial_inverted_indices = pool.map(self._process_forward_index_chunk, chunks)
            
            # Merge partial inverted indices
            full_inverted_index = {}
            for partial_index in partial_inverted_indices:
                for word_id, doc_ids in partial_index.items():
                    if word_id not in full_inverted_index:
                        full_inverted_index[word_id] = set()
                    full_inverted_index[word_id].update(doc_ids)
            
            # Convert sets to sorted lists
            full_inverted_index = {
                word_id: sorted(list(doc_ids)) 
                for word_id, doc_ids in full_inverted_index.items()
            }
            
            # Sort the inverted index by word_id
            full_inverted_index = dict(sorted(full_inverted_index.items()))
            
            # Save the full inverted index in the desired format (word_id : doc_ids)
            inverted_index_df = pd.DataFrame([{
                "word_id": word_id, 
                "doc_ids": " ".join(map(str, doc_ids))} 
                for word_id, doc_ids in full_inverted_index.items()
            ])
            
            # Save to CSV with columns "word_id" and "doc_ids"
            inverted_index_df.to_csv(self.output_inverted_index_file, index=False)
            
            # Distribute to barrels
            inverted_index_barrels = self._distribute_to_barrels(full_inverted_index, num_barrels)
            
            # Save each barrel to a separate file
            for i, barrel in enumerate(inverted_index_barrels):
                barrel_df = pd.DataFrame([{
                    "word_id": word_id, 
                    "doc_ids": " ".join(map(str, doc_ids))}
                    for word_id, doc_ids in barrel.items()
                ])
                barrel_file = os.path.join(
                    self.output_barrels_folder, 
                    f"inverted_index_barrel_{i}.csv"
                )
                barrel_df.to_csv(barrel_file, index=False)
                print(f"Inverted index barrel {i} saved to {barrel_file}")
            
            print(f"Full inverted index saved to {self.output_inverted_index_file}")
            print(f"Total unique words in inverted index: {len(full_inverted_index)}")
            
            return full_inverted_index
        
        except Exception as e:
            print(f"Error creating inverted index: {e}")
            raise

def main():
    # File paths
    input_forward_index_file = r"C:\Users\AT\CSV Dataset files\forward_indexing.csv"
    output_inverted_index_file = r"C:\Users\AT\CSV Dataset files\inverted_indexing.csv"
    output_barrels_folder = r"C:\Users\AT\CSV Dataset files\inverted_index_barrels"
    
    try:
        # Initialize and run inverted index generator
        inverted_index_generator = InvertedIndexGenerator(
            input_forward_index_file, 
            output_inverted_index_file, 
            output_barrels_folder
        )
        inverted_index_generator.create_inverted_index()
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
