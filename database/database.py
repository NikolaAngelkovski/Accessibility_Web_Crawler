import json
import sqlite3
from pathlib import Path


class Database:
    """
    Handles persistent storage of crawler results using SQLite.

    Responsibilities:
    - Create the database
    - Create the pages table
    - Store crawled page information
    - Store accessibility evaluation results
    - Retrieve stored pages
    - Retrieve individual pages
    """

    def __init__(self, database_path="crawler.db"):
        self.database_path = Path(database_path)

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.connection.row_factory = sqlite3.Row

        self._create_tables()

    def _create_tables(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                final_url TEXT,
                status_code INTEGER,
                content_type TEXT,
                title TEXT,
                language TEXT,
                headings_count INTEGER NOT NULL DEFAULT 0,
                images_count INTEGER NOT NULL DEFAULT 0,
                links_count INTEGER NOT NULL DEFAULT 0,
                forms_count INTEGER NOT NULL DEFAULT 0,
                accessibility_results TEXT,
                accessibility_summary TEXT
            )
            """
        )

        self.connection.commit()

    def save_page(
        self,
        crawl_result,
        page_data,
        evaluation
    ):
        if not isinstance(crawl_result, dict):
            raise TypeError(
                "crawl_result must be a dictionary"
            )

        if not isinstance(page_data, dict):
            raise TypeError(
                "page_data must be a dictionary"
            )

        if not isinstance(evaluation, dict):
            raise TypeError(
                "evaluation must be a dictionary"
            )

        cursor = self.connection.execute(
            """
            INSERT INTO pages (
                url,
                final_url,
                status_code,
                content_type,
                title,
                language,
                headings_count,
                images_count,
                links_count,
                forms_count,
                accessibility_results,
                accessibility_summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                crawl_result.get("url"),
                crawl_result.get("final_url"),
                crawl_result.get("status_code"),
                crawl_result.get("content_type"),
                page_data.get("title"),
                page_data.get("language"),
                len(page_data.get("headings", [])),
                len(page_data.get("images", [])),
                len(page_data.get("links", [])),
                len(page_data.get("forms", [])),
                json.dumps(
                    evaluation.get("results", [])
                ),
                json.dumps(
                    evaluation.get("summary", {})
                )
            )
        )

        self.connection.commit()

        return cursor.lastrowid

    def get_page(self, page_id):
        cursor = self.connection.execute(
            """
            SELECT *
            FROM pages
            WHERE id = ?
            """,
            (page_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_dict(row)

    def get_pages(self):
        cursor = self.connection.execute(
            """
            SELECT *
            FROM pages
            ORDER BY id
            """
        )

        return [
            self._row_to_dict(row)
            for row in cursor.fetchall()
        ]

    def count_pages(self):
        cursor = self.connection.execute(
            """
            SELECT COUNT(*)
            FROM pages
            """
        )

        return cursor.fetchone()[0]

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    @staticmethod
    def _row_to_dict(row):
        page = dict(row)

        page["accessibility_results"] = json.loads(
            page["accessibility_results"]
        )

        page["accessibility_summary"] = json.loads(
            page["accessibility_summary"]
        )

        return page

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):
        self.close()