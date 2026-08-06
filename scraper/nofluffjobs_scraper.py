"""
Scraper for NoFluffJobs.com job listings.
Fetches search results for several related job titles and extracts key fields:
title, company, salary, location, and required skills.
"""

import json
import time

import requests
from bs4 import BeautifulSoup


def scrape_page(search_term, page_number):
    """Fetch one results page for a given search term and return a list of job dicts."""
    encoded_term = search_term.replace(" ", "%20")
    url = f"https://nofluffjobs.com/pl/?criteria=jobPosition%3D%27{encoded_term}%27&page={page_number}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("a", class_="posting-list-item")

    page_jobs = []
    for card in job_cards:
        title = card.find("h3")
        company = card.find("h4", class_="company-name")
        location = card.find("nfj-posting-item-city")
        tags = card.find_all("span", class_="posting-tag")

        job = {
            "title": title.text.strip(),
            "company": company.text.strip(),
            "location": location.text.strip(),
            "salary": tags[0].text.strip() if tags else None,
            "skills": [tag.text.strip() for tag in tags[1:]] if tags else [],
            "link": card["href"],
        }
        page_jobs.append(job)

    return page_jobs


# Fake a real browser's User-Agent — the site returns 403 without one.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Related job titles — broadens coverage beyond the site's per-search
# pagination cap (~90-100 results), while staying on-topic for the
# Data Analyst job market.
search_terms = ["data analyst", "junior data analyst", "business analyst", "bi analyst"]

max_pages = 30  # safety limit per search term
all_jobs = []
seen_links = set()

for search_term in search_terms:
    print(f"--- Searching: {search_term} ---")
    page_num = 1

    while page_num <= max_pages:
        print(f"Scraping page {page_num}...")
        page_jobs = scrape_page(search_term, page_num)

        new_jobs = [job for job in page_jobs if job["link"] not in seen_links]

        if not new_jobs:
            print("No new jobs found — stopping this search term.")
            break

        for job in new_jobs:
            all_jobs.append(job)
            seen_links.add(job["link"])

        page_num += 1
        time.sleep(1.5)  # be polite to the server — don't hammer it with requests :)

print("Total unique jobs collected:", len(all_jobs))

# Save the raw scraped data to disk, so later steps (cleaning, analysis)
# don't need to re-scrape the site every time.
with open("../data/raw/jobs_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=2)

print("Saved", len(all_jobs), "jobs to data/raw/jobs_raw.json")