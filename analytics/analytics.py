class Analytics:
    """
    Calculates aggregate accessibility statistics from
    stored page results.
    """

    def __init__(self, database):
        self.database = database

    def get_overview(self):
        pages = self.database.get_pages()

        if not pages:
            return {
                "total_pages": 0,
                "average_score": 0.0,
                "highest_score": 0.0,
                "lowest_score": 0.0,
                "total_rules": 0,
                "passed": 0,
                "warnings": 0,
                "failed": 0,
                "errors": 0
            }

        scores = []
        total_rules = 0
        passed = 0
        warnings = 0
        failed = 0
        errors = 0

        for page in pages:
            summary = page.get(
                "accessibility_summary",
                {}
            )

            total_rules += summary.get(
                "total_rules",
                0
            )

            passed += summary.get(
                "passed",
                0
            )

            warnings += summary.get(
                "warnings",
                0
            )

            failed += summary.get(
                "failed",
                0
            )

            errors += summary.get(
                "errors",
                0
            )

            score = self._calculate_page_score(
                summary
            )

            if score is not None:
                scores.append(score)

        average_score = (
            sum(scores) / len(scores)
            if scores
            else 0.0
        )

        return {
            "total_pages": len(pages),
            "average_score": round(
                average_score,
                2
            ),
            "highest_score": round(
                max(scores),
                2
            ) if scores else 0.0,
            "lowest_score": round(
                min(scores),
                2
            ) if scores else 0.0,
            "total_rules": total_rules,
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
            "errors": errors
        }

    def get_rule_statistics(self):
        pages = self.database.get_pages()

        statistics = {}

        for page in pages:
            results = page.get(
                "accessibility_results",
                []
            )

            for result in results:
                rule = result.get("rule")
                status = result.get("status")

                if rule is None:
                    continue

                if rule not in statistics:
                    statistics[rule] = {
                        "rule": rule,
                        "total": 0,
                        "passed": 0,
                        "warnings": 0,
                        "failed": 0,
                        "errors": 0
                    }

                statistics[rule]["total"] += 1

                if status == "pass":
                    statistics[rule]["passed"] += 1
                elif status == "warning":
                    statistics[rule]["warnings"] += 1
                elif status == "fail":
                    statistics[rule]["failed"] += 1
                elif status == "error":
                    statistics[rule]["errors"] += 1

        return list(
            statistics.values()
        )

    def get_failed_rules(self):
        pages = self.database.get_pages()

        failed_rules = []

        for page in pages:
            results = page.get(
                "accessibility_results",
                []
            )

            for result in results:
                if result.get("status") == "fail":
                    failed_rules.append({
                        "url": page.get("url"),
                        "rule": result.get("rule"),
                        "message": result.get("message"),
                        "details": result.get("details")
                    })

        return failed_rules

    def get_page_scores(self):
        pages = self.database.get_pages()

        page_scores = []

        for page in pages:
            summary = page.get(
                "accessibility_summary",
                {}
            )

            score = self._calculate_page_score(
                summary
            )

            page_scores.append({
                "id": page.get("id"),
                "url": page.get("url"),
                "title": page.get("title"),
                "score": score
            })

        return page_scores

    @staticmethod
    def _calculate_page_score(summary):
        total_rules = summary.get(
            "total_rules",
            0
        )

        if total_rules == 0:
            return None

        passed = summary.get(
            "passed",
            0
        )

        warnings = summary.get(
            "warnings",
            0
        )

        score = (
            passed + (warnings * 0.5)
        ) / total_rules * 100

        return round(
            score,
            2
        )