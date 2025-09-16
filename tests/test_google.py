from pages.google_page import GooglePage
import pytest

def test_google_search(page):
    google = GooglePage(page)
    google.goto()

    # Handle Google consent popup if it appears
    try:
        consent_button = page.locator("button:has-text('I agree'), button:has-text('Accept all')")
        if consent_button.is_visible(timeout=3000):
            consent_button.click()
    except Exception:
        # No consent popup, continue
        pass

    # Perform search
    google.search("Playwright Python")

    # Assert title contains Playwright
    page.wait_for_timeout(2000)  # small wait for results page to load
    assert "playwright" in page.title().lower()
