"""
B2 — ECDL Entropy-based Deception Classifier Prototype
=======================================================

Features (from B1 signal catalog):
  1. entropy_late_fraction — proportion of high-entropy tokens in 2nd half (p=3.8e-13)
  2. entropy_roughness — variance of token-level entropy (p<0.001)
  3. peak_entropy — max token entropy (p<0.001 after length control)
  4. spike_ratio — count of tokens above threshold (445x vs 33x)

Input: per-token logprobs from API (top-k, typically k=5..20)
Output: binary label (truthful / deceptive) + confidence

This script:
  1. Defines feature extraction from token-level logprobs
  2. Generates synthetic data matching known ECDL effect sizes
  3. Trains and evaluates a logistic regression classifier
  4. Reports accuracy, precision, recall, F1

To run on real data: provide JSON with per-response token logprobs
in format: [{"tokens": [...], "logprobs": [...], "label": 0|1}, ...]
"""

import numpy as np
from collections import namedtuple
import json
import sys

# --- Feature extraction ---

def token_entropy(logprobs_topk):
    """Compute entropy from top-k logprobs for a single token position.
    logprobs_topk: list of log-probabilities (negative values)
    """
    probs = np.exp(logprobs_topk)
    # Normalize to sum to 1 (approximate — missing mass outside top-k)
    total = probs.sum()
    if total <= 0:
        return 0.0
    probs = probs / total
    # Shannon entropy
    entropy = -np.sum(probs * np.log2(probs + 1e-12))
    return entropy


def extract_features(token_entropies):
    """Extract 4 features from a sequence of per-token entropies.

    Args:
        token_entropies: list/array of entropy values, one per generated token

    Returns:
        dict with 4 features
    """
    e = np.array(token_entropies)
    n = len(e)
    if n < 4:
        return None  # too short

    mid = n // 2
    median_e = np.median(e)

    # 1. Late fraction: proportion of above-median entropy in second half
    high_mask = e > median_e
    late_fraction = high_mask[mid:].mean() if n - mid > 0 else 0.5

    # 2. Roughness: std of first-differences (how "jagged" the profile is)
    diffs = np.diff(e)
    roughness = np.std(diffs) if len(diffs) > 0 else 0.0

    # 3. Peak entropy
    peak = np.max(e)

    # 4. Spike ratio: fraction of tokens with entropy > 2*median
    threshold = 2.0 * median_e if median_e > 0 else 1.0
    spike_ratio = (e > threshold).mean()

    return {
        "late_fraction": float(late_fraction),
        "roughness": float(roughness),
        "peak_entropy": float(peak),
        "spike_ratio": float(spike_ratio),
    }


# --- Synthetic data generator (calibrated to ECDL effect sizes) ---

