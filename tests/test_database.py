from database import Database


def create_crawl_result():
    return {
        "url": "https://example.com",
        "final_url": "https://example.com/",
        "status_code": 200,
        "content_type": "text/html"
    }


def create_page_data():
    return {
        "title": "Example Page",
        "language": "en",
        "headings": [
            {
                "level": 1,
                "text": "Example"
            }
        ],
        "images": [
            {
                "src": "/image.png",
                "alt": "Example image",
                "has_alt_attribute": True
            }
        ],
        "links": [
            {
                "href": "/about",
                "url": "https://example.com/about",
                "text": "About"
            }
        ],
        "forms": []
    }


def create_evaluation():
    return {
        "results": [
            {
                "rule": "language_check",
                "status": "pass",
                "message": "Page declares a valid language.",
                "details": {
                    "language": "en"
                }
            }
        ],
        "summary": {
            "total_rules": 1,
            "passed": 1,
            "warnings": 0,
            "failed": 0,
            "errors": 0
        }
    }


def test_database_creates_database(tmp_path):
    database_path = tmp_path / "test.db"

    database = Database(database_path)

    assert database_path.exists()

    database.close()


def test_database_starts_with_no_pages(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    assert database.count_pages() == 0

    database.close()


def test_database_saves_page(
    tmp_path
):
    database = Database(
        tmp_path / "test.db"
    )

    page_id = database.save_page(
        create_crawl_result(),
        create_page_data(),
        create_evaluation()
    )

    assert page_id == 1
    assert database.count_pages() == 1

    database.close()


def test_database_get_page(
    tmp_path
):
    database = Database(
        tmp_path / "test.db"
    )

    page_id = database.save_page(
        create_crawl_result(),
        create_page_data(),
        create_evaluation()
    )

    page = database.get_page(page_id)

    assert page is not None
    assert page["id"] == page_id
    assert page["url"] == "https://example.com"
    assert page["final_url"] == "https://example.com/"
    assert page["status_code"] == 200
    assert page["content_type"] == "text/html"
    assert page["title"] == "Example Page"
    assert page["language"] == "en"

    database.close()


def test_database_stores_page_counts(
    tmp_path
):
    database = Database(
        tmp_path / "test.db"
    )

    page_id = database.save_page(
        create_crawl_result(),
        create_page_data(),
        create_evaluation()
    )

    page = database.get_page(page_id)

    assert page["headings_count"] == 1
    assert page["images_count"] == 1
    assert page["links_count"] == 1
    assert page["forms_count"] == 0

    database.close()


def test_database_stores_accessibility_results(
    tmp_path
):
    database = Database(
        tmp_path / "test.db"
    )

    page_id = database.save_page(
        create_crawl_result(),
        create_page_data(),
        create_evaluation()
    )

    page = database.get_page(page_id)

    assert len(
        page["accessibility_results"]
    ) == 1

    assert (
        page["accessibility_results"][0]["rule"]
        == "language_check"
    )

    database.close()


def test_database_stores_accessibility_summary(
    tmp_path
):
    database = Database(
        tmp_path / "test.db"
    )

    page_id = database.save_page(
        create_crawl_result(),
        create_page_data(),
        create_evaluation()
    )

    page = database.get_page(page_id)

    summary = page["accessibility_summary"]

    assert summary["total_rules"] == 1
    assert summary["passed"] == 1
    assert summary["warnings"] == 0
    assert summary["failed"] == 0
    assert summary["errors"] == 0

    database.close()


def test_database_get_pages(
    tmp_path
):
    database = Database(
        tmp_path / "test.db"
    )

    database.save_page(
        create_crawl_result(),
        create_page_data(),
        create_evaluation()
    )

    second_result = create_crawl_result()
    second_result["url"] = "https://example.com/about"

    database.save_page(
        second_result,
        create_page_data(),
        create_evaluation()
    )

    pages = database.get_pages()

    assert len(pages) == 2
    assert pages[0]["url"] == "https://example.com"
    assert (
        pages[1]["url"]
        == "https://example.com/about"
    )

    database.close()


def test_database_get_missing_page(
    tmp_path
):
    database = Database(
        tmp_path / "test.db"
    )

    page = database.get_page(999)

    assert page is None

    database.close()


def test_database_count_pages(
    tmp_path
):
    database = Database(
        tmp_path / "test.db"
    )

    assert database.count_pages() == 0

    database.save_page(
        create_crawl_result(),
        create_page_data(),
        create_evaluation()
    )

    assert database.count_pages() == 1

    database.save_page(
        create_crawl_result(),
        create_page_data(),
        create_evaluation()
    )

    assert database.count_pages() == 2

    database.close()


def test_database_validates_crawl_result(
    tmp_path
):
    database = Database(
        tmp_path / "test.db"
    )

    try:
        database.save_page(
            None,
            create_page_data(),
            create_evaluation()
        )
        assert False
    except TypeError:
        assert True

    database.close()


def test_database_validates_page_data(
    tmp_path
):
    database = Database(
        tmp_path / "test.db"
    )

    try:
        database.save_page(
            create_crawl_result(),
            None,
            create_evaluation()
        )
        assert False
    except TypeError:
        assert True

    database.close()


def test_database_validates_evaluation(
    tmp_path
):
    database = Database(
        tmp_path / "test.db"
    )

    try:
        database.save_page(
            create_crawl_result(),
            create_page_data(),
            None
        )
        assert False
    except TypeError:
        assert True

    database.close()


def test_database_context_manager(
    tmp_path
):
    database_path = tmp_path / "test.db"

    with Database(database_path) as database:
        database.save_page(
            create_crawl_result(),
            create_page_data(),
            create_evaluation()
        )

        assert database.count_pages() == 1