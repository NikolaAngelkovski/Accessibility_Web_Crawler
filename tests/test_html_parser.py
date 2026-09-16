from parser import HTMLParser


# ==================================================
# Basic HTML
# ==================================================

def test_parser_accepts_html():
    html = """
    <html>
        <head>
            <title>Test Page</title>
        </head>
        <body>
            <h1>Hello World</h1>
        </body>
    </html>
    """

    parser = HTMLParser(html)

    assert parser is not None


# ==================================================
# Title
# ==================================================

def test_get_title():
    html = """
    <html>
        <head>
            <title>My Website</title>
        </head>
    </html>
    """

    parser = HTMLParser(html)

    assert parser.get_title() == "My Website"


def test_missing_title():
    html = """
    <html>
        <head></head>
        <body></body>
    </html>
    """

    parser = HTMLParser(html)

    assert parser.get_title() is None


def test_title_is_trimmed():
    html = """
    <html>
        <head>
            <title>
                My Website
            </title>
        </head>
    </html>
    """

    parser = HTMLParser(html)

    assert parser.get_title() == "My Website"


# ==================================================
# Language
# ==================================================

def test_get_language():
    html = """
    <html lang="en">
        <head></head>
    </html>
    """

    parser = HTMLParser(html)

    assert parser.get_language() == "en"


def test_missing_language():
    html = """
    <html>
        <head></head>
    </html>
    """

    parser = HTMLParser(html)

    assert parser.get_language() is None


def test_empty_language():
    html = """
    <html lang="">
        <head></head>
    </html>
    """

    parser = HTMLParser(html)

    assert parser.get_language() is None


# ==================================================
# Headings
# ==================================================

def test_get_headings():
    html = """
    <html>
        <body>
            <h1>Main Heading</h1>
            <h2>Subheading</h2>
            <h3>Another Heading</h3>
        </body>
    </html>
    """

    parser = HTMLParser(html)

    headings = parser.get_headings()

    assert len(headings) == 3

    assert headings[0] == {
        "level": 1,
        "text": "Main Heading"
    }

    assert headings[1] == {
        "level": 2,
        "text": "Subheading"
    }

    assert headings[2] == {
        "level": 3,
        "text": "Another Heading"
    }


def test_no_headings():
    html = """
    <html>
        <body>
            <p>Hello</p>
        </body>
    </html>
    """

    parser = HTMLParser(html)

    assert parser.get_headings() == []


def test_heading_text_is_trimmed():
    html = """
    <h1>
        Hello
        World
    </h1>
    """

    parser = HTMLParser(html)

    headings = parser.get_headings()

    assert headings[0]["text"] == "Hello World"


# ==================================================
# Images
# ==================================================

def test_get_images():
    html = """
    <html>
        <body>
            <img
                src="cat.jpg"
                alt="A cat"
            >
            <img
                src="logo.png"
                alt="Company logo"
            >
        </body>
    </html>
    """

    parser = HTMLParser(html)

    images = parser.get_images()

    assert len(images) == 2

    assert images[0] == {
        "src": "cat.jpg",
        "alt": "A cat",
        "has_alt_attribute": True
    }

    assert images[1] == {
        "src": "logo.png",
        "alt": "Company logo",
        "has_alt_attribute": True
    }


def test_image_without_alt():
    html = """
    <img src="image.jpg">
    """

    parser = HTMLParser(html)

    images = parser.get_images()

    assert len(images) == 1

    assert images[0]["src"] == "image.jpg"
    assert images[0]["alt"] is None
    assert images[0]["has_alt_attribute"] is False


def test_decorative_image():
    html = """
    <img src="decoration.png" alt="">
    """

    parser = HTMLParser(html)

    images = parser.get_images()

    assert images[0]["alt"] == ""
    assert images[0]["has_alt_attribute"] is True


# ==================================================
# Links
# ==================================================

def test_get_links():
    html = """
    <html>
        <body>
            <a href="/about">About Us</a>
            <a href="/contact">Contact</a>
        </body>
    </html>
    """

    parser = HTMLParser(
        html,
        base_url="https://example.com"
    )

    links = parser.get_links()

    assert len(links) == 2

    assert links[0]["href"] == "/about"
    assert links[0]["url"] == (
        "https://example.com/about"
    )
    assert links[0]["text"] == "About Us"


def test_absolute_link():
    html = """
    <a href="https://google.com">
        Google
    </a>
    """

    parser = HTMLParser(
        html,
        base_url="https://example.com"
    )

    links = parser.get_links()

    assert links[0]["url"] == (
        "https://google.com"
    )


