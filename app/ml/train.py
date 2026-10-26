"""
ExcuseSense AI - ML Model Training & Artifact Generation Pipeline
"""
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from app.core.config import settings
from app.ml.engine import preprocess_text

def train_and_export(dataset_path: str = None, model_path: str = None, vectorizer_path: str = None, metrics_path: str = None):
    dataset_path = dataset_path or settings.get_dataset_path()
    model_path = model_path or settings.get_model_path()
    vectorizer_path = vectorizer_path or settings.get_vectorizer_path()
    metrics_path = metrics_path or settings.get_metrics_path()

    print("=" * 60)
    print("      EXCUSESENSE AI - MODEL TRAINING PIPELINE")
    print("=" * 60)
    print(f"Loading dataset from: {dataset_path}")
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at: {dataset_path}")

    df = pd.read_csv(dataset_path)
    print(f"Total samples: {len(df)}")
    print(f"Class breakdown:\n{df['label'].value_counts().to_string()}\n")

    # 1. Clean and preprocess
    df["clean_text"] = df["text"].astype(str).apply(preprocess_text)

    # 2. Stratified train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"]
    )

    # 3. TF-IDF Vectorization
    print("Fitting TF-IDF Vectorizer (English stop words, sublinear TF)...")
    vectorizer = TfidfVectorizer(
        stop_words="english",
        sublinear_tf=True,
        ngram_range=(1, 2),
        min_df=1
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print(f"Vocabulary size: {len(vectorizer.vocabulary_)} tokens")

    # 4. Train Model
    print("Training Logistic Regression classifier (C=1.0, max_iter=1000)...")
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_vec, y_train)

    # 5. Evaluate
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)

    print("-" * 60)
    print(f"Evaluation Accuracy: {acc * 100:.2f}%")
    print(f"Confusion Matrix ({list(model.classes_)}):\n{cm}")
    print("\nClassification Report:\n" + report)
    print("-" * 60)

    # 6. Save Artifacts
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    with open(metrics_path, "w", encoding="utf-8") as f:
        f.write(str(round(acc, 4)))

    print(f"[OK] Saved model to: {model_path}")
    print(f"[OK] Saved vectorizer to: {vectorizer_path}")
    print(f"[OK] Saved metrics to: {metrics_path}")
    print("=" * 60)

    return {
        "accuracy": acc,
        "classes": list(model.classes_),
        "vocabulary_size": len(vectorizer.vocabulary_),
        "samples": len(df)
    }

if __name__ == "__main__":
    train_and_export()
