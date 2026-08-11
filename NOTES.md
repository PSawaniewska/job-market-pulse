# Development Notes

Running list of data limitations and decisions to include in the final README.

## Limitations

- **Scope limited by robots.txt**: /posting/ and /api/ are disallowed,
  so all data comes from the search results listing only — no access to
  full job descriptions or detail pages. This is the root cause of
  several limitations below.

- **Related job titles included by design**: since the project scope
  covers Data and BI Analyst roles, data was collected across multiple
  related search terms (e.g. "data analyst", "junior data analyst",
  "bi analyst") rather than a single one, as any single search term
  alone returned too few results (the site caps results at ~90-100 per
  search term) to reach a workable dataset size.

- **Non-analyst offers filtered by title**: search results included some
  offers unrelated to analytical roles (e.g. "Project Manager", "Java
  Developer"), likely matched by the site's search on description content
  rather than exact job title. Offers were kept only if their title
  contains "Analyst", "Analityk", "Analytics", or "Analiz" (~27 offers
  removed at this stage). One borderline case ("Data Solution Designer
  with Python") was excluded despite topical relevance, as a simple,
  consistent rule was preferred over manual exceptions.

- **Business Analyst roles excluded after reviewing skill overlap**:
  initial data included both Data/BI Analyst and Business Analyst
  postings. Reviewing the skills breakdown showed Business Analyst
  requires a distinctly different skill set (UML/BPMN, process modeling)
  that would distort a skills analysis meant to reflect Data/BI Analyst
  work. Titles matching "Business Analyst" (including variants like
  "Business-System Analyst") were excluded unless they also mentioned
  "Data" (e.g. "Data Business Analyst" was kept). Two exclusion approaches
  were tested: excluding all titles containing "Business" (97 offers
  remaining) vs. this more targeted approach (118 offers remaining,
  114 after full cleaning) — the targeted approach was chosen to avoid
  losing legitimately relevant hybrid roles. This reduced the dataset
  from 312 to 114 offers, prioritizing thematic consistency over volume.

- **Incomplete salary ranges**: offers showing only a single flat amount
  (no min-max range) would result in `mid_salary` being NaN rather than
  falling back to `salary_min` — treating them as missing data would be
  more honest than assuming min == typical salary. No offers in the
  final dataset currently have this issue.

- **Multi-location offers**: offers listed at multiple cities (e.g.
  "Warszawa +6") are recorded only under their primary/first listed city
  shown on the results card — full location lists are only available on
  the (disallowed) detail page. May underrepresent the true geographic
  reach of some postings.

- **English requirement likely underrepresented**: `has_english` is True
  only when "Język angielski"/"angielski" appears as an explicit skill tag.
  Offers that mention English only within the full job description
  (not accessible due to robots.txt) are recorded as False, so the true
  share of English-requiring offers may be higher than shown.

- **Non-skill tags excluded from skill-frequency analysis**: the site
  tags offers with job role names (e.g. "Business Analyst", "Business
  Analysis") and other non-skill categories ("Data") alongside actual
  skills, all using the same tag type. Language requirements
  ("angielski"/"polski") are also tagged this way. All were excluded
  from skills_clean.csv, as none represent an actual technical or soft
  skill. Rarer role-like tags (e.g. "Project Manager") appear too
  infrequently to affect the ranking and were left as-is.

- **Seniority level data is too sparse**: only about 18% of job titles
  say "Junior", "Mid", or "Senior". "Mid" appears in just 2 titles. Because
  of this, we used a simple average instead of a median for salary by
  level, and the result should be treated as rough, not exact.

- **Top companies list mixes agencies and direct employers**: several
  top posters (e.g. Scalo, Ework Group, Link Group, Antal, Devire) are
  recruitment agencies or software houses hiring for clients, not the
  actual employer. This wasn't distinguished in the data, so the
  ranking reflects "who posted the most", not "who's building the
  largest analyst team".