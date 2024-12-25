import pandas as pd
import os

def load_data(input_file, output_file, nrows=100004):
    try:
        # Load only necessary columns to reduce memory usage
        required_columns = ['url', 'title', 'text', 'tags']
        dtype = {
            'url': 'str',
            'title': 'str',
            'text': 'str',
            'tags': 'str'
        }

        df = pd.read_csv(input_file, usecols=required_columns, nrows=nrows, dtype=dtype)

        # Drop rows with missing essential columns to avoid processing incomplete rows
        df.dropna(subset=['title', 'text', 'tags', 'url'], inplace=True)

        # Save a smaller dataset for testing
        df.to_csv(output_file, index=False)

        print(f"Loaded {len(df)} rows from {input_file}, saved to {output_file}")
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

if __name__ == "__main__":
    input_file = r"C:\Users\AT\CSV Dataset files\medium_articles.csv"
    output_file = r"C:\Users\AT\CSV Dataset files\test_100k.csv"
    load_data(input_file, output_file)
