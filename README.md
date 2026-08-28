# Job Market Pulse

A web scraper and interactive dashboard analyzing the Data & BI Analyst
job market in Poland - skill demand, salary ranges, remote work trends,
and more.

🔗 **[View the live dashboard](https://job-market-pulse-ty85taeuteztmhmxzo5xyq.streamlit.app/)**

## Key Findings

- **SQL is non-negotiable.** It appears in nearly half of all postings
  (50 of 114) - by far the most requested skill, regardless of role
  specialization.
- **Visualization skills pay more than raw SQL.** Postings requiring
  Tableau, Data Visualization, or Dashboarding average 25,000-27,000
  PLN, compared to 22,449 PLN for SQL - suggesting the ability to
  present data is valued above the ability to query it.
- **Remote work is common, English is not.** 37.7% of postings offer
  remote work, but only 9.6% explicitly require English - though the
  real share is likely higher (see Limitations).
- **Krakow and Warszawa dominate.** Together they account for over
  half of all on-site postings; other cities trail far behind.
- **Seniority is rarely stated.** 82.5% of postings don't mention a
  seniority level in the title at all, and zero mention "Junior" -
  worth noting for anyone job-hunting at entry level.

## Tech Stack

- **Scraping:** Python, requests, BeautifulSoup
- **Data processing:** Pandas
- **Database & analysis:** SQLite, SQL (via jupysql in Jupyter)
- **Visualization:** Matplotlib, Seaborn (static analysis), Plotly (interactive dashboard)
- **Dashboard:** Streamlit, deployed on Streamlit Community Cloud

## Project Structure

```
job-market-pulse/
├── scraper/
│   └── nofluffjobs_scraper.py    # collects raw job postings
├── cleaning/
│   ├── clean_data.py             # cleans and filters raw data
│   └── utils.py                  # shared helper functions (tested)
├── database/
│   └── load_data.py              # loads cleaned data into SQLite
├── notebooks/
│   ├── 01_sql_analysis.ipynb     # SQL queries answering key questions
│   └── 02_visualizations.ipynb   # charts and business insights
├── tests/
│   └── test_utils.py             # unit tests for helper functions
├── data/
│   ├── raw/                      # scraped, unprocessed data
│   └── processed/                # cleaned CSVs
├── streamlit_app.py              # interactive dashboard
├── requirements.txt
└── NOTES.md                      # development notes and data-quality decisionsotes and data-quality decisions
```

## How to Run

1. Clone the repository:
   ```
   git clone https://github.com/PSawaniewska/job-market-pulse.git
   cd job-market-pulse
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the scraper (optional - raw data is already included):
   ```
   python scraper/nofluffjobs_scraper.py
   ```

4. Clean the data:
   ```
   python cleaning/clean_data.py
   ```

5. Load data into SQLite:
   ```
   python database/load_data.py
   ```

6. Launch the dashboard:
   ```
   streamlit run streamlit_app.py
   ```
7. Run the tests (optional):
   ```
   pytest
   ```

## Methodology

The project targets Data and BI Analyst roles specifically. Since a
single search term on the site returns at most ~90-100 results, data
was collected across several related search terms (e.g. "data analyst",
"junior data analyst", "bi analyst") and deduplicated by job URL,
yielding 348 unique postings.

During cleaning, offers unrelated to analytical work (e.g. "Project
Manager", "Java Developer") were filtered out by title, reducing the
dataset to 312 postings. Business Analyst postings were then excluded
after reviewing the skills breakdown - they require a distinctly
different skill set (UML, BPMN, process modeling) that would have
distorted a skills analysis meant to reflect Data/BI Analyst work. This
final step brought the dataset to 114 postings, prioritizing thematic
consistency over volume.

This is a learning/portfolio project based on a self-collected, limited
dataset - findings illustrate methodology, not a definitive market
survey.

## Data Source & Ethics

Data was scraped from [NoFluffJobs.com](https://nofluffjobs.com) in
compliance with the site's robots.txt - only the publicly accessible
search results listing was accessed, not the disallowed /posting/ or
/api/ paths. The scraper includes delays between requests to avoid
overloading the server. All data is used strictly for
educational/portfolio purposes, not for commercial use or
redistribution. Extracted fields (title, company, salary range, skill
tags, location) are factual data points, not a reproduction of original
listing content, which remains the property of NoFluffJobs and the
posting employers.

## Limitations

- **Scope limited by robots.txt:** only search results listings were
  accessible, not full job descriptions. This is the root cause of
  several limitations below.
- **English requirement likely understated:** only counted when
  explicitly tagged as a skill; the true share is probably higher, since
  many postings likely mention it only in the full description.
- **Multi-location postings undercounted by city:** postings available
  in multiple cities are recorded only under their primary listed city,
  which may understate totals for some cities.
- **Seniority data is sparse:** only 16 of 114 postings (14%) mention a
  seniority level in the title at all, and none mention "Junior" -
  treat any seniority-based comparison as directional, not exact.
- **Top companies list mixes agencies and direct employers:** several
  frequent posters are recruitment agencies or software houses hiring
  for clients, not single companies building large in-house teams.
- **Minor skill-tag variants left unmerged:** small spelling or language
  duplicates (e.g. "Data modeling"/"Data modelling") were left as-is, as
  their impact on the overall skill ranking is minimal.

Full development notes, including all decisions and numbers behind
these limitations, are in [NOTES.md](NOTES.md).

## Screenshots

<img width="1919" height="859" alt="Zrzut ekranu 2026-08-13 221554" src="https://github.com/user-attachments/assets/ade0eeb7-59c9-416c-a643-c9a8af7a1256" />
<img width="1919" height="861" alt="Zrzut ekranu 2026-08-13 221738" src="https://github.com/user-attachments/assets/2e55f4bb-509c-4718-9c37-a9a63dcd8771" />

## About

Built by Paulina Sawaniewska as part of a career transition into data
analytics. Connect on
[LinkedIn](https://www.linkedin.com/in/paulina-sawaniewska-278030407/).
