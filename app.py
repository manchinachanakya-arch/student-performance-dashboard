from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from data_utils import REQUIRED_COLUMNS, SUBJECTS, prepare_data

st.set_page_config(
    page_title="Student Performance | Analytics Studio",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path(__file__).parent / "data" / "sample_students.csv"

# Premium dark interface
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #eaf0f8;
        --muted: #8d9bb0;
        --panel: #111d2d;
        --panel-2: #152338;
        --line: rgba(157, 181, 211, .13);
        --cyan: #76d6d0;
        --blue: #8daeff;
    }
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background:
          radial-gradient(ellipse at 85% 0%, rgba(55, 104, 145, .17), transparent 34%),
          linear-gradient(145deg, #08111e 0%, #0b1523 52%, #0d1929 100%);
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: rgba(8, 17, 30, .82); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1928 0%, #101f31 100%);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] * { color: #dce6f3; }
    [data-testid="stSidebar"] .stCaption { color: #8d9bb0; }
    .block-container { padding-top: 2.1rem; padding-bottom: 3rem; max-width: 1440px; }
    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        letter-spacing: -0.035em;
        color: #f2f6fc !important;
    }
    h1 { font-size: clamp(2rem, 3vw, 2.8rem) !important; font-weight: 800 !important; }
    h2 { font-size: 1.28rem !important; font-weight: 700 !important; }
    h3 { font-size: 1.02rem !important; font-weight: 700 !important; }
    p, label, .stMarkdown { color: #c3cfde; }
    .eyebrow {
        color: var(--cyan); text-transform: uppercase; letter-spacing: .18em;
        font-size: .69rem; font-weight: 700; margin-bottom: .55rem;
    }
    .hero-subtitle { color: #93a3b8; font-size: .96rem; margin-top: -.55rem; }
    .topline {
        display:flex; justify-content:space-between; align-items:center;
        gap:12px; margin-bottom: 1.35rem;
    }
    .brandmark {
        display:flex; align-items:center; gap:10px; color:#eaf0f8;
        font-family:'Manrope',sans-serif; font-weight:800; letter-spacing:.02em;
    }
    .brand-icon {
        width:34px; height:34px; border-radius:11px; display:grid; place-items:center;
        background:linear-gradient(135deg,#8daeff,#76d6d0); color:#091524;
        font-size:18px; box-shadow:0 6px 24px rgba(118,214,208,.16);
    }
    .live-pill {
        border:1px solid rgba(118,214,208,.25); background:rgba(118,214,208,.08);
        color:#9ce7df; border-radius:99px; padding:6px 11px;
        font-size:.72rem; font-weight:600; letter-spacing:.03em;
    }
    .metric-card {
        background:linear-gradient(145deg, rgba(23,39,59,.96), rgba(15,28,44,.96));
        border:1px solid var(--line); border-radius:16px; padding:18px 19px 16px;
        min-height:122px; box-shadow:0 12px 34px rgba(0,0,0,.13);
    }
    .metric-label { color:#91a1b7; font-size:.75rem; font-weight:600; letter-spacing:.04em; }
    .metric-value {
        color:#f3f7fc; font-family:'Manrope',sans-serif; font-weight:800;
        font-size:1.85rem; letter-spacing:-.055em; margin-top:7px; line-height:1.15;
    }
    .metric-note { color:#71839b; font-size:.7rem; margin-top:8px; }
    .section-kicker {
        color:#7e91a9; text-transform:uppercase; letter-spacing:.15em;
        font-size:.67rem; font-weight:700; margin-bottom:5px;
    }
    .panel {
        background:rgba(17,29,45,.76); border:1px solid var(--line);
        border-radius:17px; padding:17px 18px 10px; min-height:100%;
    }
    div[data-testid="stDataFrame"] {
        border:1px solid var(--line); border-radius:13px; overflow:hidden;
    }
    .stButton button, .stDownloadButton button {
        border-radius:10px; border:1px solid rgba(141,174,255,.35);
        background:linear-gradient(135deg,#8daeff,#76d6d0);
        color:#091524; font-weight:700; padding:.55rem 1rem;
    }
    .stButton button:hover, .stDownloadButton button:hover {
        border-color:#b6c9ff; color:#071321; filter:brightness(1.06);
    }
    [data-testid="stFileUploader"] {
        background:rgba(255,255,255,.025); border:1px dashed rgba(141,174,255,.3);
        border-radius:12px; padding:8px;
    }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div {
        background:#142338 !important; border-color:var(--line) !important;
    }
    hr { border-color:var(--line) !important; }
    .footnote { color:#71839b; font-size:.72rem; line-height:1.5; }
    @media (max-width: 700px) {
        .block-container { padding:1.1rem 1rem 2rem; }
        .metric-card { min-height:105px; padding:14px; }
        .metric-value { font-size:1.55rem; }
        .topline { align-items:flex-start; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_sample_data():
    return pd.read_csv(DATA_FILE)


with st.sidebar:
    st.markdown(
        '<div class="brandmark"><div class="brand-icon">◈</div><div>INSIGHT<span style="color:#76d6d0"> / </span>EDU</div></div>',
        unsafe_allow_html=True,
    )
    st.caption("STUDENT INTELLIGENCE PLATFORM")
    st.divider()
    st.markdown("#### DATA SOURCE")
    uploaded_file = st.file_uploader("Import student records", type=["csv"])
    st.caption(
        "CSV fields: student_id, student_name, class, attendance_pct, "
        "maths, science, english, social, computer"
    )
    st.divider()
    st.markdown("#### FILTERS")
    st.caption("Filters update all insights instantly.")

try:
    raw_df = pd.read_csv(uploaded_file) if uploaded_file else load_sample_data()
except (pd.errors.ParserError, UnicodeDecodeError, OSError, ValueError) as exc:
    st.error(f"Unable to read this CSV: {exc}")
    st.stop()

missing = sorted(set(REQUIRED_COLUMNS) - set(raw_df.columns))
if missing:
    st.error("Missing required columns: " + ", ".join(missing))
    st.stop()

df = prepare_data(raw_df)
if df.empty:
    st.warning(
        "No valid student records were found. Check that student details are present "
        "and marks and attendance are numeric values from 0 to 100."
    )
    st.stop()

classes = sorted(df["class"].unique())
with st.sidebar:
    selected_classes = st.multiselect("Class groups", classes, default=classes)
    show_support_only = st.checkbox("Only show students flagged for support")

filtered = df[df["class"].isin(selected_classes)]
if show_support_only:
    filtered = filtered[filtered["support_needed"]]

source_label = "LIVE CSV IMPORT" if uploaded_file else "DEMO DATASET"

st.markdown(
    f'<div class="topline"><div class="brandmark"><div class="brand-icon">◈</div>'
    f'<div>INSIGHT / EDU</div></div><div class="live-pill">● {source_label}</div></div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="eyebrow">ACADEMIC PERFORMANCE OVERVIEW</div>', unsafe_allow_html=True)
st.title("Student analytics")
st.markdown(
    '<div class="hero-subtitle">A clearer view of achievement, attendance and students who may need attention.</div>',
    unsafe_allow_html=True,
)

if filtered.empty:
    st.info("No students match the selected filters. Adjust your class or support filters.")
    st.stop()

st.write("")
avg_score = filtered["average_score"].mean()
avg_attendance = filtered["attendance_pct"].mean()
support_count = int(filtered["support_needed"].sum())
metrics = [
    ("TOTAL STUDENTS", f"{len(filtered):,}", "Records in current view"),
    ("AVERAGE SCORE", f"{avg_score:.1f}%", "Across all five subjects"),
    ("ATTENDANCE RATE", f"{avg_attendance:.1f}%", "Average attendance"),
    ("NEED ATTENTION", f"{support_count:,}", "Based on demo thresholds"),
]
cols = st.columns(4)
for col, (label, value, note) in zip(cols, metrics):
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">{label}</div>'
            f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")
st.markdown('<div class="section-kicker">PERFORMANCE INTELLIGENCE</div>', unsafe_allow_html=True)
st.subheader("Understand the numbers")
left, right = st.columns(2, gap="large")

chart_bg = "#111d2d"
text_color = "#aab8ca"
grid_color = "#2a3b50"

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("**Subject performance**")
    st.caption("Average marks across the selected student group.")
    subject_means = filtered[SUBJECTS].mean().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor(chart_bg)
    ax.set_facecolor(chart_bg)
    bars = ax.barh(
        subject_means.index.str.title(),
        subject_means.values,
        color=["#5d91a8", "#6daeb3", "#76d6d0", "#8daeff", "#a7b9ff"],
        height=.56,
    )
    ax.set_xlim(0, 110)
    ax.set_xlabel("Average marks (%)", color=text_color, fontsize=9, labelpad=10)
    ax.tick_params(colors=text_color, labelsize=9, length=0)
    ax.xaxis.grid(True, color=grid_color, linewidth=.7, alpha=.7)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for bar, val in zip(bars, subject_means.values):
        ax.text(min(val + 1.5, 103), bar.get_y() + bar.get_height()/2, f"{val:.1f}%",
                va="center", color="#eaf0f8", fontsize=8)
    fig.tight_layout(pad=1.5)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("**Attendance & achievement**")
    st.caption("Each point represents one student. Dashed lines show demo thresholds.")
    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor(chart_bg)
    ax.set_facecolor(chart_bg)
    point_colors = filtered["support_needed"].map({True: "#f0a36b", False: "#76d6d0"})
    ax.scatter(
        filtered["attendance_pct"], filtered["average_score"],
        c=point_colors, s=68, alpha=.88, edgecolors="#0d1928", linewidths=.8,
    )
    ax.axvline(75, color="#8daeff", linestyle=(0, (4, 4)), linewidth=1, alpha=.8)
    ax.axhline(40, color="#f0a36b", linestyle=(0, (4, 4)), linewidth=1, alpha=.8)
    ax.set_xlabel("Attendance (%)", color=text_color, fontsize=9, labelpad=9)
    ax.set_ylabel("Average score (%)", color=text_color, fontsize=9, labelpad=9)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 105)
    ax.tick_params(colors=text_color, labelsize=8, length=0)
    ax.grid(True, color=grid_color, linewidth=.6, alpha=.6)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout(pad=1.5)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.markdown('<div class="section-kicker">STUDENT RECORDS</div>', unsafe_allow_html=True)
st.subheader("Students requiring attention")
support = filtered[filtered["support_needed"]].copy()
if support.empty:
    st.success("No students are flagged by the illustrative rule in this view.")
else:
    support["reason"] = support.apply(
        lambda row: ", ".join(
            reason for condition, reason in [
                (row["attendance_pct"] < 75, "Attendance below 75%"),
                (row["average_score"] < 40, "Average below 40%"),
            ] if condition
        ),
        axis=1,
    )
    st.dataframe(
        support[["student_id", "student_name", "class", "attendance_pct", "average_score", "reason"]]
        .sort_values(["average_score", "attendance_pct"]),
        use_container_width=True,
        hide_index=True,
    )

with st.expander("Explore all student records", expanded=True):
    display_columns = [
        "student_id", "student_name", "class", "attendance_pct",
        *SUBJECTS, "average_score", "support_needed",
    ]
    st.dataframe(
        filtered[display_columns].sort_values("average_score", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
    csv_bytes = filtered[display_columns].to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered report (CSV)",
        data=csv_bytes,
        file_name="student_performance_filtered.csv",
        mime="text/csv",
    )

st.divider()
st.markdown(
    '<div class="footnote">DEMO NOTICE · The included records are fictional. A student is flagged when '
    'attendance is below 75% OR average marks are below 40%. These illustrative thresholds are not an '
    'official academic assessment and should not be used for consequential decisions without review.</div>',
    unsafe_allow_html=True,
)
