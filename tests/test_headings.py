from accessibility.rules import heading_check


def test_heading_check_passes_for_valid_structure():
    page_data = {
        "headings": [
            {"level": 1, "text": "Main heading"},
            {"level": 2, "text": "Section 1"},
            {"level": 2, "text": "Section 2"},
            {"level": 3, "text": "Subsection"}
        ]
    }

    result = heading_check(page_data)

    assert result["rule"] == "heading_check"
    assert result["status"] == "pass"


def test_heading_check_fails_when_h1_is_missing():
    page_data = {
        "headings": [
            {"level": 2, "text": "Section"},
            {"level": 3, "text": "Subsection"}
        ]
    }

    result = heading_check(page_data)

    assert result["status"] == "fail"
    assert result["details"]["h1_count"] == 0


def test_heading_check_warns_for_multiple_h1_elements():
    page_data = {
        "headings": [
            {"level": 1, "text": "Main heading"},
            {"level": 1, "text": "Another main heading"}
        ]
    }

    result = heading_check(page_data)

    assert result["status"] == "warning"
    assert result["details"]["h1_count"] == 2


def test_heading_check_warns_for_skipped_heading_level():
    page_data = {
        "headings": [
            {"level": 1, "text": "Main heading"},
            {"level": 2, "text": "Section"},
            {"level": 4, "text": "Subsection"}
        ]
    }

    result = heading_check(page_data)

    assert result["status"] == "warning"
    assert result["details"]["skipped_levels"] == [
        {
            "from": 2,
            "to": 4
        }
    ]


def test_heading_check_passes_when_heading_levels_are_sequential():
    page_data = {
        "headings": [
            {"level": 1, "text": "Main"},
            {"level": 2, "text": "Section"},
            {"level": 3, "text": "Subsection"},
            {"level": 4, "text": "Details"}
        ]
    }

    result = heading_check(page_data)

    assert result["status"] == "pass"


def test_heading_check_warns_for_empty_heading():
    page_data = {
        "headings": [
            {"level": 1, "text": "Main"},
            {"level": 2, "text": ""}
        ]
    }

    result = heading_check(page_data)

    assert result["status"] == "warning"
    assert len(result["details"]["empty_headings"]) == 1


def test_heading_check_warns_for_whitespace_heading():
    page_data = {
        "headings": [
            {"level": 1, "text": "Main"},
            {"level": 2, "text": "   "}
        ]
    }

    result = heading_check(page_data)

    assert result["status"] == "warning"


def test_heading_check_handles_no_headings():
    page_data = {
        "headings": []
    }

    result = heading_check(page_data)

    assert result["status"] == "fail"
    assert result["details"]["h1_count"] == 0
    assert result["details"]["heading_count"] == 0


def test_heading_check_handles_missing_heading_data():
    page_data = {}

    result = heading_check(page_data)

    assert result["status"] == "error"


def test_heading_check_handles_invalid_heading_data():
    page_data = {
        "headings": [
            "invalid heading"
        ]
    }

    result = heading_check(page_data)

    assert result["status"] == "error"


def test_heading_check_handles_invalid_heading_level():
    page_data = {
        "headings": [
            {"level": 7, "text": "Invalid heading"}
        ]
    }

    result = heading_check(page_data)

    assert result["status"] == "error"


def test_heading_check_handles_non_integer_level():
    page_data = {
        "headings": [
            {"level": "1", "text": "Main heading"}
        ]
    }

    result = heading_check(page_data)

    assert result["status"] == "error"


def test_heading_check_returns_standard_result_structure():
    page_data = {
        "headings": [
            {"level": 1, "text": "Main heading"}
        ]
    }

    result = heading_check(page_data)

    assert set(result.keys()) == {
        "rule",
        "status",
        "message",
        "details"
    }