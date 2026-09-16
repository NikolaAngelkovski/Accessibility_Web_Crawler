import logging

from crawler import Crawler, URLManager
from parser import HTMLParser


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

        # -----------------------------------------
        # Fetch page
        # -----------------------------------------

        result = crawler.fetch(url)

        if not result["success"]:
            print(
                f"Failed to crawl {url}: "
                f"{result['error']}"
            )
            continue

        print(
            f"Successfully fetched: "
            f"{result['final_url']}"
        )

        # -----------------------------------------
        # Parse HTML
        # -----------------------------------------

        parser = HTMLParser(
            html=result["html"],
            base_url=result["final_url"]
        )

        parsed_page = parser.parse()

        # -----------------------------------------
        # Display extracted information
        # -----------------------------------------

        print(
            f"Title: "
            f"{parsed_page['title']}"
        )

        print(
            f"Language: "
            f"{parsed_page['language']}"
        )

        print(
            f"Headings: "
            f"{len(parsed_page['headings'])}"
        )

        print(
            f"Images: "
            f"{len(parsed_page['images'])}"
        )

        print(
            f"Links: "
            f"{len(parsed_page['links'])}"
        )

        print(
            f"Forms: "
            f"{len(parsed_page['forms'])}"
        )

        # -----------------------------------------
        # Add discovered links to URL manager
        # -----------------------------------------
        #
        # This connects Feature 4 to Feature 3.
        #
        # The URL manager decides which links are
        # actually allowed into the crawl queue.
        # -----------------------------------------

        links = [
            link["url"]
            for link in parsed_page["links"]
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