import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Job Market Dashboard",
    page_icon="📊",
    layout="wide"
)

st.set_page_config(page_title="AI Job Market Analyzer", layout="wide")

# Title
st.title("AI Job Market Analyzer 📊")
st.markdown(
    "<p style='font-size:18px; color:#6c757d;'>Interactive dashboard showing job demand, salary trends, and AI generated insights.</p>",
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# Load data
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_job_data.csv", nrows=5000)

df = load_data()

st.sidebar.markdown("# 🎛 Filters")
st.sidebar.markdown("---")

job_filter = st.sidebar.selectbox("Job Title", sorted(df["job_title"].unique()))
location_filter = st.sidebar.selectbox("Location", sorted(df["location"].unique()))
experience_filter = st.sidebar.selectbox("Experience Level", sorted(df["experience_level"].unique()))

filtered_df = df[
    (df["job_title"] == job_filter) &
    (df["location"] == location_filter) &
    (df["experience_level"] == experience_filter)
]
# --- KPIs ---
# --- OVERVIEW SECTION ---
with st.container():

    st.markdown("## 📊 Overview")

    total_jobs = len(filtered_df)

    if not filtered_df.empty:
        avg_salary = int(filtered_df["salary_midpoint"].mean())
        median_salary = int(filtered_df["salary_midpoint"].median())
    else:
        avg_salary = 0
        median_salary = 0

    k1, k2, k3 = st.columns([1,1,1])

    with k1:
        st.metric("Total Jobs", total_jobs)

    with k2:
        st.metric("Average Salary", f"${avg_salary:,}")

    with k3:
        st.metric("Median Salary", f"${median_salary:,}")

st.markdown("---")

# Preview
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(), use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_jobs.csv",
    mime="text/csv"
)

st.markdown(
    "<p style='font-size:16px; color:gray;'>Trend based on selected job title across all locations and experience levels</p>",
    unsafe_allow_html=True
)

st.markdown("## 📈 Job Demand Trends")

# Use broader data for trends
trend_df = df[df["job_title"] == job_filter]

trend_data = (
    trend_df.groupby(["year", "month"])
    .size()
    .reset_index(name="job_count")
)

trend_data["date"] = pd.to_datetime(
    trend_data["year"].astype(str) + "-" + trend_data["month"].astype(str)
)

trend_data = trend_data.sort_values("date")

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(
    trend_data["date"],
    trend_data["job_count"],
    marker="o"
)

ax.set_title("Job Demand Over Time", fontsize=14, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Job Listings")

ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

st.divider()

# Charts + salary
col1, col2 = st.columns([2, 1])

# --- LEFT: JOB ROLES ---
with col1:
    st.subheader("Top Job Roles")

    job_counts = df["job_title"].value_counts().head(10)

    fig, ax = plt.subplots()
    job_counts.sort_values().plot(kind="barh", ax=ax)

    ax.set_title("Top Job Roles")
    ax.set_xlabel("Number of Job Listings")
    ax.set_ylabel("Job Title")

    st.pyplot(fig)

# --- RIGHT: SALARY ---
with col2:
    st.markdown("### 💰 Salary Stats")

    if not filtered_df.empty:
        avg_salary = int(filtered_df["salary_midpoint"].mean())
        median_salary = int(filtered_df["salary_midpoint"].median())
    else:
        avg_salary = 0
        median_salary = 0

    st.metric("Average Salary", f"${avg_salary:,}")
    st.metric("Median Salary", f"${median_salary:,}")
    st.markdown("<br><br>", unsafe_allow_html=True)

# --- SKILLS ANALYSIS ---

st.markdown("## 🛠 Top Skills Analysis")

skills_series = (
    filtered_df["skills_required"]
    .dropna()
    .str.split("|")
    .explode()
)

top_skills = skills_series.value_counts().head(10)

fig, ax = plt.subplots(figsize=(10,5))

top_skills.sort_values().plot(
    kind="barh",
    ax=ax
)

ax.set_title("Most In Demand Skills")
ax.set_xlabel("Number of Mentions")
ax.set_ylabel("Skill")

st.pyplot(fig)

# --- AI INSIGHTS ---
st.divider()
st.subheader("AI Insights")

with open("ai_insights.txt", "r", encoding="utf-8") as f:
    insights = f.read()

st.markdown(insights)
st.download_button(
    label="Download AI Report",
    data=insights,
    file_name="job_market_report.txt",
    mime="text/plain"
)