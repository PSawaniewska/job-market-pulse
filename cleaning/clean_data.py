"""
Cleans raw scraped job data and prepares it for analysis.
"""

import pandas as pd
from utils import check_english

df = pd.read_json("../data/raw/jobs_raw.json")

# Search results included offers unrelated to data/analyst roles
# (e.g. "Project Manager", "Java Developer"), likely matched by the site's
# search on description content rather than exact job title. Keep only
# offers whose title actually relates to analysis/analytics work.
df = df[df["title"].str.contains("Analyst|Analityk|Analytics|Analiz", case=False, na=False)]

# Business Analyst roles were excluded after reviewing the skill data —
# they require a distinctly different skill set (UML/BPMN, process
# modeling) from Data/BI Analyst roles, which this project focuses on.
# Hybrid titles explicitly mentioning "Data" (e.g. "Data Business Analyst")
# were kept, as they're closer to the project's actual scope.
# See NOTES.md for the full comparison of exclusion approaches considered.
business_analyst_pattern = "Business.{0,3}Analyst|Business.{0,3}System.{0,3}Analyst|System.{0,3}Business.{0,3}Analyst"
is_pure_business_analyst = df["title"].str.contains(business_analyst_pattern, case=False, na=False, regex=True)
has_data_in_title = df["title"].str.contains("Data", case=False, na=False)
df = df[~(is_pure_business_analyst & ~has_data_in_title)]

# --- Initial exploration ---
print(df.head())
print(df.info())


# --- Salary cleaning ---

# Replace the non-breaking space (\xa0) with nothing — it's invisible
# but breaks any attempt to convert these strings to numbers.
df["salary"] = df["salary"].str.replace("\xa0", "", regex=False)

# Offers without disclosed salary show "Sprawdź wynagrodzenie" instead of
# numbers — treat it as a proper missing value, not text to parse.
df["salary"] = df["salary"].replace("Sprawdź wynagrodzenie", pd.NA)

# Split salary into min/max, then strip "PLN" and whitespace from both parts.
df[["salary_min", "salary_max"]] = df["salary"].str.split("  – ", expand=True)

# Remove "PLN" and whitespace from both columns — even salary_min can contain
# "PLN" when an offer shows a single flat amount instead of a min-max range
# (the split then has nothing to split on, so everything lands in salary_min).
df["salary_max"] = df["salary_max"].str.replace("PLN", "", regex=False)
df["salary_min"] = df["salary_min"].str.replace("PLN", "", regex=False)
df["salary_max"] = df["salary_max"].str.strip()
df["salary_min"] = df["salary_min"].str.strip()

# Convert both columns from text to actual numbers, so we can calculate
# averages, medians etc. later.
df["salary_min"] = pd.to_numeric(df["salary_min"])
df["salary_max"] = pd.to_numeric(df["salary_max"])

# Note: offers with only a single flat salary (no max) would have mid_salary
# as NaN too, rather than falling back to salary_min — treating them as
# missing data would be more honest than assuming min == typical salary.
# In this dataset, no offers currently have this issue.
df["mid_salary"] = (df["salary_min"] + df["salary_max"]) / 2

print(df.info())


# --- Location cleaning ---

# Remove the non-breaking space character (\xa0), same issue as in salary.
df["location"] = df["location"].str.replace("\xa0", "", regex=False)

# Some offers list a main location followed by "+N" (extra locations,
# e.g. "Warszawa +2" or "Zdalnie +1"). For our analysis, only the first/main
# location matters, so we keep everything before the "+" and drop the rest.
df["location"] = df["location"].str.split("+").str[0]

# Remove leftover whitespace from splitting.
df["location"] = df["location"].str.strip()

# Standardize city name variants found via .value_counts() during exploration
# (e.g. "Cracow"/"Kraków", "Warsaw"/"Warszawa").
df["location"] = df["location"].replace({
    "Cracow": "Kraków",
    "Warsaw": "Warszawa",
    "Gdansk": "Gdańsk",
})

# Remove offers from abroad — we're only analyzing the job market in Poland.
foreign_locations = ["International", "Budapest  , HU", "Singapur  , SG", "Tirana  , AL"]
df = df[~df["location"].isin(foreign_locations)]

# Add is_remote column to differentiate remote offers from the stationary ones.
df["is_remote"] = df["location"] == "Zdalnie"


# --- Language requirement flag ---

df["has_english"] = df["skills"].apply(check_english)

# --- Skills processing ---

# Explode into a separate DataFrame — one row per (offer, skill) pair,
# used only for skill-frequency analysis, not for salary/location stats,
# where one row must still equal one offer. .copy() avoids ambiguity about
# whether this is a view into df or an independent DataFrame.
df_skills = df.explode("skills").copy()

# Merge known duplicate tags: same skill, different capitalization or
# singular/plural form. Other minor variants (e.g. spelling, language)
# are left as-is — see NOTES.md.
df_skills["skills"] = df_skills["skills"].replace({
    "Business analysis": "Business Analysis",
    "REST APIs": "REST API",
})

# "Business Analyst" (4 remaining occurrences) and "Business Analysis"
# (30 occurrences) are excluded — these are job-role/category tags,
# not skills, and their continued presence even after title-level
# filtering confirms some hybrid "Data Business Analyst" offers still
# carry them. "Data" is too broad to be meaningful, and
# "angielski"/"polski" are language requirements, not skills.
non_skill_tags = ["Business Analyst", "Business Analysis", "Data", "angielski", "polski"]
df_skills = df_skills[~df_skills["skills"].isin(non_skill_tags)]


# --- Final cleanup and export ---

# Drop the raw salary string — salary_min/salary_max/mid_salary replace it.
df = df.drop(columns=["salary"])

# Two separate files: jobs_clean.csv keeps one row per offer (for salary/
# location stats), skills_clean.csv is exploded (for skill-frequency analysis).
df.to_csv("../data/processed/jobs_clean.csv", index=False)
df_skills.to_csv("../data/processed/skills_clean.csv", index=False)

print("Saved", len(df), "cleaned job offers to jobs_clean.csv")
print("Saved", len(df_skills), "exploded skill rows to skills_clean.csv")