import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib

def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    return text

def main():
    # 1. Load dataset
    print("Loading dataset...")
    df = pd.read_csv('leave_applications.csv')
    
    # 2. Preprocess text
    df['clean_text'] = df['text'].apply(preprocess_text)
    
    # 3. Split dataset
    X_train, X_test, y_train, y_test = train_test_split(df['clean_text'], df['label'], test_size=0.2, random_state=42)
    
    # 4. Apply TF-IDF
    # Using scikit-learn's built-in english stop words list
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # 5. Train model
    print("Training Logistic Regression model...")
    model = LogisticRegression(random_state=42)
    model.fit(X_train_vec, y_train)
    
    # 6. Evaluate
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {acc:.2f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    # 7. Save model and vectorizer
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    
    # Save accuracy for displaying in UI
    with open("metrics.txt", "w") as f:
        f.write(str(acc))
        
    print("Model and vectorizer saved successfully.")

if __name__ == "__main__":
    main()
