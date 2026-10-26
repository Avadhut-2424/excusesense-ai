"""
Unified Automated Test Suite Runner for ExcuseSense AI.
Runs all core tests across ML Inference, Keyword Attribution, API Endpoints,
Batch Processing, Database Persistence, and End-to-End Smoke Tests.
Tracks and reports exact execution duration and results.
"""

import os
import sys
import time
import subprocess

TEST_FILES = [
    "tests/test_ml_classifier.py",
    "tests/test_keyword_attribution.py",
    "tests/test_database.py",
    "tests/test_api_endpoints.py",
    "tests/test_batch_processing.py",
    "tests/test_end_to_end_smoke.py",
]

def main():
    print("=" * 72)
    print("        RUNNING CONSOLIDATED EXCUSESENSE AI TEST SUITE")
    print("=" * 72)
    print(f"Target test files ({len(TEST_FILES)} total):")
    for tf in TEST_FILES:
        print(f"  - {tf}")
    print("-" * 72)

    # Use current python executable
    cmd = [sys.executable, "-m", "pytest", "-v"] + TEST_FILES
    print(f"Executing: {' '.join(cmd)}\n", flush=True)

    t0 = time.time()
    result = subprocess.run(cmd)
    duration = time.time() - t0

    print("\n" + "=" * 72)
    print(f"EXCUSESENSE AI TEST SUITE FINISHED in {duration:.2f} seconds ({duration/60:.2f} minutes)")
    print(f"Exit Code: {result.returncode}")
    print("=" * 72)

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
