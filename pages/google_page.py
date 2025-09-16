class GooglePage:
    def __init__(self, page):
        self.page = page
        self.search_box = "input[name='q']"

    def goto(self):
        self.page.goto("https://www.google.com", wait_until="domcontentloaded")

    def search(self, text):
        self.page.wait_for_selector(self.search_box, timeout=10000)
        self.page.fill(self.search_box, text)
        self.page.keyboard.press("Enter")
