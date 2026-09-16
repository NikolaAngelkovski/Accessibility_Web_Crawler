from accessibility.rules import link_check


def test_link_check_passes_for_valid_links():
    page_data = {
        "links": [
            {
                "href": "/about",
                "url": "https://finki.ukim.mk/about",
                "text": "About"
            },
            {
                "href": "/contact",
                "url": "https://finki.ukim.mk/contact",
                "text": "Contact"
            }
        ]
    }

    result = link_check(page_data)

    assert result["rule"] == "link_check"
    assert result["status"] == "pass"
    assert result["details"]["total_links"] == 2
    assert result["details"]["links_with_text"] == 2
    assert result["details"]["links_without_text"] == 0


def test_link_check_fails_when_link_text_is_missing():
    page_data = {
        "links": [
            {
                "href": "/about",
                "url": "https://finki.ukim.mk/about",
                "text": None
            }
        ]
    }

    result = link_check(page_data)

    assert result["rule"] == "link_check"
    assert result["status"] == "fail"
    assert result["details"]["links_without_text"] == 1


def test_link_check_fails_when_link_text_is_empty():
    page_data = {
        "links": [
            {
                "href": "/about",
                "url": "https://finki.ukim.mk/about",
                "text": ""
            }
        ]
    }

    result = link_check(page_data)

    assert result["status"] == "fail"


def test_link_check_fails_when_link_text_is_whitespace():
    page_data = {
        "links": [
            {
                "href": "/about",
                "url": "https://finki.ukim.mk/about",
                "text": "   "
            }
        ]
    }

    result = link_check(page_data)

    assert result["status"] == "fail"


def test_link_check_warns_when_destination_is_missing():
    page_data = {
        "links": [
            {
                "href": None,
                "url": None,
                "text": "About"
            }
        ]
    }

    result = link_check(page_data)

    assert result["rule"] == "link_check"
    assert result["status"] == "warning"
    assert result["details"]["links_without_destination"] == 1


def test_link_check_warns_when_destination_is_empty():
    page_data = {
        "links": [
            {
                "href": "",
                "url": "",
                "text": "About"
            }
        ]
    }

    result = link_check(page_data)

    assert result["status"] == "warning"


def test_link_check_fails_before_warning_when_both_problems_exist():
    page_data = {
        "links": [
            {
                "href": None,
                "url": None,
                "text": ""
            }
        ]
    }

    result = link_check(page_data)

    assert result["status"] == "fail"
    assert result["details"]["links_without_text"] == 1
    assert result["details"]["links_without_destination"] == 1


def test_link_check_handles_multiple_links():
    page_data = {
        "links": [
            {
                "href": "/one",
                "url": "https://finki.ukim.mk/one",
                "text": "One"
            },
            {
                "href": "/two",
                "url": "https://finki.ukim.mk/two",
                "text": "Two"
            },
            {
                "href": "/three",
                "url": "https://finki.ukim.mk/three",
                "text": "Three"
            }
        ]
    }

    result = link_check(page_data)

    assert result["status"] == "pass"
    assert result["details"]["total_links"] == 3
    assert result["details"]["links_with_text"] == 3


def test_link_check_passes_when_page_has_no_links():
    page_data = {
        "links": []
    }

    result = link_check(page_data)

    assert result["status"] == "pass"
    assert result["details"]["total_links"] == 0


def test_link_check_handles_missing_link_data():
    page_data = {}

    result = link_check(page_data)

    assert result["status"] == "error"


def test_link_check_handles_invalid_link_data():
    page_data = {
        "links": [
            "invalid link"
        ]
    }

    result = link_check(page_data)

    assert result["status"] == "error"


def test_link_check_strips_link_text():
    page_data = {
        "links": [
            {
                "href": "/about",
                "url": "https://finki.ukim.mk/about",
                "text": "  About Us  "
            }
        ]
    }

    result = link_check(page_data)

    assert result["status"] == "pass"
    assert (
        result["details"]["links_with_text_details"][0]["text"]
        == "About Us"
    )


def test_link_check_records_link_details():
    page_data = {
        "links": [
            {
                "href": "/about",
                "url": "https://finki.ukim.mk/about",
                "text": "About"
            }
        ]
    }

    result = link_check(page_data)

    details = result["details"]["links_with_text_details"][0]

    assert details["href"] == "/about"
    assert details["url"] == "https://finki.ukim.mk/about"
    assert details["text"] == "About"


def test_link_check_returns_standard_result_structure():
    page_data = {
        "links": [
            {
                "href": "/about",
                "url": "https://finki.ukim.mk/about",
                "text": "About"
            }
        ]
    }

    result = link_check(page_data)

    assert set(result.keys()) == {
        "rule",
        "status",
        "message",
        "details"
    }