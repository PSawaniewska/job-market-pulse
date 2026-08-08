"""
Loads cleaned job data from CSV into a SQLite database for SQL analysis.
"""

import pandas as pd
import sqlite3

df_jobs = pd.read_csv("../data/processed/jobs_clean.csv")
df_skills = pd.read_csv("../data/processed/skills_clean.csv")

# jobs.db is created here if it doesn't exist yet — no separate setup needed.
connection = sqlite3.connect("jobs.db")

# if_exists="replace" rebuilds both tables from scratch on every run,
# so re-running this script always reflects the latest cleaned data.
df_jobs.to_sql("jobs", connection, if_exists="replace", index=False)
df_skills.to_sql("skills", connection, if_exists="replace", index=False)

print("Database created successfully.")
connection.close()