"""
Scraper for NoFluffJobs.com job listings.
Fetches search results for a given job title and extracts key fields:
title, company, salary, location, and required skills.
"""

import requests
from bs4 import BeautifulSoup

url = "https://nofluffjobs.com/pl/?criteria=jobPosition%3D%27data%20analyst%27"

# Fake a real browser's User-Agent — the site returns 403 without one.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(url, headers=headers)

# Quick sanity check before parsing — confirms we got a real page,
# not an empty response or an error page disguised as a 200.
print("Status code:", response.status_code)
print("Response length:", len(response.text))

# "html.parser" is Python's built-in parser — no extra installation needed.
soup = BeautifulSoup(response.text, "html.parser")

# Each job card is an <a> tag with class "posting-list-item"
# (confirmed by inspecting the page in DevTools).
job_cards = soup.find_all("a", class_="posting-list-item")

print("Number of job cards found:", len(job_cards))

# Work with just the first card for now, to verify our selectors
# are correct before looping over all of them.
first_card = job_cards[0]

title = first_card.find("h3")
company = first_card.find("h4", class_="company-name")

print("Title:", title.text.strip())
print("Company:", company.text.strip())