def generate_synthetic_data(n_samples=500, seq_len=50, seed=42):
    """Generate synthetic entropy profiles matching known ECDL effects.

    Truthful profiles: smooth, low entropy, front-loaded uncertainty.
    Deceptive profiles: rough, high entropy, late-loaded uncertainty.

    Effect sizes calibrated to sprint results:
      - Late fraction shift: +0.408 (p=3.8e-13)
      - Spike ratio: 445x vs 33x (≈13.5x ratio)
      - Peak entropy: significantly higher under deception
    """
    rng = np.random.RandomState(seed)
    data = []

    for i in range(n_samples):
        label = i % 2  # 0=truthful, 1=deceptive

        if label == 0:  # Truthful
            # Base entropy: low, smooth, slightly decreasing
            base = 1.0 + 0.3 * rng.randn()
            decay = np.linspace(0, -0.3, seq_len)
            noise = 0.1 * rng.randn(seq_len)
            entropies = base + decay + noise
            # Occasional small spikes
            n_spikes = rng.poisson(2)
            for _ in range(n_spikes):
                pos = rng.randint(0, seq_len)
                entropies[pos] += rng.exponential(0.5)
        else:  # Deceptive
            # Base entropy: higher, rougher, increasing toward end
            base = 1.8 + 0.5 * rng.randn()
            # Late-loaded: entropy increases in second half
            ramp = np.concatenate([
                np.zeros(seq_len // 2),
                np.linspace(0, 1.5, seq_len - seq_len // 2)
            ])
            noise = 0.3 * rng.randn(seq_len)
            entropies = base + ramp + noise
            # More frequent, larger spikes
            n_spikes = rng.poisson(8)
            for _ in range(n_spikes):
                pos = rng.randint(seq_len // 3, seq_len)  # bias toward end
                entropies[pos] += rng.exponential(1.5)

        entropies = np.maximum(entropies, 0.01)  # entropy >= 0
        features = extract_features(entropies)
        if features:
            features["label"] = label
            data.append(features)

    return data


# --- Classifier ---

def train_evaluate(data, test_fraction=0.2, seed=42):
    """Train logistic regression on extracted features, report metrics."""
    rng = np.random.RandomState(seed)

    # Shuffle
    indices = np.arange(len(data))
    rng.shuffle(indices)
    split = int(len(data) * (1 - test_fraction))

    feature_names = ["late_fraction", "roughness", "peak_entropy", "spike_ratio"]
    X = np.array([[d[f] for f in feature_names] for d in data])
    y = np.array([d["label"] for d in data])

    X_train, X_test = X[indices[:split]], X[indices[split:]]
    y_train, y_test = y[indices[:split]], y[indices[split:]]

    # Standardize
    mu = X_train.mean(axis=0)
    sigma = X_train.std(axis=0) + 1e-8
    X_train_s = (X_train - mu) / sigma
    X_test_s = (X_test - mu) / sigma

    # Logistic regression (manual — no sklearn dependency)
    w = np.zeros(X_train_s.shape[1])
    b = 0.0
    lr = 0.1
    for epoch in range(200):
        z = X_train_s @ w + b
        pred = 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
        grad_w = X_train_s.T @ (pred - y_train) / len(y_train)
        grad_b = (pred - y_train).mean()
        w -= lr * grad_w
        b -= lr * grad_b

    # Evaluate
    z_test = X_test_s @ w + b
    pred_test = 1.0 / (1.0 + np.exp(-np.clip(z_test, -500, 500)))
    y_pred = (pred_test > 0.5).astype(int)

    tp = ((y_pred == 1) & (y_test == 1)).sum()
    fp = ((y_pred == 1) & (y_test == 0)).sum()
    fn = ((y_pred == 0) & (y_test == 1)).sum()
    tn = ((y_pred == 0) & (y_test == 0)).sum()

    accuracy = (tp + tn) / len(y_test)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    # Feature importance (absolute weights on standardized features)
    importance = list(zip(feature_names, np.abs(w), w))
    importance.sort(key=lambda x: -x[1])

    return {
        "n_train": len(y_train),
        "n_test": len(y_test),
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "confusion": {"tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn)},
        "feature_importance": [(name, round(abs_w, 4), round(raw_w, 4))
                               for name, abs_w, raw_w in importance],
    }


# --- Main ---

def main():
    print("=" * 60)
    print("ECDL Entropy Classifier — B2 Prototype")
    print("=" * 60)

    # Check for real data file argument
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
        print(f"\nLoading real data from: {data_file}")
        with open(data_file) as f:
            raw = json.load(f)
        data = []
        for item in raw:
            entropies = [token_entropy(lp) for lp in item["logprobs"]]
            features = extract_features(entropies)
            if features:
                features["label"] = item["label"]
                data.append(features)
        print(f"Extracted features from {len(data)} responses")
    else:
        print("\nNo data file provided — using synthetic data")
        print("(calibrated to ECDL sprint effect sizes)")
        data = generate_synthetic_data(n_samples=500)
        print(f"Generated {len(data)} synthetic samples")

    # Show feature distributions
    print("\n--- Feature Distributions ---")
    for label_name, label_val in [("Truthful", 0), ("Deceptive", 1)]:
        subset = [d for d in data if d["label"] == label_val]
        print(f"\n{label_name} (n={len(subset)}):")
        for feat in ["late_fraction", "roughness", "peak_entropy", "spike_ratio"]:
            vals = [d[feat] for d in subset]
            print(f"  {feat:20s}: mean={np.mean(vals):.4f}  std={np.std(vals):.4f}")

    # Train and evaluate
    print("\n--- Classification Results ---")
    results = train_evaluate(data)
    print(f"Train: {results['n_train']}  Test: {results['n_test']}")
    print(f"Accuracy:  {results['accuracy']}")
    print(f"Precision: {results['precision']}")
    print(f"Recall:    {results['recall']}")
    print(f"F1:        {results['f1']}")
    print(f"\nConfusion matrix:")
    cm = results["confusion"]
    print(f"  TP={cm['tp']}  FP={cm['fp']}")
    print(f"  FN={cm['fn']}  TN={cm['tn']}")
    print(f"\nFeature importance (|weight| on standardized features):")
    for name, abs_w, raw_w in results["feature_importance"]:
        direction = "↑ deceptive" if raw_w > 0 else "↑ truthful"
        print(f"  {name:20s}: {abs_w:.4f}  ({direction})")

    print("\n" + "=" * 60)
    print("To run on real data:")
    print('  python B2_entropy_classifier.py data.json')
    print('  Format: [{"logprobs": [[lp1,lp2,...], ...], "label": 0|1}, ...]')
    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
