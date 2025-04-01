# SearchIT

SearchIT is a search engine project that lets you search through articles. It uses Next.js for the frontend and Python Flask for the backend. This guide will help you set up and run the project on your computer.

---

## Features

- Fast search using inverted indexing.
- Clean interface with pagination for results.
- Scripts to load, clean, and index data.
- Backend and frontend work together using APIs.

---

## Technologies Used

- Frontend: Next.js (React)
- Backend: Python, Flask
- Data Processing: Pandas, NLTK, Scikit-learn, Joblib, Multiprocessing
- Other: Flask-CORS for API requests

---

## Project Structure

The project is organized as follows:

```
SEARCH-ENGINE-PROJECT/
├── backend/
│   ├── dataset/
│   │   └── load_dataset.py
│   ├── app.py
│   ├── forward_indexing.py
│   ├── inverted_indexing.py
│   ├── lexicon.py
│   └── search.py
├── frontend/
│   └── next/
│       ├── app/
│       │   ├── favicon.ico
│       │   ├── globals.css
│       │   ├── layout.js
│       │   ├── page.js
│       │   └── search.png
│       ├── node_modules/
│       ├── public/
│       ├── eslintrc.config.mjs
│       ├── jsconfig.json
│       ├── next.config.mjs
│       ├── package-lock.json
│       ├── package.json
│       ├── postcss.config.mjs
│       ├── README.md
│       ├── tailwind.config.mjs
│       ├── .gitattributes
│       └── .gitignore
└── README.md
```

- **backend/**: Contains Python scripts for data processing and the Flask server.
- **frontend/next/**: Contains the Next.js app for the user interface.
- **dataset/**: Inside `backend/`, this folder holds the data files.

---

## Setup Instructions

Follow these steps to set up and run SearchIT on your computer.

### Prerequisites

Make sure you have these installed:

- Python 3.x (for the backend and scripts)
- Node.js (version 18.x recommended, for the frontend)
- Git (optional, if cloning from a repository)

---

### Step 1: Get the Project

If the project is on GitHub, clone it:

```bash
git clone https://github.com/yourusername/SEARCH-ENGINE-PROJECT.git
cd SEARCH-ENGINE-PROJECT
```

If you already have the files, go to the `SEARCH-ENGINE-PROJECT` folder.

---

### Step 2: Install Dependencies

#### Python Dependencies

Install the required Python packages:

```bash
pip install pandas nltk scikit-learn joblib flask flask-cors
```

Then, download NLTK resources by running this in Python:

```python
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
```

#### Node.js Dependencies

Go to the `frontend/next` folder and install the frontend dependencies:

```bash
cd frontend/next
npm install
```

---

### Step 3: Prepare the Dataset

SearchIT needs a CSV file named `medium_articles.csv` with columns `url`, `title`, `text`, and `tags`. If you have this file, move it to the `backend/dataset/` folder:

```bash
mv /path/to/medium_articles.csv backend/dataset/
```

If you do not have the file, you will need to provide your own dataset with the same columns.

---

### Step 4: Update File Paths

The Python scripts have hardcoded file paths that you need to change to match your system. Open each file and update the paths. Use the correct format for your operating system (e.g., `/path/to/` for Unix or `C:\\path\\to\\` for Windows).

#### `backend/dataset/load_dataset.py`
Change:
```python
input_file = r"C:\Users\AT\CSV Dataset files\medium_articles.csv"
output_file = r"C:\Users\AT\CSV Dataset files\test_100k.csv"
```
To:
```python
input_file = r"/path/to/SEARCH-ENGINE-PROJECT/backend/dataset/medium_articles.csv"
output_file = r"/path/to/SEARCH-ENGINE-PROJECT/backend/dataset/test_100k.csv"
```

#### `backend/lexicon.py`
Update `input_file` and `output_lexicon_file` to your paths.

#### `backend/forward_indexing.py`
Update `input_cleaned_file`, `input_lexicon_file`, and `output_forward_index_file`.

#### `backend/inverted_indexing.py`
Update `input_forward_index_file`, `output_inverted_index_file`, and `output_barrels_folder`.

#### `backend/app.py`
Update `lexicon_path`, `barrels_folder`, and `cleaned_dataset_path`.

To make it easier, keep all files in `backend/dataset/` and use relative paths like `r"dataset/medium_articles.csv"`.

---

### Step 5: Process the Data

Run these scripts in order to prepare the data. Do this from the `SEARCH-ENGINE-PROJECT` folder:

1. Load the data:
   ```bash
   python backend/dataset/load_dataset.py
   ```

2. Build the lexicon:
   ```bash
   python backend/lexicon.py
   ```

3. Create the forward index:
   ```bash
   python backend/forward_indexing.py
   ```

4. Create the inverted index:
   ```bash
   python backend/inverted_indexing.py
   ```

These scripts may take some time depending on your dataset size.

---

### Step 6: Start the Backend

Go to the `backend` folder and start the Flask server:

```bash
cd backend
python app.py
```

Keep this terminal open. The server will run at `http://127.0.0.1:5000`.

---

### Step 7: Start the Frontend

Open a new terminal, go to `frontend/next`, and start the Next.js app:

```bash
cd frontend/next
npm run dev
```

The frontend will run at `http://localhost:3000`.

---

### Step 8: Use SearchIT

Open your browser and go to `http://localhost:3000`. Type a query in the search bar, press Enter, and see the results.

---

## Usage Notes

- Queries are not case-sensitive, and common words are ignored.
- Results show article titles and URLs with pagination.
- You can change the number of rows in `load_dataset.py` or the number of barrels in `inverted_indexing.py` if needed.

---

## Troubleshooting

If you have issues:

- Check if the Flask server (`app.py`) is running.
- Make sure all file paths are correct.
- Look at the Flask terminal or browser console (F12) for error messages.
- Ensure your dataset has the required columns (`url`, `title`, `text`, `tags`).

---

## Contributing

If you want to improve SearchIT, feel free to fork the project and submit changes. Ideas for better indexing or UI improvements are welcome.

---

## License

This project is for learning purposes. You can use it freely for education and experimentation.

---

This `README.md` is written in simple English, follows the file structure from the image, and provides clear instructions for setting up and running SearchIT. Let me know if you need any changes!
