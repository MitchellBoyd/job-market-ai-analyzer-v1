from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path("cleaned_job_data.csv")
INSIGHTS_PATH = Path("ai_insights.txt")
MAX_ROWS = 5000

REQUIRED_COLUMNS = {
    "post_date",
    "job_title",
    "location",
    "experience_level",
    "salary_midpoint",
    "skills_required",
    "industry",
    "work_type",
}


st.set_page_config(
    page_title="AI Job Market Dashboard",
    page_icon="bar_chart",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        st.error(f"Missing data file: {DATA_PATH}")
        st.stop()

    data = pd.read_csv(DATA_PATH, nrows=MAX_ROWS)
    data.columns = data.columns.str.strip()

    missing_columns = sorted(REQUIRED_COLUMNS - set(data.columns))
    if missing_columns:
        st.error("The dataset is missing required columns: " + ", ".join(missing_columns))
        st.stop()

    data["post_date"] = pd.to_datetime(data["post_date"], errors="coerce")
    data["salary_midpoint"] = pd.to_numeric(data["salary_midpoint"], errors="coerce")

    for column in ["job_title", "location", "experience_level", "industry", "work_type"]:
        data[column] = data[column].fillna("Unknown").astype(str).str.strip()

    return data


def title_case(value: str) -> str:
    if not value or value == "Unknown":
        return value
    return value.title()


def filter_options(data: pd.DataFrame, column: str) -> list[str]:
    values = sorted(data[column].dropna().unique())
    return ["All"] + values


def apply_filter(data: pd.DataFrame, column: str, selected_value: str) -> pd.DataFrame:
    if selected_value == "All":
        return data
    return data[data[column] == selected_value]


def salary_metric(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"${int(value):,}"


df = load_data()

st.title("AI Job Market Analyzer")
st.caption("Interactive dashboard for job demand, salary trends, skills, and generated market insights.")

st.sidebar.header("Filters")

job_filter = st.sidebar.selectbox(
    "Job Title",
    filter_options(df, "job_title"),
    format_func=title_case,
)
location_filter = st.sidebar.selectbox("Location", filter_options(df, "location"))
experience_filter = st.sidebar.selectbox(
    "Experience Level",
    filter_options(df, "experience_level"),
)
work_type_filter = st.sidebar.selectbox("Work Type", filter_options(df, "work_type"))

filtered_df = df.copy()
filtered_df = apply_filter(filtered_df, "job_title", job_filter)
filtered_df = apply_filter(filtered_df, "location", location_filter)
filtered_df = apply_filter(filtered_df, "experience_level", experience_filter)
filtered_df = apply_filter(filtered_df, "work_type", work_type_filter)

st.subheader("Overview")

total_jobs = len(filtered_df)
avg_salary = filtered_df["salary_midpoint"].mean()
median_salary = filtered_df["salary_midpoint"].median()
total_locations = filtered_df["location"].nunique()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Jobs", f"{total_jobs:,}")
k2.metric("Average Salary", salary_metric(avg_salary))
k3.metric("Median Salary", salary_metric(median_salary))
k4.metric("Locations", f"{total_locations:,}")

if filtered_df.empty:
    st.warning("No jobs match the selected filters. Try selecting 'All' for one or more filters.")
    st.stop()

st.divider()

st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(100), use_container_width=True, hide_index=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_jobs.csv",
    mime="text/csv",
)

st.divider()

st.subheader("Job Demand Trends")

trend_df = df.copy()
if job_filter != "All":
    trend_df = trend_df[trend_df["job_title"] == job_filter]

trend_df = trend_df.dropna(subset=["post_date"])
trend_df["month"] = trend_df["post_date"].dt.to_period("M").dt.to_timestamp()
trend_data = trend_df.groupby("month").size().reset_index(name="job_count")

if trend_data.empty:
    st.info("There is no valid posting-date data for the current job title selection.")
else:
    fig = px.line(
        trend_data,
        x="month",
        y="job_count",
        markers=True,
        title="Job Demand Over Time",
        labels={"month": "Month", "job_count": "Job Listings"},
    )
    fig.update_layout(template="plotly_white", height=450)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Top Job Roles")
    job_counts = df["job_title"].value_counts().head(10).sort_values()
    fig = px.bar(
        job_counts,
        orientation="h",
        title="Top Roles by Listing Count",
        labels={"value": "Number of Listings", "index": "Job Title"},
    )
    fig.update_layout(template="plotly_white", height=450, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Salary Distribution")
    salary_data = filtered_df.dropna(subset=["salary_midpoint"])
    if salary_data.empty:
        st.info("No salary data is available for the selected filters.")
    else:
        fig = px.box(
            salary_data,
            y="salary_midpoint",
            points="outliers",
            title="Selected Jobs",
            labels={"salary_midpoint": "Salary"},
        )
        fig.update_layout(template="plotly_white", height=450)
        st.plotly_chart(fig, use_container_width=True)

st.divider()

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Top Skills")
    skills_series = (
        filtered_df["skills_required"]
        .dropna()
        .astype(str)
        .str.split("|")
        .explode()
        .str.strip()
    )
    top_skills = skills_series[skills_series != ""].value_counts().head(10).sort_values()

    if top_skills.empty:
        st.info("No skills data is available for the selected filters.")
    else:
        fig = px.bar(
            top_skills,
            orientation="h",
            title="Most In-Demand Skills",
            labels={"value": "Mentions", "index": "Skill"},
        )
        fig.update_layout(template="plotly_white", height=450, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("Top Industries")
    industry_counts = filtered_df["industry"].value_counts().head(10).sort_values()
    fig = px.bar(
        industry_counts,
        orientation="h",
        title="Industries Hiring for Selected Jobs",
        labels={"value": "Listings", "index": "Industry"},
    )
    fig.update_layout(template="plotly_white", height=450, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("AI Insights")

if INSIGHTS_PATH.exists():
    insights = INSIGHTS_PATH.read_text(encoding="utf-8")
    st.markdown(insights)
    st.download_button(
        label="Download AI Report",
        data=insights,
        file_name="job_market_report.txt",
        mime="text/plain",
    )
else:
    st.info(f"Add {INSIGHTS_PATH} to show the generated report.")
