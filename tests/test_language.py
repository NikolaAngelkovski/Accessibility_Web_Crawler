from accessibility.rules import language_check


def test_language_check_passes_for_valid_language():
    page_data = {
        "language": "en"
    }

    result = language_check(page_data)

    assert result["rule"] == "language_check"
    assert result["status"] == "pass"
    assert result["details"]["language"] == "en"


def test_language_check_passes_for_regional_language():
    page_data = {
        "language": "en-US"
    }

    result = language_check(page_data)

    assert result["status"] == "pass"
    assert result["details"]["language"] == "en-US"


def test_language_check_passes_for_macedonian():
    page_data = {
        "language": "mk"
    }

    result = language_check(page_data)

    assert result["status"] == "pass"
    assert result["details"]["language"] == "mk"


def test_language_check_fails_when_language_is_missing():
    page_data = {
        "language": None
    }

    result = language_check(page_data)

    assert result["rule"] == "language_check"
    assert result["status"] == "fail"
    assert result["details"]["language"] is None


def test_language_check_fails_when_language_is_empty():
    page_data = {
        "language": ""
    }

    result = language_check(page_data)

    assert result["status"] == "fail"


def test_language_check_fails_when_language_is_whitespace():
    page_data = {
        "language": "   "
    }

    result = language_check(page_data)

    assert result["status"] == "fail"


def test_language_check_warns_for_suspicious_language():
    page_data = {
        "language": "english"
    }

    result = language_check(page_data)

    assert result["rule"] == "language_check"
    assert result["status"] == "warning"


def test_language_check_warns_for_invalid_format():
    page_data = {
        "language": "en_US"
    }

    result = language_check(page_data)

    assert result["status"] == "warning"


def test_language_check_strips_whitespace():
    page_data = {
        "language": "  en  "
    }

    result = language_check(page_data)

    assert result["status"] == "pass"
    assert result["details"]["language"] == "en"


def test_language_check_returns_standard_result_structure():
    page_data = {
        "language": "mk"
    }

    result = language_check(page_data)

    assert set(result.keys()) == {
        "rule",
        "status",
        "message",
        "details"
    }