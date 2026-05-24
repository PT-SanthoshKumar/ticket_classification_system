# Customer Support Ticket Classification System

This project classifies support tickets into categories and assigns a priority level so support teams can triage work faster.

## What You Built

- Text cleaning and tokenization with NLTK-compatible preprocessing
- Ticket category classification with Scikit-learn
- Category keyword rules for obvious support routing
- Priority tagging with transparent business rules
- Flask backend API
- Browser frontend for trying ticket predictions
- Jupyter Notebook for learning and experimentation
- Model evaluation with accuracy and classification report

## Project Structure

```text
ticket_classification_system/
  backend/
    app.py
  data/
    sample_tickets.csv
  frontend/
    index.html
    styles.css
    script.js
  ml/
    preprocessing.py
    category_rules.py
    priority.py
    train_model.py
    predict.py
  models/
    ticket_category_model.joblib
  notebooks/
    ticket_text_processing_learning.ipynb
  requirements.txt
  README.md
```

## Setup

Open a terminal in this folder:

```powershell
cd "$env:USERPROFILE\Desktop\ticket_classification_system"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Optional NLTK data download:

```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

The code also includes fallbacks, so it can still clean text if those NLTK datasets are missing.

## Train And Evaluate The Model

```powershell
python -m ml.train_model
```

This reads `data/sample_tickets.csv`, trains a TF-IDF + Complement Naive Bayes classifier, saves it to `models/ticket_category_model.joblib`, and prints:

- Raw model accuracy
- Full system accuracy with category rules
- Precision
- Recall
- F1-score
- Support count per category

## Run The Web App

```powershell
python backend/app.py
```

Open:

```text
http://127.0.0.1:5000
```

Paste a ticket message and click **Classify ticket**.

## API Usage

Health check:

```powershell
curl http://127.0.0.1:5000/api/health
```

Classify one ticket:

```powershell
curl -X POST http://127.0.0.1:5000/api/classify `
  -H "Content-Type: application/json" `
  -d "{\"ticket_text\":\"The app is down and our whole team cannot access data.\"}"
```

## Learn The Text Processing Pipeline

Text classification usually follows this path:

1. Collect labeled text

   A model needs examples. In this project, `sample_tickets.csv` contains ticket text plus the correct category and priority.

2. Clean the text

   Raw support tickets contain capital letters, punctuation, numbers, links, and repeated filler words. `ml/preprocessing.py` converts text into a simpler form.

   Example:

   ```text
   "My payment failed twice!!!"
   ```

   becomes:

   ```text
   payment failed twice
   ```

3. Tokenize

   Tokenization splits text into useful word pieces. A sentence becomes a list of tokens:

   ```text
   ["payment", "failed", "twice"]
   ```

4. Remove stopwords

   Stopwords are common words such as `the`, `is`, `and`, and `to`. Removing them helps the model focus on words with stronger meaning.

5. Lemmatize

   Lemmatization reduces related words to a base form. For example, `crashes`, `crashed`, and `crashing` can be simplified toward `crash`.

6. Vectorize with TF-IDF

   Machine learning models need numbers, not raw words. TF-IDF turns text into numeric features by giving more weight to words that are important in one ticket but not common everywhere.

7. Train a classifier

   This project uses Complement Naive Bayes because it is fast, simple to explain, and strong for small text classification datasets.

8. Evaluate

   Accuracy alone is not enough. The classification report shows how well each category performs with precision, recall, and F1-score.

9. Add priority logic

   Priority is not always the same as category. A billing question can be low priority, while duplicate charges can be high priority. `ml/priority.py` uses clear keyword and category rules.

10. Add category rules

   A small starter model can be uncertain. `ml/category_rules.py` adds transparent routing for high-signal words like `payment`, `server`, `delivery`, and `suspicious`.

## How To Improve This Project

- Add more real historical tickets to `data/sample_tickets.csv`
- Add more categories that match your support workflow
- Store predictions in a database
- Build an admin screen for reviewing wrong predictions
- Replace rules with a second ML model for priority once enough priority labels exist
- Add authentication before deploying this in a real support environment

## Important Files To Study

- `ml/preprocessing.py`: teaches text cleaning, tokenization, stopwords, and lemmatization
- `ml/category_rules.py`: teaches transparent keyword routing for high-signal support terms
- `ml/train_model.py`: teaches model training and evaluation
- `ml/predict.py`: teaches how trained models are loaded and used
- `ml/priority.py`: teaches business priority rules
- `backend/app.py`: exposes the ML model as an API
- `frontend/script.js`: sends tickets to the API and displays results
