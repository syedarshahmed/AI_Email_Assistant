# model/classifier.py

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

def train_model(X, y):
    """Train Logistic Regression model"""

    model = LogisticRegression(
        max_iter=1000,        # enough iterations to converge
        solver='lbfgs'        # works well for small datasets
    )

    model.fit(X, y)
    print("✅ Model trained successfully")
    return model


def evaluate_model(model, X, y, encoder):
    """Print accuracy and classification report"""

    predictions = model.predict(X)
    accuracy = accuracy_score(y, predictions)

    print(f"\n✅ Accuracy: {accuracy * 100:.2f}%")
    print("\n✅ Classification Report:")
    print(classification_report(
        y,
        predictions,
        target_names=encoder.classes_
    ))


def save_model(model, vectorizer, encoder, path="model/"):
    """Save model, vectorizer and encoder to disk"""

    pickle.dump(model,      open(os.path.join(path, "model.pkl"), "wb"))
    pickle.dump(vectorizer, open(os.path.join(path, "vectorizer.pkl"), "wb"))
    pickle.dump(encoder,    open(os.path.join(path, "encoder.pkl"), "wb"))

    print("✅ Model saved to model/ folder")


def load_model():
    path = "model"

    model_path = os.path.join(path, "model.pkl")

    if not os.path.exists(model_path):
        print("⚠️ Model not found. Training new model...")

        from data.data_loader import load_data, prepare_data, get_features_and_labels
        from data.text_processor import preprocess_all, vectorize

        df = load_data("data/emails.csv")
        df, encoder = prepare_data(df)
        X_raw, y = get_features_and_labels(df)
        X_cleaned = preprocess_all(X_raw)
        X_vectorized, vectorizer = vectorize(X_cleaned)

        model = train_model(X_vectorized, y)
        save_model(model, vectorizer, encoder)

        return model, vectorizer, encoder

    # if exists → load normally
    import pickle

    model = pickle.load(open(os.path.join(path, "model.pkl"), "rb"))
    vectorizer = pickle.load(open(os.path.join(path, "vectorizer.pkl"), "rb"))
    encoder = pickle.load(open(os.path.join(path, "encoder.pkl"), "rb"))

    return model, vectorizer, encoder