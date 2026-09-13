import pytest

from crawler import URLManager


# ==================================================
# Initialization
# ==================================================

def test_url_manager_initialization():
    manager = URLManager(
        "https://example.com",
        max_pages=10
    )

    assert manager.domain == "example.com"
    assert manager.max_pages == 10
    assert manager.queue_size() == 1
    assert manager.visited_count() == 1


def test_invalid_start_url():
    with pytest.raises(ValueError):
        URLManager(
            "not-a-valid-url"
        )


def test_invalid_max_pages():
    with pytest.raises(ValueError):
        URLManager(
            "https://example.com",
            max_pages=0
        )


# ==================================================
# URL validation
# ==================================================

def test_valid_http_url():
    assert URLManager.is_valid_http_url(
        "http://example.com"
    ) is True


def test_valid_https_url():
    assert URLManager.is_valid_http_url(
        "https://example.com"
    ) is True


def test_invalid_url():
    assert URLManager.is_valid_http_url(
        "not-a-url"
    ) is False


def test_empty_url():
    assert URLManager.is_valid_http_url(
        ""
    ) is False


def test_none_url():
    assert URLManager.is_valid_http_url(
        None
    ) is False


def test_ftp_url():
    assert URLManager.is_valid_http_url(
        "ftp://example.com"
    ) is False


# ==================================================
# URL normalization
# ==================================================

def test_normalize_url_removes_fragment():
    result = URLManager.normalize_url(
        "https://example.com/about#section"
    )

    assert result == "https://example.com/about"


def test_normalize_url_lowercases_scheme():
    result = URLManager.normalize_url(
        "HTTPS://example.com/about"
    )

    assert result == "https://example.com/about"


def test_normalize_url_lowercases_hostname():
    result = URLManager.normalize_url(
        "https://EXAMPLE.COM/about"
    )

    assert result == "https://example.com/about"


def test_normalize_url_strips_whitespace():
    result = URLManager.normalize_url(
        "  https://example.com/about  "
    )

    assert result == "https://example.com/about"


# ==================================================
# Domain checking
# ==================================================

def test_same_domain():
    manager = URLManager(
        "https://example.com"
    )

    assert manager.is_same_domain(
        "https://example.com/about"
    ) is True


def test_external_domain():
    manager = URLManager(
        "https://example.com"
    )

    assert manager.is_same_domain(
        "https://google.com"
    ) is False


def test_subdomain_is_not_same_domain():
    manager = URLManager(
        "https://example.com"
    )

    assert manager.is_same_domain(
        "https://blog.example.com"
    ) is False


# ==================================================
# Crawlable resources
# ==================================================

def test_html_page_is_crawlable():
    assert URLManager.is_crawlable_url(
        "https://example.com/about"
    ) is True


def test_pdf_is_not_crawlable():
    assert URLManager.is_crawlable_url(
        "https://example.com/document.pdf"
    ) is False


def test_image_is_not_crawlable():
    assert URLManager.is_crawlable_url(
        "https://example.com/image.jpg"
    ) is False


def test_css_is_not_crawlable():
    assert URLManager.is_crawlable_url(
        "https://example.com/style.css"
    ) is False


def test_javascript_is_not_crawlable():
    assert URLManager.is_crawlable_url(
        "https://example.com/script.js"
    ) is False


# ==================================================
# Absolute URL conversion
# ==================================================

def test_absolute_url():
    manager = URLManager(
        "https://example.com"
    )

    result = manager.make_absolute_url(
        "https://example.com/page",
        "https://example.com/about"
    )

    assert result == "https://example.com/about"


def test_relative_url():
    manager = URLManager(
        "https://example.com"
    )

    result = manager.make_absolute_url(
        "https://example.com/page",
        "/about"
    )

    assert result == "https://example.com/about"


def test_relative_url_without_slash():
    manager = URLManager(
        "https://example.com"
    )

    result = manager.make_absolute_url(
        "https://example.com/page/",
        "contact"
    )

    assert result == "https://example.com/page/contact"


def test_fragment_is_removed():
    manager = URLManager(
        "https://example.com"
    )

    result = manager.make_absolute_url(
        "https://example.com/page",
        "/about#team"
    )

    assert result == "https://example.com/about"


def test_mailto_link_is_ignored():
    manager = URLManager(
        "https://example.com"
    )

    result = manager.make_absolute_url(
        "https://example.com",
        "mailto:test@example.com"
    )

    assert result is None


