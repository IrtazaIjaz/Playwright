def assert_text_contains(actual: str, expected: str, msg: str = ""):
    assert expected.lower() in actual.lower(), msg or f"Expected '{expected}' in '{actual}'"
