from analytics import Analytics
from storage import Database


def create_crawl_result(url):
    return {
        "url": url,
        "final_url": url,
        "status_code": 200,
        "content_type": "text/html"
    }


def create_page_data(title):
    return {
        "title": title,
        "language": "en",
        "headings": [],
        "images": [],
        "links": [],
        "forms": []
    }


def create_evaluation(
    results,
    passed,
    warnings,
    failed,
    errors
):
    return {
        "results": results,
        "summary": {
            "total_rules": (
                passed
                + warnings
                + failed
                + errors
            ),
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
            "errors": errors
        }
    }


def save_page(
    database,
    url,
    title,
    results,
    passed,
    warnings,
    failed,
    errors
):
    database.save_page(
        create_crawl_result(url),
        create_page_data(title),
        create_evaluation(
            results,
            passed,
            warnings,
            failed,
            errors
        )
    )


def test_analytics_empty_database(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    analytics = Analytics(database)

    result = analytics.get_overview()

    assert result["total_pages"] == 0
    assert result["average_score"] == 0.0
    assert result["highest_score"] == 0.0
    assert result["lowest_score"] == 0.0
    assert result["total_rules"] == 0

    database.close()


def test_analytics_overview(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    save_page(
        database,
        "https://example.com",
        "Example",
        [
            {
                "rule": "language_check",
                "status": "pass",
                "message": "",
                "details": None
            },
            {
                "rule": "title_check",
                "status": "pass",
                "message": "",
                "details": None
            }
        ],
        2,
        0,
        0,
        0
    )

    analytics = Analytics(database)

    result = analytics.get_overview()

    assert result["total_pages"] == 1
    assert result["average_score"] == 100.0
    assert result["highest_score"] == 100.0
    assert result["lowest_score"] == 100.0
    assert result["total_rules"] == 2
    assert result["passed"] == 2

    database.close()


def test_analytics_average_score(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    save_page(
        database,
        "https://example.com/one",
        "One",
        [
            {
                "rule": "test",
                "status": "pass",
                "message": "",
                "details": None
            },
            {
                "rule": "test2",
                "status": "pass",
                "message": "",
                "details": None
            }
        ],
        2,
        0,
        0,
        0
    )

    save_page(
        database,
        "https://example.com/two",
        "Two",
        [
            {
                "rule": "test",
                "status": "fail",
                "message": "",
                "details": None
            },
            {
                "rule": "test2",
                "status": "fail",
                "message": "",
                "details": None
            }
        ],
        0,
        0,
        2,
        0
    )

    analytics = Analytics(database)

    result = analytics.get_overview()

    assert result["average_score"] == 50.0
    assert result["highest_score"] == 100.0
    assert result["lowest_score"] == 0.0

    database.close()


def test_analytics_counts_all_statuses(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    save_page(
        database,
        "https://example.com",
        "Example",
        [
            {
                "rule": "rule1",
                "status": "pass",
                "message": "",
                "details": None
            },
            {
                "rule": "rule2",
                "status": "warning",
                "message": "",
                "details": None
            },
            {
                "rule": "rule3",
                "status": "fail",
                "message": "",
                "details": None
            },
            {
                "rule": "rule4",
                "status": "error",
                "message": "",
                "details": None
            }
        ],
        1,
        1,
        1,
        1
    )

    analytics = Analytics(database)

    result = analytics.get_overview()

    assert result["passed"] == 1
    assert result["warnings"] == 1
    assert result["failed"] == 1
    assert result["errors"] == 1
    assert result["total_rules"] == 4

    database.close()


def test_analytics_rule_statistics(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    save_page(
        database,
        "https://example.com/one",
        "One",
        [
            {
                "rule": "title_check",
                "status": "pass",
                "message": "",
                "details": None
            },
            {
                "rule": "image_check",
                "status": "fail",
                "message": "",
                "details": None
            }
        ],
        1,
        0,
        1,
        0
    )

    save_page(
        database,
        "https://example.com/two",
        "Two",
        [
            {
                "rule": "title_check",
                "status": "warning",
                "message": "",
                "details": None
            },
            {
                "rule": "image_check",
                "status": "fail",
                "message": "",
                "details": None
            }
        ],
        0,
        1,
        1,
        0
    )

    analytics = Analytics(database)

    result = analytics.get_rule_statistics()

    statistics = {
        item["rule"]: item
        for item in result
    }

    assert statistics["title_check"]["total"] == 2
    assert statistics["title_check"]["passed"] == 1
    assert statistics["title_check"]["warnings"] == 1

    assert statistics["image_check"]["total"] == 2
    assert statistics["image_check"]["failed"] == 2

    database.close()


def test_analytics_failed_rules(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    save_page(
        database,
        "https://example.com",
        "Example",
        [
            {
                "rule": "image_check",
                "status": "fail",
                "message": "Missing alt text.",
                "details": {
                    "images_without_alt": 2
                }
            }
        ],
        0,
        0,
        1,
        0
    )

    analytics = Analytics(database)

    result = analytics.get_failed_rules()

    assert len(result) == 1
    assert result[0]["url"] == "https://example.com"
    assert result[0]["rule"] == "image_check"
    assert result[0]["message"] == "Missing alt text."

    database.close()


def test_analytics_page_scores(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    save_page(
        database,
        "https://example.com",
        "Example",
        [
            {
                "rule": "rule1",
                "status": "pass",
                "message": "",
                "details": None
            },
            {
                "rule": "rule2",
                "status": "warning",
                "message": "",
                "details": None
            }
        ],
        1,
        1,
        0,
        0
    )

    analytics = Analytics(database)

    result = analytics.get_page_scores()

    assert len(result) == 1
    assert result[0]["url"] == "https://example.com"
    assert result[0]["title"] == "Example"
    assert result[0]["score"] == 75.0

    database.close()


def test_analytics_handles_page_without_rules(tmp_path):
    database = Database(
        tmp_path / "test.db"
    )

    save_page(
        database,
        "https://example.com",
        "Example",
        [],
        0,
        0,
        0,
        0
    )

    analytics = Analytics(database)

    result = analytics.get_page_scores()

    assert len(result) == 1
    assert result[0]["score"] is None

    overview = analytics.get_overview()

    assert overview["total_pages"] == 1
    assert overview["average_score"] == 0.0

    database.close()