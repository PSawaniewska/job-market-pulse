"""
Cleans raw scraped job data and prepares it for analysis.
"""

import pandas as pd

df = pd.read_json("../data/raw/jobs_raw.json")

# --- Initial exploration ---
print(df.head())
print(df.info())

print("--- Salary samples ---")
print(df["salary"].head(10).tolist())

print("--- Location samples ---")
print(df["location"].head(10).tolist())

print("--- Skills type check ---")
print(df["skills"][0])
print(type(df["skills"][0]))


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

print(df.info())

df["mid_salary"] = (df["salary_min"] + df["salary_max"]) /2
print(df.info())

# Note: offers with only a single flat salary (no max) will have mid_salary
# as NaN too, rather than falling back to salary_min — treating them as
# missing data is more honest than assuming min == typical salary.
# This affects only ~1% of offers, so the impact on overall analysis is minimal.

# --- Location cleaning ---
# (kolejny etap)


# --- Skills processing ---
# (explode na liście skills)