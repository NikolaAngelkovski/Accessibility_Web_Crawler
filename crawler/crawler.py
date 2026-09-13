import logging
from urllib.parse import urlparse

import requests


logger = logging.getLogger(__name__)


class Crawler:
    """
    Basic HTTP/HTTPS web crawler.

    Responsibilities:
    - Validate URLs
    - Fetch web pages
    - Follow redirects
    - Handle HTTP errors
    - Handle connection errors
    - Handle timeouts
    - Verify that the response is HTML
    - Return the downloaded HTML and metadata
    """

    def __init__(self, timeout=10):
        """
        Initialize the crawler.

        Args:
            timeout (int): Maximum number of seconds to wait
                           for an HTTP request.
        """
        self.timeout = timeout

        self.headers = {
            "User-Agent": "WebAccessibilityCrawler/1.0"
        }

    @staticmethod
    def is_valid_url(url):
        """
        Check whether a URL is a valid HTTP or HTTPS URL.

        Args:
            url (str): URL to validate.

        Returns:
            bool: True if the URL is valid, otherwise False.
        """
        if not isinstance(url, str) or not url.strip():
            return False

        try:
            parsed = urlparse(url)

            return (
                parsed.scheme in ("http", "https")
                and bool(parsed.netloc)
            )

        except ValueError:
            return False

    def fetch(self, url):
        """
        Fetch a webpage from the given URL.

        Args:
            url (str): HTTP or HTTPS URL.

        Returns:
            dict: Result containing success status, metadata,
                  HTML content, or an error message.
        """

        # -----------------------------------
        # 1. Validate URL
        # -----------------------------------
        if not self.is_valid_url(url):
            logger.warning("Invalid URL: %s", url)

            return {
                "url": url,
                "success": False,
                "error": "Invalid URL"
            }

        logger.info("Fetching URL: %s", url)

        try:
            # -----------------------------------
            # 2. Send HTTP request
            # -----------------------------------
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )

            # -----------------------------------
            # 3. Check HTTP status
            # -----------------------------------
            if response.status_code >= 400:
                logger.warning(
                    "HTTP error %s for %s",
                    response.status_code,
                    url
                )

                return {
                    "url": url,
                    "final_url": response.url,
                    "success": False,
                    "status_code": response.status_code,
                    "content_type": response.headers.get(
                        "Content-Type",
                        ""
                    ),
                    "error": f"HTTP {response.status_code}"
                }

            # -----------------------------------
            # 4. Check Content-Type
            # -----------------------------------
            content_type = response.headers.get(
                "Content-Type",
                ""
            )

            if "text/html" not in content_type.lower():
                logger.warning(
                    "Non-HTML response from %s: %s",
                    url,
                    content_type
                )

                return {
                    "url": url,
                    "final_url": response.url,
                    "success": False,
                    "status_code": response.status_code,
                    "content_type": content_type,
                    "error": "Response is not HTML"
                }

            # -----------------------------------
            # 5. Successful response
            # -----------------------------------
            logger.info(
                "Successfully fetched %s",
                response.url
            )

            return {
                "url": url,
                "final_url": response.url,
                "success": True,
                "status_code": response.status_code,
                "content_type": content_type,
                "html": response.text
            }

        # -----------------------------------
        # 6. Timeout
        # -----------------------------------
        except requests.exceptions.Timeout:
            logger.error(
                "Request timed out: %s",
                url
            )

            return {
                "url": url,
                "success": False,
                "error": "Request timed out"
            }

        # -----------------------------------
        # 7. Connection error
        # -----------------------------------
        except requests.exceptions.ConnectionError:
            logger.error(
                "Connection error: %s",
                url
            )

            return {
                "url": url,
                "success": False,
                "error": "Connection error"
            }

        # -----------------------------------
        # 8. Other requests errors
        # -----------------------------------
        except requests.exceptions.RequestException as error:
            logger.error(
                "Request failed for %s: %s",
                url,
                error
            )

            return {
                "url": url,
                "success": False,
                "error": str(error)
            }

        # -----------------------------------
        # 9. Unexpected errors
        # -----------------------------------
        except Exception as error:
            logger.exception(
                "Unexpected error while fetching %s",
                url
            )

            return {
                "url": url,
                "success": False,
                "error": str(error)
            }