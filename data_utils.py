"""Reusable data-cleaning and scoring functions for the dashboard."""

import pandas as pd

REQUIRED_COLUMNS = [
    "student_id", "student_name", "class", "attendance_pct",
    "maths", "science", "english", "social", "computer",
]
SUBJECTS = ["maths", "science", "english", "social", "computer"]


def prepare_data(data: pd.DataFrame) -> pd.DataFrame:
    """Clean student records and calculate averages and the demo support flag.

    Invalid rows are dropped. Numeric values outside 0–100 are clipped.
    The support rule is illustrative only: attendance <75 OR average <40.
    """
    df = data.copy()
    for column in ["attendance_pct", *SUBJECTS]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(
        subset=["student_id", "student_name", "class", "attendance_pct", *SUBJECTS]
    )
    for column in ["attendance_pct", *SUBJECTS]:
        df[column] = df[column].clip(0, 100)

    for column in ["student_id", "student_name", "class"]:
        df[column] = df[column].astype(str).str.strip()

    df = df[
        (df["student_id"] != "")
        & (df["student_name"] != "")
        & (df["class"] != "")
    ].copy()

    df["average_score"] = df[SUBJECTS].mean(axis=1).round(1)
    df["support_needed"] = (df["attendance_pct"] < 75) | (df["average_score"] < 40)
    return df
