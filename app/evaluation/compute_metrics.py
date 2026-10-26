"""
ExcuseSense AI - Empirical Evaluation & Benchmarking Suite
Calculates precision, recall, F1-scores, confusion matrix, and latency percentiles (P50, P90, P95, P99).
"""
import time
import json
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from app.core.config import settings
from app.ml.engine import classifier, preprocess_text

def run_evaluation_benchmark():
    print("=" * 70)
    print("        EXCUSESENSE AI - EMPIRICAL BENCHMARK & EVALUATION")
    print("=" * 70)

    clf = classifier()
    dataset_path = settings.get_dataset_path()
    df = pd.read_csv(dataset_path)

    print(f"Dataset: {dataset_path} ({len(df)} samples)")
    print(f"Target classes: {clf.classes}")

    # Latency benchmarking
    sample_texts = df["text"].tolist()
    latencies = []
    predictions = []

    for text in sample_texts:
        t0 = time.perf_counter()
        res = clf.predict(text)
        duration_ms = (time.perf_counter() - t0) * 1000.0
        latencies.append(duration_ms)
        predictions.append(res["prediction"])

    y_true = df["label"].tolist()
    y_pred = predictions

    acc = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred, labels=clf.classes)
    report_dict = classification_report(y_true, y_pred, output_dict=True)

    latencies = np.array(latencies)
    p50 = np.percentile(latencies, 50)
    p90 = np.percentile(latencies, 90)
    p95 = np.percentile(latencies, 95)
    p99 = np.percentile(latencies, 99)
    avg_latency = np.mean(latencies)

    print(f"\nOverall Accuracy: {acc * 100:.2f}%")
    print(f"\nLatency Benchmarks (ms per inference):")
    print(f"  - Average: {avg_latency:.3f} ms")
    print(f"  - P50 (Median): {p50:.3f} ms")
    print(f"  - P90: {p90:.3f} ms")
    print(f"  - P95: {p95:.3f} ms")
    print(f"  - P99: {p99:.3f} ms")

    print(f"\nConfusion Matrix ({clf.classes}):")
    print(cm)

    print("\nPer-class Metrics:")
    for cls_name in clf.classes:
        metrics = report_dict[cls_name]
        print(f"  [{cls_name}]: Precision={metrics['precision']:.3f}, Recall={metrics['recall']:.3f}, F1={metrics['f1-score']:.3f}, Support={metrics['support']}")

    print("=" * 70)
    return {
        "accuracy": acc,
        "classes": clf.classes,
        "confusion_matrix": cm.tolist(),
        "report": report_dict,
        "latency_ms": {
            "mean": round(float(avg_latency), 3),
            "p50": round(float(p50), 3),
            "p90": round(float(p90), 3),
            "p95": round(float(p95), 3),
            "p99": round(float(p99), 3),
        }
    }

if __name__ == "__main__":
    run_evaluation_benchmark()
