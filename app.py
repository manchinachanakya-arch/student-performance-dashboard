from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from data_utils import REQUIRED_COLUMNS, SUBJECTS, prepare_data

st.set_page_config(page_title="Student Performance Analytics", page_icon="📊", layout="wide")

DATA_FILE = Path(__file__).parent / "data" / "sample_students.csv"


@st.cache_data
def load_sample_data():
    return pd.read_csv(DATA_FILE)


st.title("📊 Student Performance Analytics")
st.caption("A simple dashboard to explore marks, attendance, and students who may need support.")

with st.sidebar:
    st.header("Data")
    uploaded_file = st.file_uploader("Upload a student CSV", type=["csv"])
    st.caption("Required columns: student_id, student_name, class, attendance_pct, maths, science, english, social, computer")
    st.divider()
    st.header("Filters")

try:
    raw_df = pd.read_csv(uploaded_file) if uploaded_file else load_sample_data()
except (pd.errors.ParserError, UnicodeDecodeError, OSError, ValueError) as exc:
    st.error(f"Could not read the CSV file: {exc}")
    st.stop()

missing = sorted(set(REQUIRED_COLUMNS) - set(raw_df.columns))
if missing:
    st.error("Your CSV is missing required columns: " + ", ".join(missing))
    st.stop()

df = prepare_data(raw_df)
if df.empty:
    st.warning("No valid student rows were found. Check that student details are present and marks and attendance are numeric values from 0 to 100.")
    st.stop()

classes = sorted(df["class"].unique())
with st.sidebar:
    selected_classes = st.multiselect("Choose class(es)", classes, default=classes)
    show_support_only = st.checkbox("Show students needing support only")

filtered = df[df["class"].isin(selected_classes)]
if show_support_only:
    filtered = filtered[filtered["support_needed"]]

if filtered.empty:
    st.info("No students match the selected filters.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Students", f"{len(filtered):,}")
c2.metric("Average score", f"{filtered['average_score'].mean():.1f}%")
c3.metric("Average attendance", f"{filtered['attendance_pct'].mean():.1f}%")
c4.metric("Need support", f"{int(filtered['support_needed'].sum()):,}")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Average score by subject")
    subject_means = filtered[SUBJECTS].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 4))
    subject_means.plot(kind="bar", ax=ax)
    ax.set_ylabel("Average marks (%)")
    ax.set_ylim(0, 100)
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Attendance vs average score")
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = filtered["support_needed"].map({True: "#d95f02", False: "#1b9e77"})
    ax.scatter(filtered["attendance_pct"], filtered["average_score"], c=colors, alpha=0.75)
    ax.axvline(75, linestyle="--", linewidth=1, label="75% attendance threshold")
    ax.axhline(40, linestyle=":", linewidth=1, label="40% average threshold")
    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Average score (%)")
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 105)
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.subheader("Students needing support")
support = filtered[filtered["support_needed"]].copy()
if support.empty:
    st.success("No students are flagged by the demo rule in the current filter.")
else:
    support["reason"] = support.apply(
        lambda row: ", ".join(
            reason for condition, reason in [
                (row["attendance_pct"] < 75, "Attendance below 75%"),
                (row["average_score"] < 40, "Average below 40%"),
            ] if condition
        ), axis=1
    )
    st.dataframe(
        support[["student_id", "student_name", "class", "attendance_pct", "average_score", "reason"]]
        .sort_values(["average_score", "attendance_pct"]),
        use_container_width=True,
        hide_index=True,
    )

st.subheader("Student records")
display_columns = ["student_id", "student_name", "class", "attendance_pct", *SUBJECTS, "average_score", "support_needed"]
st.dataframe(filtered[display_columns].sort_values("average_score", ascending=False), use_container_width=True, hide_index=True)

csv_bytes = filtered[display_columns].to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered data (CSV)", data=csv_bytes, file_name="student_performance_filtered.csv", mime="text/csv")

st.caption("Demo rule only: a student is flagged when attendance is below 75% OR average marks are below 40%. This is an illustrative prototype, not an official academic assessment.")
