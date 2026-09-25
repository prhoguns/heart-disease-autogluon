# Heart disease prediction with AutoGluon

**Original post:** [Machine Learning Model to Predict Heart Disease](https://rhoguns.hashnode.dev/machine-learning-model-to-predict-heart-disease)

**Original article in this repo:** [Read the archived text and screenshots](docs/original-post.md)

This repository reconstructs the project described in [Machine Learning Model to Predict Heart Disease](https://rhoguns.hashnode.dev/machine-learning-model-to-predict-heart-disease), published **March 23, 2023**. The original repository was lost; these files were recreated on September 24, 2026 from the article and its screenshots. This is a reconstruction, not the original source or trained model. Git commits use their actual creation date.

The original experiment used the [Kaggle Cardiovascular Disease Dataset](https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset), a semicolon-delimited CSV with 70,000 rows. It removed `id`, converted `age` from days to years, reserved 20% for testing with `random_state=0`, trained an AutoGluon binary classifier for `cardio`, and reviewed a leaderboard, confusion matrix and classification report. The screenshot shows an AutoGluon `medium_quality_faster_train` preset with a 200-second limit. The reconstructed script uses its newer `medium_quality` name.

The [original post images and notes](docs/project-notes.md) preserve the setup, exploratory charts, training output and reported 2023 test results.

## Run

1. Download the dataset from Kaggle and put `cardio_train.csv` in `data/` (or pass its path). Dataset and trained models are intentionally untracked.
2. Create a Python environment and install `requirements.txt`. AutoGluon has platform and Python-version constraints; use a version supported by your system.
3. Run:

```sh
python train.py --data data/cardio_train.csv --output results
```

Outputs include `metrics.json`, `classification_report.txt`, `confusion_matrix.csv`, `leaderboard.csv`, and an AutoGluon model directory. `--time-limit` and `--preset` can be changed. The script validates expected columns and the binary label before training.

This is a learning exercise and is not a clinical diagnostic tool. No clinical validation or prospective testing is documented in the original article.
