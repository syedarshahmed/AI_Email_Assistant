# data/text_processor.py

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def clean_text(text):
    """Clean a single email text"""

    # Step 1: Lowercase
    text = text.lower()

    # Step 2: Remove emails, URLs, numbers, punctuation
    text = re.sub(r'\S+@\S+', '', text)        # remove emails
    text = re.sub(r'http\S+', '', text)         # remove URLs
    text = re.sub(r'\d+', '', text)             # remove numbers
    text = re.sub(r'[^a-z\s]', '', text)        # remove punctuation

    # Step 3: Tokenize
    tokens = text.split()

    # Step 4: Remove stopwords
    tokens = [t for t in tokens if t not in stop_words]

    # Step 5: Lemmatize (e.g. "running" → "run")
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    # Step 6: Remove very short words
    tokens = [t for t in tokens if len(t) > 2]

    return " ".join(tokens)


def preprocess_all(texts):
    """Clean a list of email texts"""
    cleaned = [clean_text(t) for t in texts]
    print("✅ Text cleaning done")
    return cleaned


def vectorize(train_texts, test_texts=None):
    """Convert text to TF-IDF numerical features"""
    vectorizer = TfidfVectorizer(
        max_features=500,     # keep top 500 words
        ngram_range=(1, 2),   # unigrams + bigrams
        sublinear_tf=True     # smooth term frequency
    )

    X_train = vectorizer.fit_transform(train_texts)

    print(f"✅ Vectorized — shape: {X_train.shape}")

    if test_texts is not None:
        X_test = vectorizer.transform(test_texts)
        return X_train, X_test, vectorizer

    return X_train, vectorizer