# conftest.py
import os
import pytest
from datetime import datetime

# ensure screenshots dir exists
os.makedirs("screenshots", exist_ok=True)

@pytest.fixture(autouse=True)
def configure_page_timeout(page):
    """
    Runs for every test automatically and sets a sane default timeout for Playwright actions.
    """
    page.set_default_timeout(20000)  # 20s default for wait_for_selector etc.
    yield

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    When a test fails (during "call"), take a screenshot automatically.
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)
        if page:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"{item.name}_{ts}.png"
            path = os.path.join("screenshots", name)
            try:
                page.screenshot(path=path)
                print(f"\n📸 Screenshot saved to {path}")
            except Exception as e:
                print(f"\n⚠️ Failed to save screenshot: {e}")
