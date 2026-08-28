from cleaning.utils import check_english, get_experience_level, is_excluded_business_analyst


def test_check_english_returns_true_when_english_present():
    result = check_english(["SQL", "angielski", "Python"])
    assert result == True


def test_check_english_returns_false_when_english_not_present():
    result = check_english(["SQL", "Python"])
    assert result == False


def test_get_experience_level_detects_senior():
    result = get_experience_level("Senior Data Analyst")
    assert result == "Senior"


def test_get_experience_level_detects_junior():
    result = get_experience_level("Junior Data Analyst")
    assert result == "Junior"


def test_get_experience_level_returns_not_specified_when_no_level():
    result = get_experience_level("Data Analyst")
    assert result == "Not specified"


def test_excludes_pure_business_analyst():
    result = is_excluded_business_analyst("Senior Business Analyst")
    assert result == True


def test_keeps_data_business_analyst_hybrid():
    result = is_excluded_business_analyst("Data Business Analyst")
    assert result == False


def test_keeps_regular_data_analyst():
    result = is_excluded_business_analyst("Data Analyst")
    assert result == False