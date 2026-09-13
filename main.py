import logging

from crawler import Crawler, URLManager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    start_url = "https://example.com"

    crawler = Crawler(timeout=10)

    url_manager = URLManager(
        start_url=start_url,
        max_pages=10
    )

    while url_manager.has_pending_urls():
        url = url_manager.get_next_url()

        print(f"\nCrawling: {url}")

        result = crawler.fetch(url)

        if not result["success"]:
            print(
                f"Failed to crawl {url}: "
                f"{result['error']}"
            )
            continue

        print(
            f"Successfully fetched "
            f"{result['final_url']}"
        )

        print(
            f"Status code: "
            f"{result['status_code']}"
        )

        print(
            f"HTML size: "
            f"{len(result['html'])} characters"
        )

        # ------------------------------------------------
        # Temporary link demonstration
        # ------------------------------------------------
        #
        # Feature 4 will extract links properly using
        # an HTML parser.
        #
        # For now, the URL manager itself is ready to
        # receive links.
        #
        # Example:
        #
        # links = [
        #     "/about",
        #     "/contact"
        # ]
        #
        # url_manager.add_links(url, links)

    print("\nCrawling finished.")

    print(
        f"URLs scheduled: "
        f"{url_manager.visited_count()}"
    )


if __name__ == "__main__":
    main()