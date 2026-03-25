# data/data_loader.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_data(filepath):
    """Load the CSV dataset"""
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df)} emails")
    print(df.head())
    return df


def prepare_data(df):
    """Combine text fields and encode labels"""

    # Step 1: Combine subject + body into one text column
    df['text'] = df['subject'] + " " + df['body']

    # Step 2: Encode priority labels to numbers
    # CRITICAL=0, HIGH=1, LOW=2, MEDIUM=3 (alphabetical)
    encoder = LabelEncoder()
    df['label'] = encoder.fit_transform(df['expected_priority'])

    print("\n✅ Label Mapping:")
    for i, cls in enumerate(encoder.classes_):
        print(f"   {i} → {cls}")

    return df, encoder


def get_features_and_labels(df):
    """Return X (input text) and y (labels)"""
    X = df['text'].values
    y = df['label'].values
    return X, y