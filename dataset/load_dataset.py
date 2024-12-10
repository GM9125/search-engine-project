import pandas as pd

# Specify file paths
input_file = r"C:\Users\AT\CSV Dataset files\medium_articles.csv"
output_file = r"C:\Users\AT\CSV Dataset files\test.csv"

# Columns not needed for processing
non_required_columns = ['url', 'authors', 'timestamp']  # Keep 'title', 'text', and 'tags'

# Load only the first 100 rows
df = pd.read_csv(input_file, nrows=100)

# Drop unnecessary columns
df = df.drop(columns=non_required_columns)

# Save to a smaller file for testing
df.to_csv(output_file, index=False)

print(f"Test dataset saved to {output_file}")
