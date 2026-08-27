"""
Reusable helper functions for cleaning job posting data.
"""


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