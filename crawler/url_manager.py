import logging
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag


logger = logging.getLogger(__name__)


class URLManager:
    """
    Manages URLs for the web crawler.

    Responsibilities:
    - Maintain a queue of URLs to crawl
    - Track visited URLs
    - Prevent duplicate URLs
    - Normalize URLs
    - Convert relative URLs to absolute URLs
    - Restrict crawling to the target domain
    - Ignore unsupported URL schemes and resources
    - Limit the maximum number of pages
    """

    def __init__(self, start_url, max_pages=100):
        """
        Initialize the URL manager.

        Args:
            start_url (str): The initial URL of the website.
            max_pages (int): Maximum number of URLs that can be crawled.
        """

        if not self.is_valid_http_url(start_url):
            raise ValueError("Invalid start URL")

        if not isinstance(max_pages, int) or max_pages <= 0:
            raise ValueError("max_pages must be a positive integer")

        self.start_url = self.normalize_url(start_url)

        parsed_start_url = urlparse(self.start_url)

        self.domain = parsed_start_url.netloc.lower()

        self.max_pages = max_pages

        # URLs waiting to be crawled.
        self.queue = deque()

        # URLs that have already been visited or scheduled.
        self.visited = set()

        # Add the starting URL.
        self.add_url(self.start_url)

        logger.info(
            "URL manager initialized for domain: %s",
            self.domain
        )

    # --------------------------------------------------
    # URL validation
    # --------------------------------------------------

    @staticmethod
    def is_valid_http_url(url):
        """
        Check whether a URL uses HTTP or HTTPS and
        contains a valid network location.

        Args:
            url (str): URL to validate.

        Returns:
            bool: True if valid, otherwise False.
        """

        if not isinstance(url, str):
            return False

        if not url.strip():
            return False

        try:
            parsed = urlparse(url)

            return (
                parsed.scheme.lower() in ("http", "https")
                and bool(parsed.netloc)
            )

        except ValueError:
            return False

    # --------------------------------------------------
    # URL normalization
    # --------------------------------------------------

    @staticmethod
    def normalize_url(url):
        """
        Normalize a URL.

        Currently this:
        - Removes URL fragments
        - Removes leading/trailing whitespace
        - Converts the scheme and hostname to lowercase

        Args:
            url (str): URL to normalize.

        Returns:
            str: Normalized URL.
        """

        if not isinstance(url, str):
            return url

        url = url.strip()

        try:
            parsed = urlparse(url)

            scheme = parsed.scheme.lower()

            hostname = parsed.hostname

            if hostname is None:
                return url

            hostname = hostname.lower()

            # Preserve the port if one exists.
            netloc = hostname

            if parsed.port is not None:
                netloc = f"{hostname}:{parsed.port}"

            normalized = parsed._replace(
                scheme=scheme,
                netloc=netloc,
                fragment=""
            )

            return normalized.geturl()

        except (ValueError, AttributeError):
            return url

    # --------------------------------------------------
    # Domain checking
    # --------------------------------------------------

    def is_same_domain(self, url):
        """
        Check whether a URL belongs to the target domain.

        Args:
            url (str): URL to check.

        Returns:
            bool: True if the URL belongs to the target domain.
        """

        if not self.is_valid_http_url(url):
            return False

        try:
            parsed = urlparse(url)

            return parsed.netloc.lower() == self.domain

        except ValueError:
            return False

    # --------------------------------------------------
    # Resource checking
    # --------------------------------------------------

    @staticmethod
    def is_crawlable_url(url):
        """
        Determine whether a URL represents a webpage that
        should be considered for crawling.

        Non-webpage resources such as images, PDFs, CSS,
        JavaScript and videos are ignored.

        Args:
            url (str): URL to check.

        Returns:
            bool: True if the URL can be crawled.
        """

        if not URLManager.is_valid_http_url(url):
            return False

        try:
            parsed = urlparse(url)

            path = parsed.path.lower()

            ignored_extensions = (
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".svg",
                ".webp",
                ".ico",
                ".bmp",
                ".tiff",
                ".pdf",
                ".doc",
                ".docx",
                ".xls",
                ".xlsx",
                ".ppt",
                ".pptx",
                ".zip",
                ".rar",
                ".7z",
                ".tar",
                ".gz",
                ".mp3",
                ".wav",
                ".ogg",
                ".mp4",
                ".avi",
                ".mov",
                ".mkv",
                ".webm",
                ".css",
                ".js",
                ".json",
                ".xml",
                ".rss",
                ".atom",
            )

            return not path.endswith(ignored_extensions)

        except ValueError:
            return False

    # --------------------------------------------------
    # Convert link to absolute URL
    # --------------------------------------------------

    def make_absolute_url(self, base_url, link):
        """
        Convert a relative link into an absolute URL.

        Examples:

            /about
            -> https://example.com/about

            contact
            -> https://example.com/contact

            https://example.com/about
            -> https://example.com/about

        Args:
            base_url (str): URL of the page containing the link.
            link (str): Extracted href value.

        Returns:
            str or None: Absolute URL or None if invalid.
        """

        if not isinstance(link, str):
            return None

        link = link.strip()

        if not link:
            return None

        # Ignore fragments.
        if link.startswith("#"):
            return None

        # Ignore email links.
        if link.lower().startswith("mailto:"):
            return None

        # Ignore telephone links.
        if link.lower().startswith("tel:"):
            return None

        # Ignore JavaScript links.
        if link.lower().startswith("javascript:"):
            return None

        # Ignore data URLs.
        if link.lower().startswith("data:"):
            return None

        try:
            absolute_url = urljoin(base_url, link)

            absolute_url, _ = urldefrag(absolute_url)

            if not self.is_valid_http_url(absolute_url):
                return None

            return self.normalize_url(absolute_url)

        except (ValueError, TypeError):
            return None

    # --------------------------------------------------
    # Add URL
    # --------------------------------------------------

    def add_url(self, url):
        """
        Add a URL to the crawling queue.

        The URL is added only if:
        - It is a valid HTTP/HTTPS URL
        - It belongs to the target domain
        - It represents a crawlable resource
        - It has not already been visited/scheduled
        - The page limit has not been reached

        Args:
            url (str): URL to add.

        Returns:
            bool: True if added, otherwise False.
        """

        if not self.is_valid_http_url(url):
            logger.debug(
                "Rejected invalid URL: %s",
                url
            )
            return False

        url = self.normalize_url(url)

        if not self.is_same_domain(url):
            logger.debug(
                "Rejected external URL: %s",
                url
            )
            return False

        if not self.is_crawlable_url(url):
            logger.debug(
                "Rejected non-crawlable URL: %s",
                url
            )
            return False

        if url in self.visited:
            logger.debug(
                "Rejected duplicate URL: %s",
                url
            )
            return False

        if len(self.visited) >= self.max_pages:
            logger.debug(
                "Maximum page limit reached."
            )
            return False

        self.queue.append(url)

        # Mark it immediately so it cannot be queued twice.
        self.visited.add(url)

        logger.info(
            "Added URL to queue: %s",
            url
        )

        return True

    # --------------------------------------------------
    # Add links from a page
    # --------------------------------------------------

    def add_links(self, base_url, links):
        """
        Convert and add multiple links discovered on a page.

        Args:
            base_url (str): URL of the current page.
            links (iterable): Links found on the page.

        Returns:
            int: Number of new URLs added.
        """

        added_count = 0

        for link in links:
            absolute_url = self.make_absolute_url(
                base_url,
                link
            )

            if absolute_url is None:
                continue

            if self.add_url(absolute_url):
                added_count += 1

        logger.info(
            "Added %d new URLs from %s",
            added_count,
            base_url
        )

        return added_count

    # --------------------------------------------------
    # Get next URL
    # --------------------------------------------------

    def get_next_url(self):
        """
        Retrieve the next URL from the queue.

        Returns:
            str or None: Next URL or None if the queue is empty.
        """

        if not self.queue:
            return None

        return self.queue.popleft()

    # --------------------------------------------------
    # Queue state
    # --------------------------------------------------

    def has_pending_urls(self):
        """
        Check whether URLs are waiting to be crawled.

        Returns:
            bool: True if queue contains URLs.
        """

        return len(self.queue) > 0

    def queue_size(self):
        """
        Get the current queue size.

        Returns:
            int: Number of URLs waiting.
        """

        return len(self.queue)

    def visited_count(self):
        """
        Get the number of URLs already scheduled/visited.

        Returns:
            int: Number of URLs.
        """

        return len(self.visited)

    def get_visited_urls(self):
        """
        Return all URLs that have been scheduled.

        Returns:
            set: Set containing visited URLs.
        """

        return self.visited.copy()