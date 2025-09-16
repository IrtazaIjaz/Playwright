from pages.google_page import GooglePage

def test_google_search(page):
    google = GooglePage(page)
    google.goto()
    google.search("Playwright Python")
    assert "Playwright" in page.title()
