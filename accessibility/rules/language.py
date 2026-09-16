import re


def language_check(page_data):
    """
    Check whether the HTML document declares a language.

    Accessibility requirement:
    The root <html> element should have a valid,
    non-empty lang attribute.

    Args:
        page_data (dict): Parsed page data produced by HTMLParser.

    Returns:
        dict: Standardized accessibility rule result.
    """

    language = page_data.get("language")

    # Missing or empty language
    if language is None or not str(language).strip():
        return {
            "rule": "language_check",
            "status": "fail",
            "message": (
                "Page does not declare a language."
            ),
            "details": {
                "language": language
            }
        }

    language = str(language).strip()

    # Basic BCP 47-style validation.
    #
    # Examples accepted:
    #   en
    #   mk
    #   en-US
    #   sr-Latn
    #   zh-Hans-CN
    #
    # This is intentionally not a complete BCP 47 parser.
    language_pattern = re.compile(
        r"^[A-Za-z]{2,3}"
        r"(?:-[A-Za-z0-9]{2,8})*$"
    )

    if not language_pattern.fullmatch(language):
        return {
            "rule": "language_check",
            "status": "warning",
            "message": (
                "Page declares a language, but the language "
                "value may be malformed."
            ),
            "details": {
                "language": language
            }
        }

    return {
        "rule": "language_check",
        "status": "pass",
        "message": (
            "Page declares a valid language."
        ),
        "details": {
            "language": language
        }
    }