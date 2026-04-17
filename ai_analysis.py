import pandas as pd

df = pd.read_csv("final_job_data.csv")

summary = {
    "top_jobs": df["job_title"].value_counts().head(10).to_dict(),
    "top_locations": df["location"].value_counts().head(10).to_dict(),
    "salary_stats": df["salary_midpoint"].describe().to_dict()
}

print(summary)

from openai import OpenAI

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("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"))

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a data analyst."},
        {"role": "user", "content": f"Analyze this job market data and give key insights: {summary}"}
    ]
)

print(response.choices[0].message.content)

prompt = f"""
Analyze this job market dataset and provide a clear, structured report with:

1. Top Job Trends
- Most in-demand roles
- Key patterns in job demand

2. Salary Insights
- Average, median, and range
- What this tells us about the market

3. Location Insights
- Top hiring locations
- Remote vs city trends

4. Key Recommendations
- What skills or roles are most valuable
- What job seekers should focus on

Data:
{summary}
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a professional data analyst."},
        {"role": "user", "content": prompt}
    ]
)

ai_text = response.choices[0].message.content

print(ai_text)

with open("ai_insights.txt", "w", encoding="utf-8") as f:
    f.write(ai_text)

print("AI insights saved to file.")

with open("ai_insights.txt", "w", encoding="utf-8") as f:
    f.write("JOB MARKET AI REPORT\n")
    f.write("=" * 30 + "\n\n")
    f.write(ai_text)