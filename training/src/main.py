import argparse
import json
import os.path
import re
import subprocess
from typing import List

from joblib import dump
from sklearn.datasets import fetch_20newsgroups
from sklearn.dummy import DummyClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.utils._testing import ignore_warnings


@ignore_warnings(category=ConvergenceWarning)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="Directory for model artifacts")
    parser.add_argument("output_requirements_txt", help="requirements.txt file to update with specific version numbers for this model")
    args = parser.parse_args()

    training_data = fetch_20newsgroups(subset="train")
    testing_data = fetch_20newsgroups(subset="test")

    training_data.target = [training_data.target_names[t] for t in training_data.target]
    testing_data.target = [testing_data.target_names[t] for t in testing_data.target]

    model = make_pipeline(
        TfidfVectorizer(min_df=30, ngram_range=(1, 2), sublinear_tf=True),
        LogisticRegressionCV()
    )

    baseline_model = make_pipeline(
        TfidfVectorizer(min_df=0.1),
        DummyClassifier(strategy="most_frequent")
    )

    model.fit(training_data.data, training_data.target)

    predictions = model.predict(testing_data.data)
    test_accuracy = accuracy_score(testing_data.target, predictions)
    baseline_accuracy = accuracy_score(testing_data.target,
                                       baseline_model.fit(training_data.data, training_data.target).predict(
                                           testing_data.target))

    with open(os.path.join(args.output_dir, "training_report.md"), "w") as key_stats:
        key_stats.write(f"""
# Evaluation on test set
    Model: {test_accuracy:.1%}
    Baseline / predict majority: {baseline_accuracy:.1%}

# Data info
    Training rows: {len(training_data.data):,}
    Testing rows: {len(testing_data.data):,}
        """)

    dump(model, os.path.join(args.output_dir, "model.joblib.gz"), compress=9)
    freeze_model_file_requirements(args.output_requirements_txt, ["scikit-learn", "joblib"])

    with open(os.path.join(args.output_dir, "metrics.json"), "w") as json_out:
        json.dump({
            "accuracy": test_accuracy,
            "baseline": {
                "accuracy": baseline_accuracy
            },
            "training_rows": len(training_data.data),
            "testing_rows": len(testing_data.data)
        }, json_out, sort_keys=True, indent=3)


def freeze_model_file_requirements(requirements_file: str, package_prefixes: List[str]):
    """
    Save the versions of packages matching the prefixes into the requirements file.
    This is used to ensure that the serving code is using the same versions
    of any packages that are used to save and load the model.
    """
    # get the frozen requirements that match the prefix
    result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE)
    requirements_text = result.stdout.decode("utf8")

    package_pattern = re.compile(fr"^({'|'.join(package_prefixes)}).*", flags=re.IGNORECASE)

    lines = requirements_text.split("\n")
    lines = [line for line in lines if package_pattern.match(line)]

    # get everything else
    with open(requirements_file, "r") as requirements_in:
        for line in requirements_in:
            if not package_pattern.match(line):
                lines.append(line.strip())

    # merge them into the new file
    requirements_file_new = requirements_file + ".new"
    with open(requirements_file_new, "w") as requirements_out:
        for line in sorted(lines):
            requirements_out.write(line + "\n")

    subprocess.run(["mv", requirements_file_new, requirements_file])


if __name__ == "__main__":
    main()
