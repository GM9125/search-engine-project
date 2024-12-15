from flask import Flask, jsonify, request
from flask_cors import CORS
from search import SearchEngine  # Ensure this file exists and works

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow CORS for React app

# Initialize Search Engine
search_engine = SearchEngine(
    lexicon_path=r"C:\Users\AT\CSV Dataset files\lexicon.csv",
    barrels_folder=r"C:\Users\AT\CSV Dataset files\barrels_inverted_index",
    cleaned_dataset_path=r"C:\Users\AT\CSV Dataset files\cleaned_articles_test.csv"
)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        # Perform search and return results
        results = search_engine.search(query)
        return jsonify({'results': results}), 200
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
