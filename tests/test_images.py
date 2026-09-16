from accessibility.rules import image_check


def test_image_check_passes_when_all_images_have_alt():
    page_data = {
        "images": [
            {
                "src": "logo.png",
                "alt": "FINKI logo",
                "has_alt_attribute": True
            },
            {
                "src": "building.jpg",
                "alt": "FINKI faculty building",
                "has_alt_attribute": True
            }
        ]
    }

    result = image_check(page_data)

    assert result["rule"] == "image_check"
    assert result["status"] == "pass"
    assert result["details"]["total_images"] == 2
    assert result["details"]["images_with_alt"] == 2
    assert result["details"]["images_without_alt"] == 0


def test_image_check_fails_when_alt_attribute_is_missing():
    page_data = {
        "images": [
            {
                "src": "logo.png",
                "alt": None,
                "has_alt_attribute": False
            }
        ]
    }

    result = image_check(page_data)

    assert result["rule"] == "image_check"
    assert result["status"] == "fail"
    assert result["details"]["images_without_alt"] == 1


def test_image_check_fails_when_one_image_is_missing_alt():
    page_data = {
        "images": [
            {
                "src": "logo.png",
                "alt": "FINKI logo",
                "has_alt_attribute": True
            },
            {
                "src": "building.jpg",
                "alt": None,
                "has_alt_attribute": False
            }
        ]
    }

    result = image_check(page_data)

    assert result["status"] == "fail"
    assert result["details"]["total_images"] == 2
    assert result["details"]["images_with_alt"] == 1
    assert result["details"]["images_without_alt"] == 1


def test_image_check_warns_for_empty_alt():
    page_data = {
        "images": [
            {
                "src": "decoration.png",
                "alt": "",
                "has_alt_attribute": True
            }
        ]
    }

    result = image_check(page_data)

    assert result["rule"] == "image_check"
    assert result["status"] == "warning"
    assert result["details"]["images_with_empty_alt"] == 1


def test_image_check_warns_for_whitespace_alt():
    page_data = {
        "images": [
            {
                "src": "decoration.png",
                "alt": "   ",
                "has_alt_attribute": True
            }
        ]
    }

    result = image_check(page_data)

    assert result["status"] == "warning"
    assert result["details"]["images_with_empty_alt"] == 1


def test_image_check_handles_multiple_empty_alt_images():
    page_data = {
        "images": [
            {
                "src": "decoration1.png",
                "alt": "",
                "has_alt_attribute": True
            },
            {
                "src": "decoration2.png",
                "alt": "",
                "has_alt_attribute": True
            }
        ]
    }

    result = image_check(page_data)

    assert result["status"] == "warning"
    assert result["details"]["images_with_empty_alt"] == 2


def test_image_check_passes_when_page_has_no_images():
    page_data = {
        "images": []
    }

    result = image_check(page_data)

    assert result["status"] == "pass"
    assert result["details"]["total_images"] == 0


def test_image_check_handles_missing_image_data():
    page_data = {}

    result = image_check(page_data)

    assert result["status"] == "error"


def test_image_check_handles_invalid_image_data():
    page_data = {
        "images": [
            "invalid image"
        ]
    }

    result = image_check(page_data)

    assert result["status"] == "error"


def test_image_check_records_image_details():
    page_data = {
        "images": [
            {
                "src": "logo.png",
                "alt": "FINKI logo",
                "has_alt_attribute": True
            }
        ]
    }

    result = image_check(page_data)

    assert (
        result["details"]["images_with_alt_details"][0]["src"]
        == "logo.png"
    )

    assert (
        result["details"]["images_with_alt_details"][0]["alt"]
        == "FINKI logo"
    )


def test_image_check_returns_standard_result_structure():
    page_data = {
        "images": [
            {
                "src": "logo.png",
                "alt": "FINKI logo",
                "has_alt_attribute": True
            }
        ]
    }

    result = image_check(page_data)

    assert set(result.keys()) == {
        "rule",
        "status",
        "message",
        "details"
    }