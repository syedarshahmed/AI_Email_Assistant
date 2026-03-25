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


def load_model(path="model/"):
    """Load saved model from disk"""

    model      = pickle.load(open(os.path.join(path, "model.pkl"), "rb"))
    vectorizer = pickle.load(open(os.path.join(path, "vectorizer.pkl"), "rb"))
    encoder    = pickle.load(open(os.path.join(path, "encoder.pkl"), "rb"))

    print("✅ Model loaded successfully")
    return model, vectorizer, encoder