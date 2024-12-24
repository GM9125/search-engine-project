from flask import Flask, jsonify, request
from flask_cors import CORS
from search import SearchEngine

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
    page = int(request.args.get('page', 1))  # Default to page 1 if not provided

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        results = search_engine.search(query)
        per_page = 10  # Number of results per page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_results = results[start:end]

        return jsonify({
            'results': paginated_results,
            'total_results': len(results),
            'page': page,
            'total_pages': (len(results) + per_page - 1) // per_page  # Calculate total pages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
