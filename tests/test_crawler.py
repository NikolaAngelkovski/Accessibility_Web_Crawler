from unittest.mock import Mock, patch

from crawler import Crawler


# -----------------------------------
# URL validation tests
# -----------------------------------

def test_valid_http_url():
    crawler = Crawler()

    assert crawler.is_valid_url(
        "http://example.com"
    ) is True


def test_valid_https_url():
    crawler = Crawler()

    assert crawler.is_valid_url(
        "https://example.com"
    ) is True


def test_invalid_url():
    crawler = Crawler()

    assert crawler.is_valid_url(
        "not-a-url"
    ) is False


def test_empty_url():
    crawler = Crawler()

    assert crawler.is_valid_url(
        ""
    ) is False


def test_unsupported_protocol():
    crawler = Crawler()

    assert crawler.is_valid_url(
        "ftp://example.com"
    ) is False


# -----------------------------------
# Successful fetch
# -----------------------------------

@patch("crawler.crawler.requests.get")
def test_fetch_success(mock_get):
    mock_response = Mock()

    mock_response.status_code = 200
    mock_response.url = "https://example.com/"
    mock_response.text = "<html><body>Hello</body></html>"

    mock_response.headers = {
        "Content-Type": "text/html"
    }

    mock_get.return_value = mock_response

    crawler = Crawler()

    result = crawler.fetch(
        "https://example.com"
    )

    assert result["success"] is True
    assert result["status_code"] == 200
    assert result["content_type"] == "text/html"
    assert result["html"] == (
        "<html><body>Hello</body></html>"
    )


# -----------------------------------
# HTTP error
# -----------------------------------

@patch("crawler.crawler.requests.get")
def test_fetch_http_error(mock_get):
    mock_response = Mock()

    mock_response.status_code = 404
    mock_response.url = "https://example.com/missing"

    mock_response.headers = {
        "Content-Type": "text/html"
    }

    mock_get.return_value = mock_response

    crawler = Crawler()

    result = crawler.fetch(
        "https://example.com/missing"
    )

    assert result["success"] is False
    assert result["status_code"] == 404
    assert result["error"] == "HTTP 404"


# -----------------------------------
# Non-HTML response
# -----------------------------------

@patch("crawler.crawler.requests.get")
def test_fetch_non_html(mock_get):
    mock_response = Mock()

    mock_response.status_code = 200
    mock_response.url = "https://example.com/file.pdf"

    mock_response.headers = {
        "Content-Type": "application/pdf"
    }

    mock_get.return_value = mock_response

    crawler = Crawler()

    result = crawler.fetch(
        "https://example.com/file.pdf"
    )

    assert result["success"] is False
    assert result["error"] == "Response is not HTML"


# -----------------------------------
# Timeout
# -----------------------------------

@patch("crawler.crawler.requests.get")
def test_fetch_timeout(mock_get):
    from requests.exceptions import Timeout

    mock_get.side_effect = Timeout()

    crawler = Crawler()

    result = crawler.fetch(
        "https://example.com"
    )

    assert result["success"] is False
    assert result["error"] == "Request timed out"


# -----------------------------------
# Connection error
# -----------------------------------

@patch("crawler.crawler.requests.get")
def test_fetch_connection_error(mock_get):
    from requests.exceptions import ConnectionError

    mock_get.side_effect = ConnectionError()

    crawler = Crawler()

    result = crawler.fetch(
        "https://example.com"
    )

    assert result["success"] is False
    assert result["error"] == "Connection error"


# -----------------------------------
# Invalid URL should not make request
# -----------------------------------

@patch("crawler.crawler.requests.get")
def test_invalid_url_does_not_make_request(mock_get):
    crawler = Crawler()

    result = crawler.fetch(
        "this-is-not-a-url"
    )

    assert result["success"] is False
    assert result["error"] == "Invalid URL"

    mock_get.assert_not_called()


# -----------------------------------
# Redirect handling
# -----------------------------------

@patch("crawler.crawler.requests.get")
def test_redirect(mock_get):
    mock_response = Mock()

    mock_response.status_code = 200
    mock_response.url = "https://example.com/final"
    mock_response.text = "<html></html>"

    mock_response.headers = {
        "Content-Type": "text/html"
    }

    mock_get.return_value = mock_response

    crawler = Crawler()

    result = crawler.fetch(
        "https://example.com/start"
    )

    assert result["success"] is True
    assert result["final_url"] == (
        "https://example.com/final"
    )