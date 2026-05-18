# AI Job Market Analyzer

An interactive Streamlit dashboard for exploring job market data, salary trends, skills demand, hiring locations, and AI-generated insights.

---

## Features

- Filter jobs by title, location, experience level, and work type
- View key metrics including total jobs, average salary, median salary, and location count
- Analyze job demand trends over time
- Explore top job roles, in-demand skills, industries, and salary distribution
- Preview and download filtered job data
- View and download an AI-generated job market insights report

---

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly

---

## How to Run

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Run the dashboard:

```powershell
streamlit run app.py
```

3. Open the local app:

```text
http://localhost:8501
```

---

## Project Structure

```text
job-market-ai-analyzer/
├── app.py                 # Streamlit dashboard
├── cleaned_job_data.csv   # Cleaned job market dataset
├── ai_insights.txt        # AI-generated insights report
├── requirements.txt       # Python dependencies
└── README.md              # Project overview
```

---

## Example Insights

The dashboard and report highlight patterns such as:

- Top in-demand job roles
- Salary trends and distribution
- Skills most frequently requested by employers
- Industries and locations with strong hiring activity
- Recommendations based on job market patterns

---

## Project Purpose

This project analyzes job market data and presents the results in a clear interactive dashboard. It helps users explore hiring demand, salary patterns, skill requirements, and AI-generated market insights.

---

## Future Improvements

- Add PDF report export
- Add live job data scraping
- Add model-generated insights from selected dashboard filters
- Add authentication before deploying publicly

---

## Author

Mitchell Boyd
