"""Reconstructed AutoGluon experiment from the 2023 project writeup."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


EXPECTED = {
    "age", "gender", "height", "weight", "ap_hi", "ap_lo", "cholesterol",
    "gluc", "smoke", "alco", "active", "cardio",
}


def load_data(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path, sep=";")
    missing = EXPECTED - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    if data[list(EXPECTED)].isna().any().any():
        raise ValueError("The required columns contain missing values")
    if set(data["cardio"].unique()) != {0, 1}:
        raise ValueError("cardio must contain both binary labels 0 and 1")
    data = data.drop(columns=["id"], errors="ignore")
    data["age"] = data["age"] / 365
    return data


def run(data_path: Path, output: Path, time_limit: int, preset: str) -> None:
    output.mkdir(parents=True, exist_ok=True)
    data = load_data(data_path)
    train, test = train_test_split(
        data, test_size=0.2, random_state=42, stratify=data["cardio"]
    )
    predictor = TabularPredictor(
        label="cardio", problem_type="binary", eval_metric="accuracy",
        path=str(output / "model"),
    ).fit(train_data=train, time_limit=time_limit, presets=preset)
    predictions = predictor.predict(test.drop(columns=["cardio"]))
    labels = test["cardio"]
    metrics = {
        "accuracy": accuracy_score(labels, predictions),
        "train_rows": len(train),
        "test_rows": len(test),
        "time_limit_seconds": time_limit,
        "preset": preset,
    }
    (output / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    (output / "classification_report.txt").write_text(
        classification_report(labels, predictions, zero_division=0)
    )
    pd.DataFrame(
        confusion_matrix(labels, predictions, labels=[0, 1]),
        index=["actual_0", "actual_1"], columns=["predicted_0", "predicted_1"],
    ).to_csv(output / "confusion_matrix.csv")
    predictor.leaderboard(test, silent=True).to_csv(output / "leaderboard.csv", index=False)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--time-limit", type=int, default=200)
    parser.add_argument("--preset", default="medium_quality")
    args = parser.parse_args()
    run(args.data, args.output, args.time_limit, args.preset)
