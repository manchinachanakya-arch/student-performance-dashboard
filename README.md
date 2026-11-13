# Student Performance Analytics Dashboard

A beginner-friendly Streamlit project for exploring student marks and attendance. It includes class filters, subject averages, an attendance-versus-score chart, a support list, CSV upload, and filtered CSV download.

## Features

- KPI cards for student count, average marks, attendance, and support flags
- Filter records by class
- Upload your own CSV file
- Subject-wise average marks chart
- Attendance vs. average-score scatter plot
- Demo support rule: attendance below 75% **or** average marks below 40%
- Download the filtered records as CSV

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (recommended):

   **Windows PowerShell**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

Streamlit will print a local URL (usually http://localhost:8501).

## Run the automated tests

From this folder, run:

```bash
python -m unittest discover -s tests -v
```

The tests cover sample-data structure, average-score calculation, both support-flag conditions, invalid numeric rows, and value-range handling.

## Project structure

- `app.py` — Streamlit interface and charts
- `data_utils.py` — reusable data cleaning and scoring logic
- `data/sample_students.csv` — fictional sample records
- `tests/test_data_utils.py` — automated unit tests

## CSV format

Your CSV must contain these columns:

`student_id, student_name, class, attendance_pct, maths, science, english, social, computer`

Marks and attendance should be numeric values from 0 to 100. See `data/sample_students.csv` for an example.

## Important note

The included data is fictional sample data. The support rule is an illustrative demo rule, not a validated educational or clinical assessment. Do not use this prototype to make consequential decisions about real students without appropriate review.

## Current status

Initial portfolio prototype. Run it locally, test with the included sample CSV and another valid CSV, and review/understand the code before describing it as a completed project in an internship application.
