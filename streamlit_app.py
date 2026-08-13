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

# --- Sidebar filters ---

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

# Skills rows matching the currently filtered offers, via shared link.
filtered_links = filtered_jobs["link"]
filtered_skills = df_skills[df_skills["link"].isin(filtered_links)]

# --- Top metrics ---

median_salary = filtered_jobs["mid_salary"].median()
pct_remote = filtered_jobs["is_remote"].mean() * 100
pct_english = filtered_jobs["has_english"].mean() * 100
# .index[0] gets the name of the most frequent skill, not the count.
top_skill = filtered_skills["skills"].value_counts().index[0] if len(filtered_skills) else "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total postings", len(filtered_jobs))
col2.metric("Median salary", f"{median_salary:,.0f} PLN" if pd.notna(median_salary) else "N/A")
col3.metric("Remote offers", f"{pct_remote:.1f}%")
col4.metric("Top skill", top_skill)

# --- Top skills ---

st.subheader("Top 15 Most In-Demand Skills")

top_skills_df = filtered_skills["skills"].value_counts().head(15).reset_index()
top_skills_df.columns = ["skill", "count"]

fig_skills = px.bar(
    top_skills_df, x="count", y="skill", orientation="h",
    color_discrete_sequence=["#0B7285"],
)
fig_skills.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Number of postings", yaxis_title="")
st.plotly_chart(fig_skills, use_container_width=True)

# --- Salary distribution ---

st.subheader("Salary Distribution")

salary_data = filtered_jobs.dropna(subset=["mid_salary"])

if len(salary_data) > 0:
    fig_salary = px.histogram(
        salary_data, x="mid_salary", nbins=20,
        color_discrete_sequence=["#0B7285"],
    )
    fig_salary.add_vline(
        x=median_salary, line_dash="dash", line_color="#D9480F",
        annotation_text=f"Median: {median_salary:,.0f} PLN",
    )
    fig_salary.update_layout(xaxis_title="Monthly salary (PLN, gross)", yaxis_title="Number of postings")
    st.plotly_chart(fig_salary, use_container_width=True)
else:
    st.write("No salary data available for the current filter selection.")

# --- Seniority distribution ---

st.subheader("Seniority Distribution Across Postings")


def get_experience_level(title):
    if "Junior" in title:
        return "Junior"
    elif "Senior" in title:
        return "Senior"
    elif "Mid" in title:
        return "Mid"
    else:
        return "Not specified"


filtered_jobs = filtered_jobs.copy()
filtered_jobs["experience_level"] = filtered_jobs["title"].apply(get_experience_level)
level_counts = filtered_jobs["experience_level"].value_counts().reset_index()
level_counts.columns = ["level", "count"]

fig_seniority = px.pie(
    level_counts, names="level", values="count",
    color_discrete_sequence=px.colors.sequential.Teal,
)
st.plotly_chart(fig_seniority, use_container_width=True)
st.caption(
    "Most postings don't specify a seniority level in the title, "
    "so this breakdown should be read as directional, not exact."
)

# --- English / remote share ---

st.subheader("Share of Postings Requiring English / Offering Remote Work")

summary_df = pd.DataFrame({
    "category": ["Requires English", "Remote work"],
    "percentage": [pct_english, pct_remote],
})

fig_summary = px.bar(
    summary_df, x="percentage", y="category", orientation="h",
    color_discrete_sequence=["#0B7285"],
)
fig_summary.update_layout(xaxis_title="Percentage of postings", yaxis_title="", xaxis_range=[0, 100])
st.plotly_chart(fig_summary, use_container_width=True)

# --- Top cities ---

st.subheader("Top Cities for On-Site Postings")
st.caption(
    "Postings listed at multiple cities are counted only under their "
    "primary location, which may understate totals for some cities."
)

on_site_jobs = filtered_jobs[filtered_jobs["location"] != "Zdalnie"]
top_cities_df = on_site_jobs["location"].value_counts().head(10).reset_index()
top_cities_df.columns = ["city", "count"]

fig_cities = px.bar(
    top_cities_df, x="count", y="city", orientation="h",
    color_discrete_sequence=["#0B7285"],
)
fig_cities.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Number of postings", yaxis_title="")
st.plotly_chart(fig_cities, use_container_width=True)

# --- Top companies ---

st.subheader("Top Companies Posting These Roles")
st.caption("Several top posters are recruitment agencies hiring for multiple clients, not single in-house teams.")

top_companies_df = filtered_jobs["company"].value_counts().head(10).reset_index()
top_companies_df.columns = ["company", "count"]

fig_companies = px.bar(
    top_companies_df, x="count", y="company", orientation="h",
    color_discrete_sequence=["#0B7285"],
)
fig_companies.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Number of postings", yaxis_title="")
st.plotly_chart(fig_companies, use_container_width=True)

# --- Skill popularity vs salary ---

st.subheader("Skill Popularity vs. Average Salary")

skill_salary = filtered_skills[filtered_skills["mid_salary"].notna()]
skill_salary = skill_salary.groupby("skills")["mid_salary"].agg(["mean", "count"]).reset_index()
skill_salary = skill_salary[skill_salary["count"] >= 5]

if len(skill_salary) > 0:
    fig_bubble = px.scatter(
        skill_salary, x="count", y="mean", size="count", text="skills",
        color_discrete_sequence=["#0B7285"], size_max=60,
    )
    fig_bubble.update_traces(textposition="top center")
    fig_bubble.update_layout(
        xaxis_title="Number of postings (popularity)",
        yaxis_title="Average salary (PLN, gross)",
    )
    st.plotly_chart(fig_bubble, use_container_width=True)
    st.caption("Only skills appearing in at least 5 postings (within the current filter) are shown, for reliability.")
else:
    st.write("Not enough data for this chart with the current filter selection.")

# --- Footer ---

st.divider()
st.caption(
    "Data scraped from [NoFluffJobs.com](https://nofluffjobs.com) in "
    "compliance with robots.txt, for educational/portfolio purposes only. "
    "See the [project repository](https://github.com/PSawaniewska/job-market-pulse) "
    "for source code, methodology, and data limitations."
)