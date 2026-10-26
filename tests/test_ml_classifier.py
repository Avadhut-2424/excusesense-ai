import pytest
from app.ml.engine import classifier, preprocess_text

@pytest.fixture
def clf():
    return classifier()

def test_preprocess_text():
    raw = "Hello! I am feeling UNWELL... due to acute bronchitis???"
    clean = preprocess_text(raw)
    assert clean == "hello i am feeling unwell due to acute bronchitis"
    assert preprocess_text("") == ""
    assert preprocess_text("!!!???") == ""

def test_classifier_artifacts_loaded(clf):
    assert clf.model is not None
    assert clf.vectorizer is not None
    assert len(clf.classes) == 3
    assert set(clf.classes) == {"Genuine", "Emotional", "Suspicious"}

def test_predict_genuine_leave(clf):
    text = "I have a high fever and doctor advised two days of strict bed rest."
    res = clf.predict(text)
    assert res["prediction"] == "Genuine"
    assert 0.0 <= res["confidence"] <= 1.0
    assert "Genuine" in res["probabilities"]
    assert res["risk_level"] == "low"
    assert len(res["keywords"]) > 0

def test_predict_suspicious_leave(clf):
    text = "My fish ate my car keys so I cannot commute to the office today."
    res = clf.predict(text)
    assert res["prediction"] == "Suspicious"
    assert res["risk_level"] == "high"
    assert "Audit Recommended" in res["recommendation"]

def test_predict_emotional_leave(clf):
    text = "I am taking a mental health day to prioritize my emotional well-being and stress recovery."
    res = clf.predict(text)
    assert res["prediction"] == "Emotional"
    assert res["risk_level"] == "medium"

def test_empty_input_raises_value_error(clf):
    with pytest.raises(ValueError):
        clf.predict("   ")
    with pytest.raises(ValueError):
        clf.predict("!@#$$%^^&*")
