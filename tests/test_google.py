from playwright.sync_api import expect

def test_search_duckduckgo(page):
    page.goto("https://duckduckgo.com/")
    page.fill("input[name='q']", "Playwright Python")
    page.press("input[name='q']", "Enter")

    # Title check (DuckDuckGo format is "<query> at DuckDuckGo")
    expect(page).to_have_title(lambda title: "playwright" in title.lower())
