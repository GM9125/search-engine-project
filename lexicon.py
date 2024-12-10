import pandas as pd
from nltk.tokenize import word_tokenize

# File paths
input_file = r"C:\Users\AT\CSV Dataset files\cleaned_articles_test.csv"
output_lexicon_file = r"C:\Users\AT\CSV Dataset files\lexicon.csv"

# Create a lexicon mapping words to unique IDs
def create_lexicon(df):
    lexicon = {}
    word_id = 1
    for text in df["cleaned_text"]:
        if not isinstance(text, str):
            continue
        tokens = word_tokenize(text)  # Tokenize the text
        for word in tokens:
            if word not in lexicon:
                lexicon[word] = word_id
                word_id += 1
    return lexicon

# Load the cleaned dataset
df = pd.read_csv(input_file)

# Generate the lexicon
lexicon = create_lexicon(df)

# Save the lexicon to a CSV file
lexicon_df = pd.DataFrame(list(lexicon.items()), columns=["word", "word_id"])
lexicon_df.to_csv(output_lexicon_file, index=False)

print(f"Lexicon saved to {output_lexicon_file}")
