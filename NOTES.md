# Development Notes

Running list of data limitations and decisions to include in the final README.

## Limitations

- **Scope limited by robots.txt**: /posting/ and /api/ are disallowed,
  so all data comes from the search results listing only — no access to
  full job descriptions or detail pages. This is the root cause of
  several limitations below.

- **Related job titles included by design**: since the project scope
  covers analytical roles broadly (Data, Business, and BI Analyst), data
  was collected across four related search terms ("data analyst",
  "junior data analyst", "business analyst", "bi analyst") and
  deduplicated by URL. This approach also worked around the site's
  ~90-100 result cap per single search term.

- **Non-analyst offers filtered by title**: search results included some
  offers unrelated to analytical roles (e.g. "Project Manager", "Java
  Developer"), likely matched by the site's search on description content
  rather than exact job title. Offers were kept only if their title
  contains "Analyst", "Analityk", "Analytics", or "Analiz" (~27 offers
  removed, ~8% of the scraped dataset). One borderline case ("Data
  Solution Designer with Python") was excluded despite topical relevance,
  as a simple, consistent rule was preferred over manual exceptions.

- **Incomplete salary ranges**: offers showing only a single flat amount
  (no min-max range) result in `mid_salary` being NaN rather than falling
  back to `salary_min`. Affects 2 offers (~0.6%) — treated as missing data
  rather than assuming min == typical salary.

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
  tags offers with job role names (e.g. "Business Analyst", 40
  occurrences after title filtering) and overly broad category tags
  (e.g. "Business Analysis", "Data") alongside actual skills, all using
  the same tag type. Language requirements ("angielski"/"polski") are
  also tagged this way. All of these were excluded from
  skills_clean.csv, as none represent an actual technical or soft skill.
  Rarer role-like tags (e.g. "Project Manager", "Product Manager") were
  left, as their low frequency doesn't affect the ranking in practice.