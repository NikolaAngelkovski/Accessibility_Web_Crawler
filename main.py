import logging

from crawler import Crawler, URLManager
from parser import HTMLParser
from accessibility import AccessibilityEvaluator


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def example_rule(page_data):
    """
    Temporary accessibility rule used to demonstrate
    the accessibility engine.

    Real accessibility rules will be added in
    Features 6-11.
    """

    title = page_data.get("title")

    if title:
        return {
            "rule": "example_title_check",
            "status": "pass",
            "message": "Page contains a title.",
            "details": {
                "title": title
            }
        }

    return {
        "rule": "example_title_check",
        "status": "fail",
        "message": "Page does not contain a title.",
        "details": None
    }


def main():
    start_url = "https://finki.ukim.mk"

    crawler = Crawler(
        timeout=10
    )

    url_manager = URLManager(
        start_url=start_url,
        max_pages=10
    )

    evaluator = AccessibilityEvaluator()

    # Temporary rule for Feature 5.
    evaluator.register_rule(
        example_rule
    )

    while url_manager.has_pending_urls():

        url = url_manager.get_next_url()

        print(f"\nCrawling: {url}")

        # -----------------------------------------
        # Fetch page
        # -----------------------------------------

        crawl_result = crawler.fetch(url)

        if not crawl_result["success"]:
            print(
                f"Failed to crawl {url}: "
                f"{crawl_result['error']}"
            )
            continue

        # -----------------------------------------
        # Parse HTML
        # -----------------------------------------

        parser = HTMLParser(
            html=crawl_result["html"],
            base_url=crawl_result["final_url"]
        )

        page_data = parser.parse()

        # -----------------------------------------
        # Display parsed information
        # -----------------------------------------

        print(
            f"Title: "
            f"{page_data['title']}"
        )

        print(
            f"Language: "
            f"{page_data['language']}"
        )

        print(
            f"Headings: "
            f"{len(page_data['headings'])}"
        )

        print(
            f"Images: "
            f"{len(page_data['images'])}"
        )

        print(
            f"Links: "
            f"{len(page_data['links'])}"
        )

        print(
            f"Forms: "
            f"{len(page_data['forms'])}"
        )

        # -----------------------------------------
        # Accessibility evaluation
        # -----------------------------------------

        evaluation = evaluator.evaluate(
            page_data
        )

        summary = evaluation["summary"]

        print("\nAccessibility Results:")

        print(
            f"Passed: "
            f"{summary['passed']}"
        )

        print(
            f"Warnings: "
            f"{summary['warnings']}"
        )

        print(
            f"Failed: "
            f"{summary['failed']}"
        )

        print(
            f"Errors: "
            f"{summary['errors']}"
        )

        # -----------------------------------------
        # Add discovered links
        # -----------------------------------------

        links = [
            link["url"]
            for link in page_data["links"]
            if link["url"] is not None
        ]

        url_manager.add_links(
            url,
            links
        )

    print("\nCrawling finished.")

    print(
        f"Total URLs scheduled: "
        f"{url_manager.visited_count()}"
    )


if __name__ == "__main__":
    main()