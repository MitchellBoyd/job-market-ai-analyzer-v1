import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("AI Job Market Dashboard")

st.caption("Real-time insights into job demand, salaries, and trends")

st.set_page_config(page_title="AI Job Market Analyzer", layout="wide")

# Title
st.title("AI Job Market Analyzer 📊")
st.markdown("Analyze job demand, salary trends, and insights with interactive filters.")
st.caption("Interactive dashboard showing job demand, salary trends, and AI-generated insights.")

# Load data
df = pd.read_csv("cleaned_job_data.csv")

st.sidebar.header("Filters")

job_filter = st.sidebar.selectbox("Job Title", sorted(df["job_title"].unique()))
location_filter = st.sidebar.selectbox("Location", sorted(df["location"].unique()))
experience_filter = st.sidebar.selectbox("Experience Level", sorted(df["experience_level"].unique()))

filtered_df = df[
    (df["job_title"] == job_filter) &
    (df["location"] == location_filter) &
    (df["experience_level"] == experience_filter)
]
# --- KPIs ---
total_jobs = len(filtered_df)

if not filtered_df.empty:
    avg_salary = int(filtered_df["salary_midpoint"].mean())
else:
    avg_salary = 0

k1, k2 = st.columns(2)

with k1:
    st.metric("Total Jobs Found", total_jobs)

with k2:
    st.metric("Average Salary", f"${avg_salary:,}")
# Preview

st.subheader("Dataset Preview")
st.write(filtered_df.head())

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