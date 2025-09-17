from pages.google_page import GooglePage
from playwright.sync_api import expect

def test_google_search(page):
    google = GooglePage(page)
    google.goto()
    google.search("Playwright Python")

    # Wait for search results
    expect(page).to_have_title(lambda title: "playwright" in title.lower())
