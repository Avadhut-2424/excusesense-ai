import os
import re
from typing import Dict, List, Tuple, Any, Optional
import joblib
import numpy as np
from app.core.config import settings

def preprocess_text(text: str) -> str:
    """Standardize text by lowercasing and removing punctuation."""
    if not text:
        return ""
    text = text.lower()
    return re.sub(r"[^\w\s]", "", text).strip()

class ExcuseSenseClassifier:
    """
    Core Machine Learning classification & explainability engine for ExcuseSense AI.
    Handles inference, probability calibration, and feature attribution.
    """
    _instance: Optional["ExcuseSenseClassifier"] = None

    def __init__(self, model_path: Optional[str] = None, vectorizer_path: Optional[str] = None, metrics_path: Optional[str] = None):
        self.model_path = model_path or settings.get_model_path()
        self.vectorizer_path = vectorizer_path or settings.get_vectorizer_path()
        self.metrics_path = metrics_path or settings.get_metrics_path()
        
        self.model = None
        self.vectorizer = None
        self.accuracy: float = 1.0
        self.classes: List[str] = []
        self.load_artifacts()

    @classmethod
    def get_instance(cls) -> "ExcuseSenseClassifier":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_artifacts(self) -> None:
        """Load trained scikit-learn model and TF-IDF vectorizer."""
        if not os.path.exists(self.model_path) or not os.path.exists(self.vectorizer_path):
            raise FileNotFoundError(
                f"Model or vectorizer artifact missing at {self.model_path} / {self.vectorizer_path}. "
                "Run `python -m app.ml.train` or `train_model.py` first."
            )

        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)
        self.classes = list(self.model.classes_)

        if os.path.exists(self.metrics_path):
            try:
                with open(self.metrics_path, "r", encoding="utf-8") as f:
                    self.accuracy = float(f.read().strip())
            except Exception:
                self.accuracy = 1.0
        else:
            self.accuracy = 1.0

    def compute_keyword_attributions(self, raw_text: str, class_idx: int, top_n: int = 6) -> List[Dict[str, Any]]:
        """
        Computes Explainable AI (XAI) feature attributions.
        Identifies words in the text that positively contribute to the target class decision.
        """
        clean = preprocess_text(raw_text)
        words = clean.split()
        if not words or self.model is None or self.vectorizer is None:
            return []

        coef = self.model.coef_[class_idx]
        vocab = self.vectorizer.vocabulary_
        seen = set()
        scored_keywords: List[Tuple[str, float]] = []

        for w in words:
            if w in seen or w not in vocab:
                continue
            seen.add(w)
            token_idx = vocab[w]
            weight = float(coef[token_idx])
            if weight > 0:
                scored_keywords.append((w, round(weight, 4)))

        # Sort descending by influence weight
        scored_keywords.sort(key=lambda x: x[1], reverse=True)
        return [{"word": w, "weight": weight} for w, weight in scored_keywords[:top_n]]

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Run inference on a single leave application string.
        Returns prediction, calibrated confidence, class probabilities, and XAI keyword attributions.
        """
        cleaned_text = preprocess_text(text)
        if not cleaned_text:
            raise ValueError("Input application text cannot be empty or solely punctuation.")

        vec_input = self.vectorizer.transform([cleaned_text])
        prediction = str(self.model.predict(vec_input)[0])
        probs = self.model.predict_proba(vec_input)[0]

        class_idx = self.classes.index(prediction)
        confidence = float(probs[class_idx])

        attributions = self.compute_keyword_attributions(text, class_idx, top_n=6)
        top_keywords = [item["word"] for item in attributions]

        prob_dict = {
            cls_name: round(float(p), 4)
            for cls_name, p in zip(self.classes, probs)
        }

        # Determine risk assessment and recommendation
        risk_level = "low"
        recommendation = "Approved - Legitimate leave application."
        if prediction == "Suspicious":
            risk_level = "high"
            recommendation = "Audit Recommended - Unusual or unverifiable justification flagged."
        elif prediction == "Emotional":
            risk_level = "medium"
            recommendation = "Empathetic Support - Wellness/Mental health check-in advised."

        return {
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "probabilities": prob_dict,
            "keywords": top_keywords,
            "attributions": attributions,
            "risk_level": risk_level,
            "recommendation": recommendation,
        }

    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Run batch inference over a list of applications."""
        return [self.predict(t) for t in texts]

# Export singleton accessor
classifier = ExcuseSenseClassifier.get_instance
