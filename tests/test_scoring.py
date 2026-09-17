import pytest

from accessibility import AccessibilityScorer


def create_evaluation(statuses):
    return {
        "results": [
            {
                "rule": f"rule_{index}",
                "status": status,
                "message": "",
                "details": None
            }
            for index, status in enumerate(statuses)
        ]
    }


def test_scorer_returns_100_for_all_passes():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "pass",
        "pass",
        "pass"
    ])

    result = scorer.calculate(evaluation)

    assert result["score"] == 100.0
    assert result["percentage"] == 100.0
    assert result["grade"] == "A"


def test_scorer_returns_50_for_all_warnings():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "warning",
        "warning"
    ])

    result = scorer.calculate(evaluation)

    assert result["score"] == 50.0
    assert result["percentage"] == 50.0
    assert result["grade"] == "F"


def test_scorer_returns_zero_for_all_failures():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "fail",
        "fail"
    ])

    result = scorer.calculate(evaluation)

    assert result["score"] == 0.0
    assert result["percentage"] == 0.0
    assert result["grade"] == "F"


def test_scorer_counts_warnings_as_half():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "pass",
        "warning"
    ])

    result = scorer.calculate(evaluation)

    assert result["score"] == 75.0


def test_scorer_handles_mixed_results():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "pass",
        "pass",
        "warning",
        "fail"
    ])

    result = scorer.calculate(evaluation)

    assert result["score"] == 62.5
    assert result["total_rules"] == 4
    assert result["passed"] == 2
    assert result["warnings"] == 1
    assert result["failed"] == 1
    assert result["errors"] == 0


def test_scorer_treats_errors_as_zero():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "pass",
        "error"
    ])

    result = scorer.calculate(evaluation)

    assert result["score"] == 50.0
    assert result["errors"] == 1


def test_scorer_handles_empty_results():
    scorer = AccessibilityScorer()

    evaluation = {
        "results": []
    }

    result = scorer.calculate(evaluation)

    assert result["score"] == 0.0
    assert result["percentage"] == 0.0
    assert result["grade"] == "N/A"
    assert result["total_rules"] == 0


def test_scorer_grade_a():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "pass",
        "pass",
        "pass",
        "pass",
        "warning"
    ])

    result = scorer.calculate(evaluation)

    assert result["score"] == 90.0
    assert result["grade"] == "A"


def test_scorer_grade_b():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "pass",
        "pass",
        "pass",
        "warning"
    ])

    result = scorer.calculate(evaluation)

    assert result["score"] == 87.5
    assert result["grade"] == "B"


def test_scorer_grade_c():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "pass",
        "pass",
        "warning",
        "warning"
    ])

    result = scorer.calculate(evaluation)

    assert result["score"] == 75.0
    assert result["grade"] == "C"


def test_scorer_grade_d():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "pass",
        "pass",
        "pass",
        "fail",
        "fail"
    ])

    result = scorer.calculate(evaluation)

    assert result["score"] == 60.0
    assert result["grade"] == "D"


def test_scorer_grade_f():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "pass",
        "warning",
        "fail",
        "fail"
    ])

    result = scorer.calculate(evaluation)

    assert result["score"] == 37.5
    assert result["grade"] == "F"


def test_scorer_validates_evaluation():
    scorer = AccessibilityScorer()

    with pytest.raises(TypeError):
        scorer.calculate(None)


def test_scorer_requires_results():
    scorer = AccessibilityScorer()

    with pytest.raises(ValueError):
        scorer.calculate({})


def test_scorer_validates_result_data():
    scorer = AccessibilityScorer()

    evaluation = {
        "results": [
            "invalid result"
        ]
    }

    with pytest.raises(ValueError):
        scorer.calculate(evaluation)


def test_scorer_validates_status():
    scorer = AccessibilityScorer()

    evaluation = {
        "results": [
            {
                "rule": "test",
                "status": "invalid",
                "message": "",
                "details": None
            }
        ]
    }

    with pytest.raises(ValueError):
        scorer.calculate(evaluation)


def test_scorer_returns_standard_structure():
    scorer = AccessibilityScorer()

    evaluation = create_evaluation([
        "pass"
    ])

    result = scorer.calculate(evaluation)

    assert set(result.keys()) == {
        "score",
        "percentage",
        "grade",
        "total_rules",
        "passed",
        "warnings",
        "failed",
        "errors"
    }