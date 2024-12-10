import pandas as pd

# File paths
input_forward_index_file = r"C:\Users\AT\CSV Dataset files\forward_index.csv"
output_inverted_index_file = r"C:\Users\AT\CSV Dataset files\inverted_index.csv"

# Create inverted index
def create_inverted_index(forward_index):
    inverted_index = {}
    for doc_id, word_ids in forward_index.items():
        for word_id in word_ids:
            if word_id not in inverted_index:
                inverted_index[word_id] = []
            inverted_index[word_id].append(doc_id)
    return inverted_index

# Load the forward index
forward_index_df = pd.read_csv(input_forward_index_file)

# Parse forward index data
forward_index = {
    int(row["doc_id"]): list(map(int, row["word_ids"].split()))  # Convert doc_id and word_ids to integers
    for _, row in forward_index_df.iterrows()
}

# Generate the inverted index
inverted_index = create_inverted_index(forward_index)

# Convert inverted index to DataFrame and save
inverted_index_df = pd.DataFrame(
    [{"word_id": word_id, "doc_ids": " ".join(map(str, doc_ids))} for word_id, doc_ids in inverted_index.items()]
)
inverted_index_df.to_csv(output_inverted_index_file, index=False)

print(f"Inverted index saved to {output_inverted_index_file}")