def test_tel_link_is_ignored():
    manager = URLManager(
        "https://example.com"
    )

    result = manager.make_absolute_url(
        "https://example.com",
        "tel:+123456789"
    )

    assert result is None


def test_javascript_link_is_ignored():
    manager = URLManager(
        "https://example.com"
    )

    result = manager.make_absolute_url(
        "https://example.com",
        "javascript:void(0)"
    )

    assert result is None


def test_empty_link_is_ignored():
    manager = URLManager(
        "https://example.com"
    )

    result = manager.make_absolute_url(
        "https://example.com",
        ""
    )

    assert result is None


def test_fragment_only_link_is_ignored():
    manager = URLManager(
        "https://example.com"
    )

    result = manager.make_absolute_url(
        "https://example.com",
        "#section"
    )

    assert result is None


# ==================================================
# Queue
# ==================================================

def test_start_url_is_in_queue():
    manager = URLManager(
        "https://example.com"
    )

    assert manager.get_next_url() == (
        "https://example.com"
    )


def test_get_next_url_returns_in_order():
    manager = URLManager(
        "https://example.com"
    )

    manager.add_url(
        "https://example.com/about"
    )

    manager.add_url(
        "https://example.com/contact"
    )

    assert manager.get_next_url() == (
        "https://example.com"
    )

    assert manager.get_next_url() == (
        "https://example.com/about"
    )

    assert manager.get_next_url() == (
        "https://example.com/contact"
    )


def test_empty_queue_returns_none():
    manager = URLManager(
        "https://example.com"
    )

    manager.get_next_url()

    assert manager.get_next_url() is None


# ==================================================
# Duplicate URLs
# ==================================================

def test_duplicate_url_is_not_added():
    manager = URLManager(
        "https://example.com"
    )

    result = manager.add_url(
        "https://example.com"
    )

    assert result is False
    assert manager.queue_size() == 1


def test_duplicate_relative_urls_are_not_added():
    manager = URLManager(
        "https://example.com"
    )

    manager.get_next_url()

    first = manager.add_url(
        "https://example.com/about"
    )

    second = manager.add_url(
        "https://example.com/about"
    )

    assert first is True
    assert second is False
    assert manager.queue_size() == 1


# ==================================================
# Domain restrictions
# ==================================================

def test_external_url_is_not_added():
    manager = URLManager(
        "https://example.com"
    )

    result = manager.add_url(
        "https://google.com"
    )

    assert result is False
    assert manager.queue_size() == 1


# ==================================================
# Page limit
# ==================================================

def test_max_pages_limit():
    manager = URLManager(
        "https://example.com",
        max_pages=3
    )

    assert manager.add_url(
        "https://example.com/page1"
    ) is True

    assert manager.add_url(
        "https://example.com/page2"
    ) is True

    assert manager.add_url(
        "https://example.com/page3"
    ) is False

    assert manager.visited_count() == 3


# ==================================================
# Add multiple links
# ==================================================

def test_add_links():
    manager = URLManager(
        "https://example.com"
    )

    manager.get_next_url()

    links = [
        "/about",
        "/contact",
        "https://google.com",
        "mailto:test@example.com",
        "/document.pdf",
    ]

    added = manager.add_links(
        "https://example.com",
        links
    )

    assert added == 2
    assert manager.queue_size() == 2


def test_add_links_does_not_add_duplicates():
    manager = URLManager(
        "https://example.com"
    )

    manager.get_next_url()

    links = [
        "/about",
        "/about",
        "/about#section",
    ]

    added = manager.add_links(
        "https://example.com",
        links
    )

    assert added == 1
    assert manager.queue_size() == 1


# ==================================================
# State helpers
# ==================================================

def test_has_pending_urls():
    manager = URLManager(
        "https://example.com"
    )

    assert manager.has_pending_urls() is True

    manager.get_next_url()

    assert manager.has_pending_urls() is False


def test_visited_count():
    manager = URLManager(
        "https://example.com"
    )

    assert manager.visited_count() == 1

    manager.add_url(
        "https://example.com/about"
    )

    assert manager.visited_count() == 2


def test_get_visited_urls_returns_copy():
    manager = URLManager(
        "https://example.com"
    )

    visited = manager.get_visited_urls()

    visited.clear()

    assert manager.visited_count() == 1