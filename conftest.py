import pytest
import os
from datetime import datetime

# Ensure screenshots folder exists
os.makedirs("screenshots", exist_ok=True)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to run after each test step.
    If test fails, capture a screenshot.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)
        if page:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/{item.name}_{timestamp}.png"
            page.screenshot(path=filename)
            print(f"\n📸 Screenshot saved to {filename}")
