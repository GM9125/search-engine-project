# Welcome to SearchIT! 👋

Hey there! Ready to jump into the exciting world of search engines? **SearchIT** is your very own sandbox to see how search magic happens behind the scenes. With a cool Next.js frontend and a powerful Python Flask backend, you’ll be searching through articles like a pro in no time. Whether you’re a curious coder or just love tinkering, we’ve made this as fun and straightforward as possible—let’s get started!

---

## What’s SearchIT All About?

- **Super-Speedy Searches**: Thanks to some clever indexing tricks, your queries zip through fast. ⚡
- **Slick Design**: A clean, modern interface with pagination to keep everything neat. 🎨
- **Data Wizardry**: Scripts that load, clean, and index your dataset with ease. 🧙‍♂️
- **Teamwork**: A Flask backend and Next.js frontend chatting seamlessly via APIs. 🤝

---

## Tech Stack

Here’s the toolkit we’re working with:

- **Frontend**: Next.js (React)
- **Backend**: Python, Flask
- **Data Crunching**: Pandas, NLTK, Scikit-learn, Joblib, Multiprocessing
- **Extras**: Flask-CORS for smooth cross-origin requests

---

## How’s It Organized?

The project (named `SEARCH-ENGINE-PROJECT` in the image) is neatly split into backend and frontend goodies. Here’s the layout based on what I saw:

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

- **backend/**: The brains of the operation—Python scripts for data processing and the Flask server.
- **frontend/next/**: The face of SearchIT—a Next.js app with all the UI bells and whistles.
- **dataset/**: Tucked inside `backend/`, this is where your data lives and gets prepped.

---

## Let’s Get You Set Up!

Ready to bring SearchIT to life? Follow these steps, and we’ll have you searching in no time. Don’t worry—I’ll keep it simple and fun! 😊

### Before You Begin

Make sure you’ve got these installed:

- **Python 3.x**: For running the backend and data scripts.
- **Node.js**: Version 18.x works best for the frontend.
- **Git**: Optional, but great if you’re cloning from a repo.

---

### Step 1: Grab the Project

If SearchIT is hosted on GitHub, clone it like this:

```bash
git clone https://github.com/yourusername/SEARCH-ENGINE-PROJECT.git
cd SEARCH-ENGINE-PROJECT
```

Or, if you’ve got the files already, just hop into the `SEARCH-ENGINE-PROJECT` folder.

---

### Step 2: Install the Essentials

#### For the Backend (Python)

Install the Python packages we need:

```bash
pip install pandas nltk scikit-learn joblib flask flask-cors
```

Then, fire up Python and grab some NLTK extras:

```python
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
```

#### For the Frontend (Node.js)

Navigate to `frontend/next` and set up the frontend dependencies:

```bash
cd frontend/next
npm install
```

---

### Step 3: Prep Your Dataset

SearchIT loves a CSV file named `medium_articles.csv` with columns like `url`, `title`, `text`, and `tags`. Got one? Awesome! Move it to the `backend/dataset/` folder:

```bash
mv /path/to/medium_articles.csv backend/dataset/
```

No dataset? You might need to grab one or tweak `load_dataset.py` to fit your data—more on that later!

---

### Step 4: Tweak Those File Paths

The Python scripts have hardcoded paths that need to match where your files live. Open each one and update them to point to your setup (e.g., `/path/to/SEARCH-ENGINE-PROJECT/` on Unix or `C:\\path\\to\\SEARCH-ENGINE-PROJECT\\` on Windows). Here’s the rundown:

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
Adjust `input_cleaned_file`, `input_lexicon_file`, and `output_forward_index_file`.

#### `backend/inverted_indexing.py`
Fix `input_forward_index_file`, `output_inverted_index_file`, and `output_barrels_folder`.

#### `backend/app.py`
Update `lexicon_path`, `barrels_folder`, and `cleaned_dataset_path`.

**Quick Tip**: Keep everything in `backend/dataset/` and use relative paths like `r"dataset/medium_articles.csv"` to save yourself some hassle!

---

### Step 5: Process the Data

Time to get that dataset ready! Run these scripts in order from the `SEARCH-ENGINE-PROJECT` root:

1. **Load the Data**:
   ```bash
   python backend/dataset/load_dataset.py
   ```

2. **Build the Lexicon**:
   ```bash
   python backend/lexicon.py
   ```

3. **Create the Forward Index**:
   ```bash
   python backend/forward_indexing.py
   ```

4. **Generate the Inverted Index**:
   ```bash
   python backend/inverted_indexing.py
   ```

These might take a minute depending on your dataset size—perfect time for a snack break! 🍪

---

### Step 6: Launch the Backend

Head to the `backend` folder and start the Flask server:

```bash
cd backend
python app.py
```

Keep this terminal running—it’s the heartbeat of your search engine.

---

### Step 7: Fire Up the Frontend

Open a new terminal, navigate to `frontend/next`, and kick off the Next.js app:

```bash
cd frontend/next
npm run dev
```

---

### Step 8: Start Searching!

Pop open your browser and go to `http://localhost:3000`. Type a query, hit search, and watch the magic happen! 🎉

---

## Using SearchIT

- **Search Tips**: Queries are case-insensitive, and common words get skipped.
- **What You’ll See**: Results with pagination—nice and organized!
- **Customize It**: Play with `load_dataset.py` to adjust row counts or tweak `inverted_indexing.py` for barrel sizes.

---

## Troubleshooting

Running into hiccups? Try these:

- **No Results?** Check if `app.py` is running and paths match your setup.
- **Errors?** Peek at the Flask terminal or browser console (F12) for clues.
- **Stuck?** Double-check your dataset columns (`url`, `title`, `text`, `tags`).

---

## Want to Contribute?

Spotted a bug or got a brilliant idea? Fork the project, tweak it, and send a pull request—we’d love your input! 🙌

---
