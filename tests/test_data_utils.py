import unittest
from pathlib import Path

import pandas as pd

from data_utils import REQUIRED_COLUMNS, prepare_data

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "sample_students.csv"


class PrepareDataTests(unittest.TestCase):
    def test_sample_dataset_has_required_columns_and_20_rows(self):
        sample = pd.read_csv(DATA_FILE)
        self.assertTrue(set(REQUIRED_COLUMNS).issubset(sample.columns))
        self.assertEqual(len(sample), 20)

    def test_average_score_is_calculated(self):
        row = {
            "student_id": "T001", "student_name": "Test", "class": "10-A",
            "attendance_pct": 80, "maths": 80, "science": 70,
            "english": 90, "social": 60, "computer": 100,
        }
        result = prepare_data(pd.DataFrame([row]))
        self.assertEqual(result.iloc[0]["average_score"], 80.0)

    def test_low_attendance_flags_student(self):
        row = {
            "student_id": "T002", "student_name": "Test", "class": "10-A",
            "attendance_pct": 74.9, "maths": 80, "science": 80,
            "english": 80, "social": 80, "computer": 80,
        }
        result = prepare_data(pd.DataFrame([row]))
        self.assertTrue(bool(result.iloc[0]["support_needed"]))

    def test_low_average_flags_student(self):
        row = {
            "student_id": "T003", "student_name": "Test", "class": "10-A",
            "attendance_pct": 90, "maths": 30, "science": 30,
            "english": 30, "social": 30, "computer": 30,
        }
        result = prepare_data(pd.DataFrame([row]))
        self.assertTrue(bool(result.iloc[0]["support_needed"]))

    def test_invalid_numeric_row_is_removed(self):
        row = {
            "student_id": "T004", "student_name": "Test", "class": "10-A",
            "attendance_pct": "not a number", "maths": 70, "science": 70,
            "english": 70, "social": 70, "computer": 70,
        }
        result = prepare_data(pd.DataFrame([row]))
        self.assertTrue(result.empty)

    def test_marks_and_attendance_are_clipped_to_range(self):
        row = {
            "student_id": "T005", "student_name": "Test", "class": "10-A",
            "attendance_pct": 120, "maths": 110, "science": -5,
            "english": 70, "social": 70, "computer": 70,
        }
        result = prepare_data(pd.DataFrame([row]))
        self.assertEqual(result.iloc[0]["attendance_pct"], 100)
        self.assertEqual(result.iloc[0]["maths"], 100)
        self.assertEqual(result.iloc[0]["science"], 0)

if __name__ == "__main__":
    unittest.main()
