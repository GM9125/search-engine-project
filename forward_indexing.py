import pandas as pd
from nltk.tokenize import word_tokenize

# File paths
input_cleaned_file = r"C:\Users\AT\CSV Dataset files\cleaned_articles_test.csv"
input_lexicon_file = r"C:\Users\AT\CSV Dataset files\lexicon.csv"
output_forward_index_file = r"C:\Users\AT\CSV Dataset files\forward_index.csv"

# Create forward index
def create_forward_index(df, lexicon):
    forward_index = {}
    for idx, row in df.iterrows():
        if not isinstance(row["cleaned_text"], str):
            continue
        tokens = word_tokenize(row["cleaned_text"])
        word_ids = [lexicon[word] for word in tokens if word in lexicon]
        forward_index[idx] = word_ids
    return forward_index

# Load the cleaned dataset and lexicon
df = pd.read_csv(input_cleaned_file)
lexicon = pd.read_csv(input_lexicon_file).set_index("word").to_dict()["word_id"]

# Generate the forward index
forward_index = create_forward_index(df, lexicon)

# Convert forward index to a DataFrame and save
forward_index_df = pd.DataFrame(
    [{"doc_id": doc_id, "word_ids": " ".join(map(str, word_ids))} for doc_id, word_ids in forward_index.items()]
)
forward_index_df.to_csv(output_forward_index_file, index=False)

print(f"Forward index saved to {output_forward_index_file}")
