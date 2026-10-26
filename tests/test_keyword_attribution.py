import pytest
from app.ml.engine import classifier

@pytest.fixture
def clf():
    return classifier()

def test_keyword_attribution_fidelity(clf):
    text = "Doctor prescribed antibiotics for severe viral fever and clinic visit."
    class_idx = clf.classes.index("Genuine")
    attributions = clf.compute_keyword_attributions(text, class_idx, top_n=5)
    
    assert isinstance(attributions, list)
    assert len(attributions) > 0
    for item in attributions:
        assert "word" in item
        assert "weight" in item
        assert item["weight"] > 0

    words = [a["word"] for a in attributions]
    assert any(w in words for w in ["fever", "doctor", "clinic", "severe", "viral"])

def test_attribution_ordering(clf):
    text = "Feeling severe burnout and emotional stress depression."
    class_idx = clf.classes.index("Emotional")
    attributions = clf.compute_keyword_attributions(text, class_idx, top_n=5)
    
    # Check descending order
    weights = [a["weight"] for a in attributions]
    assert weights == sorted(weights, reverse=True)
