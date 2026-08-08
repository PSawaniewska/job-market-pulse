# Development Notes

Running list of data limitations and decisions to include in the final README.

## Limitations

- **Scope limited by robots.txt**: /posting/ and /api/ are disallowed,
  so all data comes from the search results listing only — no access to
  full job descriptions or detail pages. This is the root cause of
  several limitations below.

- **Incomplete salary ranges**: offers showing only a single flat amount
  (no min-max range) result in `mid_salary` being NaN rather than falling
  back to `salary_min`. Affects ~1% of offers — treated as missing data
  rather than assuming min == typical salary.

- **Multi-location offers**: offers listed at multiple cities (e.g.
  "Warszawa +6") are recorded only under their primary/first listed city
  shown on the results card — full location lists are only available on
  the (disallowed) detail page. May underrepresent the true geographic
  reach of some postings.

- **Related job titles included**: to work around the site's ~90-100
  result cap per single search, data was collected across four related
  search terms ("data analyst", "junior data analyst", "business analyst",
  "bi analyst") and deduplicated by URL. This broadens the dataset beyond
  strictly "Data Analyst"-titled postings.

- **English requirement likely underrepresented**: `has_english` is True
  only when "Język angielski"/"angielski" appears as an explicit skill tag.
  Offers that mention English only within the full job description
  (not accessible due to robots.txt) are recorded as False, so the true
  share of English-requiring offers may be higher than shown.

- **Role tags mixed with skill tags**: the site tags some offers with job
  role names (e.g. "Business Analyst", "Project Manager") alongside actual
  skills, since both use the same tag type. Only "Business Analyst" (53
  occurrences) was removed, as it was frequent enough to distort a
  top-skills ranking; rarer role tags were left, as they don't affect
  the ranking in practice.