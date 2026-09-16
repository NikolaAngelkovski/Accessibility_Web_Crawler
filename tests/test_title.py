from accessibility.rules import title_check


def test_title_check_passes_for_normal_title():
    page_data = {
        "title": "FINKI - Faculty of Computer Science"
    }

    result = title_check(page_data)

    assert result["rule"] == "title_check"
    assert result["status"] == "pass"
    assert (
        result["details"]["title"]
        == "FINKI - Faculty of Computer Science"
    )


def test_title_check_passes_for_short_but_meaningful_title():
    page_data = {
        "title": "FAQ"
    }

    result = title_check(page_data)

    assert result["status"] == "pass"


def test_title_check_passes_for_home_title():
    page_data = {
        "title": "Home"
    }

    result = title_check(page_data)

    assert result["status"] == "pass"


def test_title_check_fails_when_title_is_missing():
    page_data = {
        "title": None
    }

    result = title_check(page_data)

    assert result["rule"] == "title_check"
    assert result["status"] == "fail"
    assert result["details"]["title"] is None


def test_title_check_fails_when_title_is_empty():
    page_data = {
        "title": ""
    }

    result = title_check(page_data)

    assert result["status"] == "fail"


def test_title_check_fails_when_title_contains_only_whitespace():
    page_data = {
        "title": "   "
    }

    result = title_check(page_data)

    assert result["status"] == "fail"


def test_title_check_warns_for_very_short_title():
    page_data = {
        "title": "A"
    }

    result = title_check(page_data)

    assert result["rule"] == "title_check"
    assert result["status"] == "warning"


def test_title_check_warns_for_two_character_title():
    page_data = {
        "title": "AB"
    }

    result = title_check(page_data)

    assert result["status"] == "warning"


def test_title_check_strips_whitespace():
    page_data = {
        "title": "  Home Page  "
    }

    result = title_check(page_data)

    assert result["status"] == "pass"
    assert result["details"]["title"] == "Home Page"


def test_title_check_returns_title_length():
    page_data = {
        "title": "About Us"
    }

    result = title_check(page_data)

    assert result["details"]["length"] == len("About Us")


def test_title_check_returns_standard_result_structure():
    page_data = {
        "title": "Example Page"
    }

    result = title_check(page_data)

    assert set(result.keys()) == {
        "rule",
        "status",
        "message",
        "details"
    }