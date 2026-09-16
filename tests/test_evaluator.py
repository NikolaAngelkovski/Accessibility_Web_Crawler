import pytest

from accessibility import AccessibilityEvaluator


# ==================================================
# Example rules used for testing
# ==================================================

def passing_rule(page_data):
    return {
        "rule": "passing_rule",
        "status": "pass",
        "message": "The page passed.",
        "details": None
    }


def warning_rule(page_data):
    return {
        "rule": "warning_rule",
        "status": "warning",
        "message": "The page has a warning.",
        "details": {
            "reason": "Example warning"
        }
    }


def failing_rule(page_data):
    return {
        "rule": "failing_rule",
        "status": "fail",
        "message": "The page failed.",
        "details": {
            "reason": "Example failure"
        }
    }


def error_rule(page_data):
    raise RuntimeError("Test error")


def invalid_status_rule(page_data):
    return {
        "rule": "invalid_rule",
        "status": "invalid",
        "message": "Invalid result."
    }


def non_dictionary_rule(page_data):
    return "invalid result"


# ==================================================
# Initialization
# ==================================================

def test_evaluator_initialization():
    evaluator = AccessibilityEvaluator()

    assert evaluator.get_rules() == []


# ==================================================
# Rule registration
# ==================================================

def test_register_rule():
    evaluator = AccessibilityEvaluator()

    evaluator.register_rule(
        passing_rule
    )

    assert len(evaluator.get_rules()) == 1
    assert evaluator.get_rules()[0] == passing_rule


def test_register_multiple_rules():
    evaluator = AccessibilityEvaluator()

    evaluator.register_rule(
        passing_rule
    )

    evaluator.register_rule(
        warning_rule
    )

    assert len(evaluator.get_rules()) == 2


def test_register_invalid_rule():
    evaluator = AccessibilityEvaluator()

    with pytest.raises(TypeError):
        evaluator.register_rule(
            "not a function"
        )


# ==================================================
# Rule removal
# ==================================================

def test_unregister_rule():
    evaluator = AccessibilityEvaluator()

    evaluator.register_rule(
        passing_rule
    )

    result = evaluator.unregister_rule(
        passing_rule
    )

    assert result is True
    assert evaluator.get_rules() == []


def test_unregister_missing_rule():
    evaluator = AccessibilityEvaluator()

    result = evaluator.unregister_rule(
        passing_rule
    )

    assert result is False


# ==================================================
# Evaluation
# ==================================================

def test_evaluate_passing_rule():
    evaluator = AccessibilityEvaluator()

    evaluator.register_rule(
        passing_rule
    )

    page_data = {
        "title": "Test page",
        "language": "en"
    }

    result = evaluator.evaluate(
        page_data
    )

    assert result["summary"]["total_rules"] == 1
    assert result["summary"]["passed"] == 1
    assert result["summary"]["warnings"] == 0
    assert result["summary"]["failed"] == 0
    assert result["summary"]["errors"] == 0


def test_evaluate_warning_rule():
    evaluator = AccessibilityEvaluator()

    evaluator.register_rule(
        warning_rule
    )

    result = evaluator.evaluate({})

    assert result["summary"]["warnings"] == 1


def test_evaluate_failing_rule():
    evaluator = AccessibilityEvaluator()

    evaluator.register_rule(
        failing_rule
    )

    result = evaluator.evaluate({})

    assert result["summary"]["failed"] == 1


def test_evaluate_multiple_rules():
    evaluator = AccessibilityEvaluator()

    evaluator.register_rule(
        passing_rule
    )

    evaluator.register_rule(
        warning_rule
    )

    evaluator.register_rule(
        failing_rule
    )

    result = evaluator.evaluate({})

    summary = result["summary"]

    assert summary["total_rules"] == 3
    assert summary["passed"] == 1
    assert summary["warnings"] == 1
    assert summary["failed"] == 1
    assert summary["errors"] == 0


# ==================================================
# Error handling
# ==================================================

def test_rule_exception_becomes_error():
    evaluator = AccessibilityEvaluator()

    evaluator.register_rule(
        error_rule
    )

    result = evaluator.evaluate({})

    assert result["summary"]["errors"] == 1

    assert result["results"][0]["rule"] == (
        "error_rule"
    )

    assert result["results"][0]["status"] == (
        "error"
    )


def test_invalid_rule_result_becomes_error():
    evaluator = AccessibilityEvaluator()

    evaluator.register_rule(
        invalid_status_rule
    )

    result = evaluator.evaluate({})

    assert result["summary"]["errors"] == 1


def test_non_dictionary_result_becomes_error():
    evaluator = AccessibilityEvaluator()

    evaluator.register_rule(
        non_dictionary_rule
    )

    result = evaluator.evaluate({})

    assert result["summary"]["errors"] == 1


# ==================================================
# Input validation
# ==================================================

def test_evaluate_requires_dictionary():
    evaluator = AccessibilityEvaluator()

    with pytest.raises(TypeError):
        evaluator.evaluate(
            "not a dictionary"
        )


# ==================================================
# Result structure
# ==================================================

def test_result_structure():
    evaluator = AccessibilityEvaluator()

    evaluator.register_rule(
        passing_rule
    )

    result = evaluator.evaluate({})

    assert "results" in result
    assert "summary" in result

    assert len(result["results"]) == 1

    rule_result = result["results"][0]

    assert "rule" in rule_result
    assert "status" in rule_result
    assert "message" in rule_result
    assert "details" in rule_result


# ==================================================
# Empty evaluator
# ==================================================

def test_empty_evaluator():
    evaluator = AccessibilityEvaluator()

    result = evaluator.evaluate({})

    assert result["results"] == []

    assert result["summary"] == {
        "total_rules": 0,
        "passed": 0,
        "warnings": 0,
        "failed": 0,
        "errors": 0
    }