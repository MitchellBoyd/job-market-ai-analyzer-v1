import pandas as pd

df = pd.read_csv("job_postings.csv")

print(df.head())
print(df.columns)
print(df.shape)
print(df.isnull().sum())
print(df.dtypes)

df = df.drop(columns=["job_id"])
df["post_date"] = pd.to_datetime(df["post_date"])

print(df.dtypes)
print(df.duplicated().sum())

df["job_title"] = df["job_title"].str.lower()
df["job_title"] = df["job_title"].str.strip()

print(df["job_title"].head())
print(df[["salary_min", "salary_max", "salary_midpoint"]].head())

df["salary"] = df["salary_midpoint"]
df = df.drop(columns=["salary_min", "salary_max"])

print(df[["salary"]].head())
print(df["salary"].describe())

df["skills_required"] = df["skills_required"].str.lower().str.strip()

print(df["job_title"].value_counts().head())
print(df["location"].value_counts().head())
print(df["experience_level"].value_counts())

df.to_csv("cleaned_job_data.csv", index=False)

job_counts = df["job_title"].value_counts().head(10)
print(job_counts)

import matplotlib.pyplot as plt

plt.figure(figsize=(12,7))

job_counts = df["job_title"].value_counts().head(10).sort_values()

job_counts.plot(kind="barh")

plt.title("Top 10 Most In-Demand Job Roles", fontsize=16)
plt.xlabel("Number of Jobs")
plt.ylabel("Job Title")

for i, v in enumerate(job_counts):
    plt.text(v - 20000, i, f"{int(v):,}", va='center', color='white')

plt.tight_layout()
plt.show()

plt.figure(figsize=(12,7))

top_jobs_salary = df.groupby("job_title")["salary_midpoint"].mean().sort_values().tail(10)

top_jobs_salary.plot(kind="barh")

plt.title("Top 10 Highest Paying Jobs", fontsize=16)
plt.xlabel("Average Salary")
plt.ylabel("Job Title")

for i, v in enumerate(top_jobs_salary):
    plt.text(v - 20000, i, f"{int(v):,}", va='center', color='white')

plt.tight_layout()
plt.show()

print("Top job roles show strong demand for analytical and technical positions.")

print(df["salary_midpoint"].describe())

print("High salary variation shows a wide range of experience levels and job seniority.")

avg_salary_by_job = df.groupby("job_title")["salary_midpoint"].mean().sort_values(ascending=False)

print(avg_salary_by_job.head(10))

top_jobs_salary = avg_salary_by_job.head(10).sort_values()

plt.figure(figsize=(12,7))

top_locations = df.groupby("location")["salary_midpoint"].mean().sort_values().tail(10)

top_locations.plot(kind="barh")

plt.title("Top Paying Locations", fontsize=16)
plt.xlabel("Average Salary")
plt.ylabel("Location")

for i, v in enumerate(top_locations):
    plt.text(v - 20000, i, f"{int(v):,}", va='center', color='white')

plt.tight_layout()
plt.show()

print("Some job roles clearly offer higher salaries, especially in technical and specialized fields.")

location_salary = df.groupby("location")["salary_midpoint"].mean().sort_values(ascending=False)

print(location_salary.head(10))

top_locations = location_salary.head(10)

plt.figure(figsize=(8,5))

work_type_salary = df.groupby("work_type")["salary_midpoint"].mean()

work_type_salary.plot(kind="bar")

plt.title("Average Salary by Work Type", fontsize=14)
plt.xlabel("Work Type")
plt.ylabel("Average Salary")

for i, v in enumerate(work_type_salary):
    plt.text(v - 20000, i, f"{int(v):,}", va='center', color='white')

plt.tight_layout()
plt.show()

print("Work type impacts salary, with remote and hybrid roles often competing with major city salaries.")

df.to_csv("final_job_data.csv", index=False)

print("Final cleaned dataset saved successfully.")

print("Data analysis complete. Dataset ready for AI processing.")