import logging


logger = logging.getLogger(__name__)


class AccessibilityEvaluator:
    """
    Main accessibility evaluation engine.

    The evaluator receives structured page information from
    the HTML parser and runs registered accessibility rules.

    Individual rules are intentionally kept separate from
    this class so they can be added independently in future
    features.
    """

    def __init__(self):
        """
        Initialize the accessibility evaluator.
        """

        self.rules = []

    # --------------------------------------------------
    # Rule registration
    # --------------------------------------------------

    def register_rule(self, rule):
        """
        Register an accessibility rule.

        A rule must be a callable that accepts the parsed
        page data and returns a result dictionary.

        Args:
            rule (callable): Accessibility rule.

        Raises:
            TypeError: If rule is not callable.
        """

        if not callable(rule):
            raise TypeError(
                "Accessibility rule must be callable"
            )

        self.rules.append(rule)

        logger.info(
            "Registered accessibility rule: %s",
            self._get_rule_name(rule)
        )

    # --------------------------------------------------
    # Rule removal
    # --------------------------------------------------

    def unregister_rule(self, rule):
        """
        Remove a registered accessibility rule.

        Args:
            rule (callable): Rule to remove.

        Returns:
            bool: True if removed, False if it wasn't
                  registered.
        """

        if rule not in self.rules:
            return False

        self.rules.remove(rule)

        logger.info(
            "Unregistered accessibility rule: %s",
            self._get_rule_name(rule)
        )

        return True

    # --------------------------------------------------
    # Rule information
    # --------------------------------------------------

    def get_rules(self):
        """
        Return the currently registered rules.

        Returns:
            list: Copy of the registered rules.
        """

        return self.rules.copy()

    # --------------------------------------------------
    # Evaluation
    # --------------------------------------------------

    def evaluate(self, page_data):
        """
        Evaluate a parsed webpage.

        Args:
            page_data (dict): Structured data produced by
                              HTMLParser.parse().

        Returns:
            dict: Evaluation results.
        """

        if not isinstance(page_data, dict):
            raise TypeError(
                "page_data must be a dictionary"
            )

        logger.info(
            "Starting accessibility evaluation"
        )

        results = []

        for rule in self.rules:
            rule_name = self._get_rule_name(rule)

            try:
                result = rule(page_data)

                validated_result = self._validate_result(
                    result,
                    rule_name
                )

                results.append(validated_result)

            except Exception as error:
                logger.exception(
                    "Accessibility rule failed: %s",
                    rule_name
                )

                results.append({
                    "rule": rule_name,
                    "status": "error",
                    "message": (
                        "Rule could not be evaluated"
                    ),
                    "details": str(error)
                })

        summary = self._create_summary(results)

        logger.info(
            "Accessibility evaluation finished"
        )

        return {
            "results": results,
            "summary": summary
        }

    # --------------------------------------------------
    # Rule result validation
    # --------------------------------------------------

    @staticmethod
    def _validate_result(result, rule_name):
        """
        Validate and normalize a rule result.

        Supported statuses:

        - pass
        - warning
        - fail
        - error

        Args:
            result (dict): Result returned by a rule.
            rule_name (str): Name of the rule.

        Returns:
            dict: Normalized rule result.
        """

        if not isinstance(result, dict):
            raise ValueError(
                f"Rule '{rule_name}' must return a dictionary"
            )

        status = result.get("status")

        valid_statuses = {
            "pass",
            "warning",
            "fail",
            "error"
        }

        if status not in valid_statuses:
            raise ValueError(
                f"Rule '{rule_name}' returned invalid "
                f"status: {status}"
            )

        normalized = {
            "rule": result.get(
                "rule",
                rule_name
            ),
            "status": status,
            "message": result.get(
                "message",
                ""
            ),
            "details": result.get(
                "details",
                None
            )
        }

        return normalized

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    @staticmethod
    def _create_summary(results):
        """
        Create a summary of accessibility results.

        Args:
            results (list): Individual rule results.

        Returns:
            dict: Summary statistics.
        """

        summary = {
            "total_rules": len(results),
            "passed": 0,
            "warnings": 0,
            "failed": 0,
            "errors": 0
        }

        for result in results:
            status = result["status"]

            if status == "pass":
                summary["passed"] += 1

            elif status == "warning":
                summary["warnings"] += 1

            elif status == "fail":
                summary["failed"] += 1

            elif status == "error":
                summary["errors"] += 1

        return summary

    # --------------------------------------------------
    # Rule name
    # --------------------------------------------------

    @staticmethod
    def _get_rule_name(rule):
        """
        Get a readable name for a rule.

        Args:
            rule (callable): Rule function.

        Returns:
            str: Rule name.
        """

        return getattr(
            rule,
            "__name__",
            rule.__class__.__name__
        )