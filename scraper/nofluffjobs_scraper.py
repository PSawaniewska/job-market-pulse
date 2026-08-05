"""
Scraper for NoFluffJobs.com job listings.
Fetches search results for a given job title and extracts key fields:
title, company, salary, location, and required skills.
"""

import requests
from bs4 import BeautifulSoup


def scrape_page(page_number):
    """Fetch one results page and return a list of job dicts."""
    url = f"https://nofluffjobs.com/pl/?criteria=jobPosition%3D%27data%20analyst%27&page={page_number}"

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

all_jobs = []
for page_num in range(1, 4):
    print(f"Scraping page {page_num}...")
    all_jobs.extend(scrape_page(page_num))

print("Total jobs collected:", len(all_jobs))

# Deduplicate by link — a dict automatically keeps only one entry per key,
# so storing jobs keyed by their unique link removes duplicates in one step.
unique_jobs = {job["link"]: job for job in all_jobs}.values()
unique_jobs = list(unique_jobs)

print("Total scraped (with duplicates):", len(all_jobs))
print("Unique jobs:", len(unique_jobs))

