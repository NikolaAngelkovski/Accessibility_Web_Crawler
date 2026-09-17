class AccessibilityScorer:
    """
    Calculates an overall accessibility score from
    accessibility rule results.

    Scoring:
    - pass    = 100%
    - warning = 50%
    - fail    = 0%
    - error   = 0%

    The final score is expressed as a value from 0 to 100.
    """

    STATUS_SCORES = {
        "pass": 1.0,
        "warning": 0.5,
        "fail": 0.0,
        "error": 0.0,
    }

    def calculate(self, evaluation):
        if not isinstance(evaluation, dict):
            raise TypeError(
                "evaluation must be a dictionary"
            )

        results = evaluation.get("results")

        if not isinstance(results, list):
            raise ValueError(
                "evaluation must contain a results list"
            )

        if not results:
            return {
                "score": 0.0,
                "percentage": 0.0,
                "grade": "N/A",
                "total_rules": 0,
                "passed": 0,
                "warnings": 0,
                "failed": 0,
                "errors": 0
            }

        total_score = 0.0
        passed = 0
        warnings = 0
        failed = 0
        errors = 0

        for result in results:
            if not isinstance(result, dict):
                raise ValueError(
                    "Each accessibility result must be a dictionary"
                )

            status = result.get("status")

            if status not in self.STATUS_SCORES:
                raise ValueError(
                    f"Invalid accessibility status: {status}"
                )

            total_score += self.STATUS_SCORES[status]

            if status == "pass":
                passed += 1
            elif status == "warning":
                warnings += 1
            elif status == "fail":
                failed += 1
            elif status == "error":
                errors += 1

        total_rules = len(results)

        percentage = (
            total_score / total_rules
        ) * 100

        percentage = round(
            percentage,
            2
        )

        return {
            "score": percentage,
            "percentage": percentage,
            "grade": self._get_grade(percentage),
            "total_rules": total_rules,
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
            "errors": errors
        }

    @staticmethod
    def _get_grade(score):
        if score >= 90:
            return "A"

        if score >= 80:
            return "B"

        if score >= 70:
            return "C"

        if score >= 60:
            return "D"

        return "F"