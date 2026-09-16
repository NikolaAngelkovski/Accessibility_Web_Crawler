def title_check(page_data):
    """
    Check whether the webpage contains a meaningful title.

    Accessibility requirement:
    The page should have a non-empty <title> element that
    identifies the purpose or content of the page.

    Args:
        page_data (dict): Parsed page data produced by HTMLParser.

    Returns:
        dict: Standardized accessibility rule result.
    """

    title = page_data.get("title")

    # No title element or None value.
    if title is None:
        return {
            "rule": "title_check",
            "status": "fail",
            "message": (
                "Page does not contain a title."
            ),
            "details": {
                "title": None
            }
        }

    title = str(title).strip()

    # Empty title.
    if not title:
        return {
            "rule": "title_check",
            "status": "fail",
            "message": (
                "Page contains an empty title."
            ),
            "details": {
                "title": title
            }
        }

    # A very short title is suspicious.
    #
    # We don't automatically fail it because a short title
    # can still be meaningful, for example:
    #
    #   "Home"
    #   "About"
    #   "Contact"
    #
    if len(title) < 3:
        return {
            "rule": "title_check",
            "status": "warning",
            "message": (
                "Page has a very short title that may not "
                "adequately describe the page."
            ),
            "details": {
                "title": title,
                "length": len(title)
            }
        }

    return {
        "rule": "title_check",
        "status": "pass",
        "message": (
            "Page contains a meaningful title."
        ),
        "details": {
            "title": title,
            "length": len(title)
        }
    }