def test_relative_link():
    html = """
    <a href="contact">
        Contact
    </a>
    """

    parser = HTMLParser(
        html,
        base_url="https://example.com/about/"
    )

    links = parser.get_links()

    assert links[0]["url"] == (
        "https://example.com/about/contact"
    )


def test_empty_link():
    html = """
    <a href="">Empty</a>
    """

    parser = HTMLParser(
        html,
        base_url="https://example.com"
    )

    links = parser.get_links()

    assert links[0]["href"] == ""
    assert links[0]["url"] is None


def test_link_without_href():
    html = """
    <a>Not a real link</a>
    """

    parser = HTMLParser(
        html,
        base_url="https://example.com"
    )

    links = parser.get_links()

    assert links[0]["href"] is None
    assert links[0]["url"] is None


# ==================================================
# Forms
# ==================================================

def test_get_forms():
    html = """
    <form action="/login" method="post">
        <input
            type="text"
            name="username"
            id="username"
        >

        <input
            type="password"
            name="password"
            id="password"
        >

        <button type="submit">
            Login
        </button>
    </form>
    """

    parser = HTMLParser(html)

    forms = parser.get_forms()

    assert len(forms) == 1

    assert forms[0]["action"] == "/login"
    assert forms[0]["method"] == "post"

    assert len(forms[0]["controls"]) == 3

    assert forms[0]["controls"][0]["tag"] == "input"
    assert forms[0]["controls"][0]["name"] == "username"


def test_form_default_method():
    html = """
    <form action="/search">
        <input type="text">
    </form>
    """

    parser = HTMLParser(html)

    forms = parser.get_forms()

    assert forms[0]["method"] == "get"


def test_no_forms():
    html = """
    <html>
        <body>
            <p>No forms here.</p>
        </body>
    </html>
    """

    parser = HTMLParser(html)

    assert parser.get_forms() == []


# ==================================================
# Metadata
# ==================================================

def test_get_metadata():
    html = """
    <html>
        <head>
            <meta charset="UTF-8">

            <meta
                name="description"
                content="Test website"
            >

            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            >
        </head>
    </html>
    """

    parser = HTMLParser(html)

    metadata = parser.get_metadata()

    assert metadata["charset"] == "UTF-8"
    assert metadata["description"] == "Test website"
    assert metadata["viewport"] == (
        "width=device-width, initial-scale=1"
    )


def test_missing_metadata():
    html = """
    <html>
        <head></head>
    </html>
    """

    parser = HTMLParser(html)

    metadata = parser.get_metadata()

    assert metadata["charset"] is None
    assert metadata["description"] is None
    assert metadata["viewport"] is None


# ==================================================
# Text
# ==================================================

def test_get_text():
    html = """
    <html>
        <body>
            <h1>Hello</h1>
            <p>This is a test.</p>
        </body>
    </html>
    """

    parser = HTMLParser(html)

    text = parser.get_text()

    assert "Hello" in text
    assert "This is a test." in text


def test_script_and_style_are_removed_from_text():
    html = """
    <html>
        <head>
            <style>
                body { color: red; }
            </style>

            <script>
                console.log("test");
            </script>
        </head>

        <body>
            <p>Visible text</p>
        </body>
    </html>
    """

    parser = HTMLParser(html)

    text = parser.get_text()

    assert "Visible text" in text
    assert "color: red" not in text
    assert "console.log" not in text


# ==================================================
# Complete parse
# ==================================================

def test_parse_returns_all_information():
    html = """
    <!DOCTYPE html>

    <html lang="en">
        <head>

            <title>Test Website</title>

            <meta charset="UTF-8">

            <meta
                name="description"
                content="A test website"
            >

        </head>

        <body>

            <h1>Welcome</h1>

            <h2>About</h2>

            <img
                src="/image.jpg"
                alt="Test image"
            >

            <a href="/about">
                About
            </a>

            <form action="/submit">
                <input type="text">
            </form>

            <p>Hello world.</p>

        </body>
    </html>
    """

    parser = HTMLParser(
        html,
        base_url="https://example.com"
    )

    result = parser.parse()

    assert result["title"] == "Test Website"
    assert result["language"] == "en"

    assert len(result["headings"]) == 2
    assert len(result["images"]) == 1
    assert len(result["links"]) == 1
    assert len(result["forms"]) == 1

    assert result["metadata"]["charset"] == "UTF-8"

    assert "Hello world." in result["text"]