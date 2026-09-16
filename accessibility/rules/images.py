def image_check(page_data):
    """
    Check whether images contain alternative text information.

    The rule checks:

    - Whether image data is available.
    - Whether each image has an alt attribute.
    - Whether images with alt="" are present.
    - Whether images contain meaningful alternative text.

    An empty alt attribute is not considered an automatic failure
    because it can be appropriate for decorative images.

    Args:
        page_data (dict): Parsed page data produced by HTMLParser.

    Returns:
        dict: Standardized accessibility rule result.
    """

    images = page_data.get("images")

    # The parser normally returns a list.
    if not isinstance(images, list):
        return {
            "rule": "image_check",
            "status": "error",
            "message": (
                "Image information could not be evaluated."
            ),
            "details": None
        }

    # A page without images has nothing to evaluate.
    if not images:
        return {
            "rule": "image_check",
            "status": "pass",
            "message": (
                "Page does not contain any images."
            ),
            "details": {
                "total_images": 0,
                "images_with_alt": 0,
                "images_with_empty_alt": 0,
                "images_without_alt": 0
            }
        }

    images_with_alt = []
    images_with_empty_alt = []
    images_without_alt = []

    for index, image in enumerate(images):

        if not isinstance(image, dict):
            return {
                "rule": "image_check",
                "status": "error",
                "message": (
                    "Invalid image data was provided."
                ),
                "details": {
                    "index": index
                }
            }

        has_alt_attribute = image.get(
            "has_alt_attribute"
        )

        alt = image.get("alt")

        # Missing alt attribute.
        if not has_alt_attribute:
            images_without_alt.append({
                "index": index,
                "src": image.get("src")
            })

            continue

        # alt="" is valid for decorative images.
        if alt is None or not str(alt).strip():
            images_with_empty_alt.append({
                "index": index,
                "src": image.get("src")
            })

            continue

        # Image has non-empty alternative text.
        images_with_alt.append({
            "index": index,
            "src": image.get("src"),
            "alt": str(alt).strip()
        })

    details = {
        "total_images": len(images),
        "images_with_alt": len(images_with_alt),
        "images_with_empty_alt": len(images_with_empty_alt),
        "images_without_alt": len(images_without_alt),
        "images_with_alt_details": images_with_alt,
        "images_with_empty_alt_details": images_with_empty_alt,
        "images_without_alt_details": images_without_alt
    }

    # Missing alt attributes are an accessibility failure.
    if images_without_alt:
        return {
            "rule": "image_check",
            "status": "fail",
            "message": (
                "One or more images do not have an alt attribute."
            ),
            "details": details
        }

    # Empty alt attributes are allowed, but report them so
    # the user knows that decorative images were encountered.
    if images_with_empty_alt:
        return {
            "rule": "image_check",
            "status": "warning",
            "message": (
                "All images have alt attributes, but some "
                "use empty alt text."
            ),
            "details": details
        }

    return {
        "rule": "image_check",
        "status": "pass",
        "message": (
            "All images have non-empty alternative text."
        ),
        "details": details
    }