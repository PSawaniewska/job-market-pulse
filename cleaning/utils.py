"""
Reusable helper functions for cleaning job posting data.
"""
import re

def check_english(skills_list):
    if "Język angielski" in skills_list or "angielski" in skills_list:
        return True
    return False

def get_experience_level(title):
    if "Junior" in title:
        return "Junior"
    elif "Senior" in title:
        return "Senior"
    elif "Mid" in title:
        return "Mid"
    else:
        return "Not specified"

def is_excluded_business_analyst(title):
    """Return True if the title is a pure Business Analyst role
    (not a Data/BI hybrid) that should be excluded from the dataset."""
    pattern = "Business.{0,3}Analyst|Business.{0,3}System.{0,3}Analyst|System.{0,3}Business.{0,3}Analyst"
    is_pure_ba = bool(re.search(pattern, title, re.IGNORECASE))
    has_data = "data" in title.lower()
    return is_pure_ba and not has_data