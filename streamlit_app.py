"""
Interactive dashboard for exploring the Data & BI Analyst job market
in Poland, based on data scraped from NoFluffJobs.com.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Market Pulse", layout="wide")

df_jobs = pd.read_csv("data/processed/jobs_clean.csv")
df_skills = pd.read_csv("data/processed/skills_clean.csv")

st.title("Job Market Pulse")
st.write("Analyzing the Data & BI Analyst job market in Poland")

st.sidebar.header("Filters")

selected_cities = st.sidebar.multiselect(
    "City",
    options=sorted(df_jobs["location"].unique()),
    default=[],
)

remote_only = st.sidebar.checkbox("Remote only")

filtered_jobs = df_jobs.copy()

if selected_cities:
    filtered_jobs = filtered_jobs[filtered_jobs["location"].isin(selected_cities)]

if remote_only:
    filtered_jobs = filtered_jobs[filtered_jobs["is_remote"]]

median_salary = filtered_jobs["mid_salary"].median()
pct_remote = filtered_jobs["is_remote"].mean() * 100
# .index[0] gets the name of the most frequent skill, not the count.
# Not filtered by city/remote — reflects the overall dataset.
top_skill = df_skills["skills"].value_counts().index[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total postings", len(filtered_jobs))
col2.metric("Median salary", f"{median_salary:,.0f} PLN")
col3.metric("Remote offers", f"{pct_remote:.1f}%")
col4.metric("Top skill", top_skill)

st.subheader("Top 15 Most In-Demand Skills")

# Only include skills from offers matching the current filter, by
# restricting to skill rows whose link exists in filtered_jobs.
filtered_links = filtered_jobs["link"]
filtered_skills = df_skills[df_skills["link"].isin(filtered_links)]

top_skills_df = filtered_skills["skills"].value_counts().head(15).reset_index()
top_skills_df.columns = ["skill", "count"]

fig_skills = px.bar(
    top_skills_df,
    x="count",
    y="skill",
    orientation="h",
    color_discrete_sequence=["#0B7285"],
)
fig_skills.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_skills, use_container_width=True)