from bs4 import BeautifulSoup
from urllib.parse import urljoin


class HTMLParser:
    """
    Parses HTML documents and extracts structured information.

    Responsibilities:
    - Parse raw HTML
    - Extract page title
    - Extract HTML language
    - Extract headings
    - Extract images
    - Extract links
    - Extract forms
    - Extract metadata
    - Extract page text

    Accessibility evaluation is NOT performed here.
    That will be handled by the accessibility engine.
    """

    def __init__(self, html, base_url=None):
        """
        Initialize the HTML parser.

        Args:
            html (str): Raw HTML content.
            base_url (str): URL of the page being parsed.
                           Used to convert relative links
                           into absolute URLs.
        """

        if not isinstance(html, str):
            raise TypeError("html must be a string")

        self.html = html
        self.base_url = base_url

        self.soup = BeautifulSoup(
            html,
            "html.parser"
        )

    # --------------------------------------------------
    # Page information
    # --------------------------------------------------

    def get_title(self):
        """
        Extract the page title.

        Returns:
            str or None: Page title.
        """

        title = self.soup.find("title")

        if title is None:
            return None

        return title.get_text(strip=True)

    def get_language(self):
        """
        Extract the language from the <html> element.

        Example:

            <html lang="en">

        Returns:
            str or None: Language value.
        """

        html_tag = self.soup.find("html")

        if html_tag is None:
            return None

        language = html_tag.get("lang")

        if language is None:
            return None

        return language.strip() or None

    # --------------------------------------------------
    # Headings
    # --------------------------------------------------

    def get_headings(self):
        """
        Extract all headings from h1 through h6.

        Returns:
            list: List of dictionaries containing heading
                  level and text.
        """

        headings = []

        for heading in self.soup.find_all(
            ["h1", "h2", "h3", "h4", "h5", "h6"]
        ):
            level = int(heading.name[1:])

            text = heading.get_text(
                " ",
                strip=True
            )

            headings.append({
                "level": level,
                "text": text
            })

        return headings

    # --------------------------------------------------
    # Images
    # --------------------------------------------------

    def get_images(self):
        """
        Extract all images.

        Returns:
            list: List of image information.
        """

        images = []

        for image in self.soup.find_all("img"):
            images.append({
                "src": image.get("src"),
                "alt": image.get("alt"),
                "has_alt_attribute": image.has_attr("alt")
            })

        return images

    # --------------------------------------------------
    # Links
    # --------------------------------------------------

    def get_links(self):
        """
        Extract links from <a> elements.

        Relative URLs are converted into absolute URLs
        when a base URL is provided.

        Returns:
            list: List of link information.
        """

        links = []

        for anchor in self.soup.find_all("a"):
            href = anchor.get("href")

            text = anchor.get_text(
                " ",
                strip=True
            )

            absolute_url = self._make_absolute_url(href)

            links.append({
                "href": href,
                "url": absolute_url,
                "text": text
            })

        return links

    def _make_absolute_url(self, href):
        """
        Convert a relative URL to an absolute URL.

        Args:
            href (str or None): Link target.

        Returns:
            str or None: Absolute URL.
        """

        if href is None:
            return None

        href = href.strip()

        if not href:
            return None

        if self.base_url is None:
            return href

        return urljoin(
            self.base_url,
            href
        )

    # --------------------------------------------------
    # Forms
    # --------------------------------------------------

    def get_forms(self):
        """
        Extract forms and their controls.

        Returns:
            list: List of forms.
        """

        forms = []

        for form in self.soup.find_all("form"):
            controls = []

            for control in form.find_all(
                ["input", "select", "textarea", "button"]
            ):
                controls.append({
                    "tag": control.name,
                    "type": control.get("type"),
                    "name": control.get("name"),
                    "id": control.get("id"),
                    "value": control.get("value")
                })

            forms.append({
                "action": form.get("action"),
                "method": form.get(
                    "method",
                    "get"
                ).lower(),
                "controls": controls
            })

        return forms

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def get_metadata(self):
        """
        Extract common metadata.

        Returns:
            dict: Metadata information.
        """

        metadata = {
            "charset": None,
            "description": None,
            "viewport": None
        }

        # <meta charset="UTF-8">
        charset_tag = self.soup.find(
            "meta",
            charset=True
        )

        if charset_tag:
            metadata["charset"] = charset_tag.get(
                "charset"
            )

        # <meta name="description" content="...">
        description_tag = self.soup.find(
            "meta",
            attrs={
                "name": lambda value:
                    value and value.lower() == "description"
            }
        )

        if description_tag:
            metadata["description"] = (
                description_tag.get("content")
            )

        # <meta name="viewport" content="...">
        viewport_tag = self.soup.find(
            "meta",
            attrs={
                "name": lambda value:
                    value and value.lower() == "viewport"
            }
        )

        if viewport_tag:
            metadata["viewport"] = (
                viewport_tag.get("content")
            )

        return metadata

    # --------------------------------------------------
    # Page text
    # --------------------------------------------------

    def get_text(self):
        """
        Extract visible page text.

        Script and style elements are removed first.

        Returns:
            str: Extracted text.
        """

        for element in self.soup(
            ["script", "style", "noscript"]
        ):
            element.decompose()

        return self.soup.get_text(
            " ",
            strip=True
        )

    # --------------------------------------------------
    # Complete parse
    # --------------------------------------------------

    def parse(self):
        """
        Extract all currently supported page information.

        Returns:
            dict: Structured page information.
        """

        return {
            "title": self.get_title(),
            "language": self.get_language(),
            "headings": self.get_headings(),
            "images": self.get_images(),
            "links": self.get_links(),
            "forms": self.get_forms(),
            "metadata": self.get_metadata(),
            "text": self.get_text()
        }