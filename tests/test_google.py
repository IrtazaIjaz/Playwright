from playwright.sync_api import expect

def test_search_duckduckgo(page):
    page.goto("https://duckduckgo.com/")
    page.fill("input[name='q']", "Playwright Python")
    page.press("input[name='q']", "Enter")

    # Correct title check (DuckDuckGo format: "<query> at DuckDuckGo")
    expect(page).to_have_title("Playwright Python at DuckDuckGo")
