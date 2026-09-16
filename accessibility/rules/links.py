def link_check(page_data):
    """
    Check the accessibility of links on a webpage.

    The rule checks:

    - Whether link information is available.
    - Whether links contain visible text.
    - Whether links have a usable destination.
    - Whether links use only whitespace as their text.

    Args:
        page_data (dict): Parsed page data produced by HTMLParser.

    Returns:
        dict: Standardized accessibility rule result.
    """

    links = page_data.get("links")

    if not isinstance(links, list):
        return {
            "rule": "link_check",
            "status": "error",
            "message": (
                "Link information could not be evaluated."
            ),
            "details": None
        }

    # A page without links has nothing to evaluate.
    if not links:
        return {
            "rule": "link_check",
            "status": "pass",
            "message": (
                "Page does not contain any links."
            ),
            "details": {
                "total_links": 0,
                "links_with_text": 0,
                "links_without_text": 0,
                "links_without_destination": 0
            }
        }

    links_with_text = []
    links_without_text = []
    links_without_destination = []

    for index, link in enumerate(links):

        if not isinstance(link, dict):
            return {
                "rule": "link_check",
                "status": "error",
                "message": (
                    "Invalid link data was provided."
                ),
                "details": {
                    "index": index
                }
            }

        text = link.get("text")
        url = link.get("url")
        href = link.get("href")

        # Check whether the link has visible text.
        if text is None or not str(text).strip():
            links_without_text.append({
                "index": index,
                "href": href,
                "url": url
            })
        else:
            links_with_text.append({
                "index": index,
                "href": href,
                "url": url,
                "text": str(text).strip()
            })

        # Check whether the link has a destination.
        #
        # Some links may intentionally have no destination,
        # such as placeholder anchors. These are reported
        # separately from missing link text.
        if url is None or not str(url).strip():
            links_without_destination.append({
                "index": index,
                "href": href
            })

    details = {
        "total_links": len(links),
        "links_with_text": len(links_with_text),
        "links_without_text": len(links_without_text),
        "links_without_destination": len(
            links_without_destination
        ),
        "links_with_text_details": links_with_text,
        "links_without_text_details": links_without_text,
        "links_without_destination_details": (
            links_without_destination
        )
    }

    # Empty links are an accessibility failure because users
    # may not know what the link is for.
    if links_without_text:
        return {
            "rule": "link_check",
            "status": "fail",
            "message": (
                "One or more links do not contain visible text."
            ),
            "details": details
        }

    # Links without destinations are reported as warnings.
    if links_without_destination:
        return {
            "rule": "link_check",
            "status": "warning",
            "message": (
                "One or more links do not have a usable destination."
            ),
            "details": details
        }

    return {
        "rule": "link_check",
        "status": "pass",
        "message": (
            "All links contain text and have destinations."
        ),
        "details": details
    }