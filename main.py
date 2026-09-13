import logging

from crawler import Crawler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    crawler = Crawler(timeout=10)

    url = "https://google.com"

    result = crawler.fetch(url)

    if result["success"]:
        print("Crawl successful!")
        print(f"Original URL: {result['url']}")
        print(f"Final URL: {result['final_url']}")
        print(f"Status code: {result['status_code']}")
        print(f"Content type: {result['content_type']}")

        print("\nHTML preview:")
        print(result["html"][:500])

    else:
        print("Crawl failed!")
        print(f"URL: {result['url']}")
        print(f"Error: {result['error']}")


if __name__ == "__main__":
    main()