import streamlit as st
import pandas as pd

from database import Database
from analytics import Analytics


DATABASE_PATH = "crawler.db"


st.set_page_config(
    page_title="Web Accessibility Crawler",
    page_icon="🌐",
    layout="wide"
)


def load_data():
    database = Database(
        DATABASE_PATH
    )

    analytics = Analytics(
        database
    )

    overview = analytics.get_overview()
    rule_statistics = analytics.get_rule_statistics()
    page_scores = analytics.get_page_scores()
    failed_rules = analytics.get_failed_rules()

    database.close()

    return (
        overview,
        rule_statistics,
        page_scores,
        failed_rules
    )


def main():
    st.title(
        "Web Accessibility Crawler"
    )

    st.write(
        "Accessibility analysis dashboard "
        "for crawled web pages."
    )

    try:
        (
            overview,
            rule_statistics,
            page_scores,
            failed_rules
        ) = load_data()

    except Exception as error:
        st.error(
            f"Unable to load database: {error}"
        )
        return

    if overview["total_pages"] == 0:
        st.warning(
            "No crawled pages are available. "
            "Run the crawler first with "
            "`python3 main.py`."
        )
        return

    st.header(
        "Overview"
    )

    column1, column2, column3, column4 = st.columns(4)

    with column1:
        st.metric(
            "Total Pages",
            overview["total_pages"]
        )

    with column2:
        st.metric(
            "Average Score",
            f"{overview['average_score']}/100"
        )

    with column3:
        st.metric(
            "Highest Score",
            f"{overview['highest_score']}/100"
        )

    with column4:
        st.metric(
            "Lowest Score",
            f"{overview['lowest_score']}/100"
        )

    st.divider()

    st.header(
        "Accessibility Results"
    )

    column1, column2, column3, column4 = st.columns(4)

    with column1:
        st.metric(
            "Passed",
            overview["passed"]
        )

    with column2:
        st.metric(
            "Warnings",
            overview["warnings"]
        )

    with column3:
        st.metric(
            "Failed",
            overview["failed"]
        )

    with column4:
        st.metric(
            "Errors",
            overview["errors"]
        )

    st.divider()

    st.header(
        "Rule Statistics"
    )

    if rule_statistics:
        rule_dataframe = pd.DataFrame(
            rule_statistics
        )

        st.dataframe(
            rule_dataframe,
            width="stretch",
            hide_index=True
        )

        chart_data = rule_dataframe[
            [
                "rule",
                "passed",
                "warnings",
                "failed",
                "errors"
            ]
        ].set_index("rule")

        st.bar_chart(
            chart_data
        )

    else:
        st.info(
            "No rule statistics are available."
        )

    st.divider()

    st.header(
        "Page Scores"
    )

    if page_scores:
        page_dataframe = pd.DataFrame(
            page_scores
        )

        st.dataframe(
            page_dataframe,
            width="stretch",
            hide_index=True
        )

        chart_data = page_dataframe[
            [
                "url",
                "score"
            ]
        ].set_index("url")

        st.bar_chart(
            chart_data
        )

    else:
        st.info(
            "No page scores are available."
        )

    st.divider()

    st.header(
        "Failed Accessibility Checks"
    )

    if failed_rules:
        failed_dataframe = pd.DataFrame(
            failed_rules
        )

        st.dataframe(
            failed_dataframe,
            width="stretch",
            hide_index=True
        )

    else:
        st.success(
            "No failed accessibility checks were found."
        )


if __name__ == "__main__":
    main()