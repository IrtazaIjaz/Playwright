class GooglePage:
    def __init__(self, page):
        self.page = page
        # Support both input and textarea selectors
        self.search_box = "input[name='q'], textarea[name='q']"

    def goto(self):
        # Try Google first
        self.page.goto("https://www.google.com", wait_until="domcontentloaded")
        # handle cookie/consent popup if present
        try:
            consent = self.page.locator(
                "button:has-text('I agree'), "
                "button:has-text('Accept all'), "
                "button:has-text('Accept cookies')"
            )
            if consent.is_visible(timeout=2000):
                consent.click()
        except Exception:
            pass

    def search(self, text: str):
        # wait for search box; if it fails, fallback to DuckDuckGo
        try:
            self.page.wait_for_selector(self.search_box, timeout=20000)
        except Exception:
            # fallback to DuckDuckGo which is more CI-friendly
            self.page.goto("https://duckduckgo.com", wait_until="domcontentloaded")
            self.search_box = "input[name='q']"
            self.page.wait_for_selector(self.search_box, timeout=10000)

        self.page.fill(self.search_box, text)
        self.page.press(self.search_box, "Enter")
