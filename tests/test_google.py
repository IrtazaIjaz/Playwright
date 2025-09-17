from pages.google_page import GooglePage
from playwright.sync_api import expect

def test_google_search(page):
    google = GooglePage(page)
    google.goto()
    google.search("Playwright Python")

    # Wait until title contains "Playwright"
    expect(page).to_have_title(r".*Playwright.*")
