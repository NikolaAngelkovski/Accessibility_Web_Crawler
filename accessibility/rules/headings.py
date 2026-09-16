def heading_check(page_data):
    """
    Check the heading structure of a webpage.

    The rule checks:

    - Whether the page contains an h1 heading.
    - Whether the page contains more than one h1 heading.
    - Whether heading levels skip levels.
    - Whether headings contain text.

    Args:
        page_data (dict): Parsed page data produced by HTMLParser.

    Returns:
        dict: Standardized accessibility rule result.
    """

    headings = page_data.get("headings")

    # The parser normally returns a list.
    # Treat missing/invalid heading data as an error.
    if not isinstance(headings, list):
        return {
            "rule": "heading_check",
            "status": "error",
            "message": (
                "Heading information could not be evaluated."
            ),
            "details": None
        }

    h1_count = 0
    empty_headings = []
    levels = []

    for index, heading in enumerate(headings):

        if not isinstance(heading, dict):
            return {
                "rule": "heading_check",
                "status": "error",
                "message": (
                    "Invalid heading data was provided."
                ),
                "details": {
                    "index": index
                }
            }

        level = heading.get("level")
        text = heading.get("text")

        if not isinstance(level, int) or level < 1 or level > 6:
            return {
                "rule": "heading_check",
                "status": "error",
                "message": (
                    "Invalid heading level detected."
                ),
                "details": {
                    "index": index,
                    "level": level
                }
            }

        levels.append(level)

        if level == 1:
            h1_count += 1

        if text is None or not str(text).strip():
            empty_headings.append({
                "index": index,
                "level": level
            })

    # A page should have a primary heading.
    if h1_count == 0:
        return {
            "rule": "heading_check",
            "status": "fail",
            "message": (
                "Page does not contain an h1 heading."
            ),
            "details": {
                "h1_count": h1_count,
                "heading_count": len(headings),
                "levels": levels,
                "empty_headings": empty_headings
            }
        }

    # Multiple h1 elements are reported as a warning rather
    # than an automatic failure. Modern HTML can technically
    # contain multiple h1 elements, although a single clear
    # page-level heading is easier to interpret.
    if h1_count > 1:
        return {
            "rule": "heading_check",
            "status": "warning",
            "message": (
                "Page contains multiple h1 headings."
            ),
            "details": {
                "h1_count": h1_count,
                "heading_count": len(headings),
                "levels": levels,
                "empty_headings": empty_headings
            }
        }

    # Check for heading level jumps.
    #
    # Example:
    #
    # h1 -> h2 -> h3      OK
    # h1 -> h2 -> h4      WARNING
    #
    # We only care about jumps greater than one level.
    skipped_levels = []

    for previous, current in zip(levels, levels[1:]):
        if current > previous + 1:
            skipped_levels.append({
                "from": previous,
                "to": current
            })

    if skipped_levels:
        return {
            "rule": "heading_check",
            "status": "warning",
            "message": (
                "Heading levels skip one or more levels."
            ),
            "details": {
                "h1_count": h1_count,
                "heading_count": len(headings),
                "levels": levels,
                "skipped_levels": skipped_levels,
                "empty_headings": empty_headings
            }
        }

    # Empty headings can make the heading structure less useful.
    if empty_headings:
        return {
            "rule": "heading_check",
            "status": "warning",
            "message": (
                "Page contains headings without text."
            ),
            "details": {
                "h1_count": h1_count,
                "heading_count": len(headings),
                "levels": levels,
                "empty_headings": empty_headings
            }
        }

    return {
        "rule": "heading_check",
        "status": "pass",
        "message": (
            "Page has a valid heading structure."
        ),
        "details": {
            "h1_count": h1_count,
            "heading_count": len(headings),
            "levels": levels,
            "empty_headings": []
        }
    }