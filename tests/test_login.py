import pytest
from playwright.sync_api import sync_playwright

# Helper: take screenshot on failure
def take_screenshot_on_failure(page, name):
    page.screenshot(path=f"screenshots/{name}.png")

# Fixture: set up and tear down browser/page
@pytest.fixture(scope="function")
def setup():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # set headless=True for CI
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.saucedemo.com/")
        yield page
        context.close()
        browser.close()

# -------------------------
# Tests
# -------------------------

def test_login_valid_user(setup):
    page = setup
    page.fill("input[data-test='username']", "standard_user")
    page.fill("input[data-test='password']", "secret_sauce")
    page.click("input[data-test='login-button']")

    try:
        assert page.url == "https://www.saucedemo.com/inventory.html"
    except AssertionError:
        take_screenshot_on_failure(page, "login_valid_user")
        raise

def test_login_invalid_user(setup):
    page = setup
    page.fill("input[data-test='username']", "locked_out_user")
    page.fill("input[data-test='password']", "secret_sauce")
    page.click("input[data-test='login-button']")

    error_message = page.locator("h3[data-test='error']")
    try:
        assert error_message.is_visible()
        assert "locked out" in error_message.text_content().lower()
    except AssertionError:
        take_screenshot_on_failure(page, "login_invalid_user")
        raise

def test_add_products_and_checkout(setup):
    page = setup
    page.fill("input[data-test='username']", "standard_user")
    page.fill("input[data-test='password']", "secret_sauce")
    page.click("input[data-test='login-button']")

    # Add products
    page.click("button[data-test='add-to-cart-sauce-labs-backpack']")
    page.click("button[data-test='add-to-cart-sauce-labs-bike-light']")
    page.click("a.shopping_cart_link")

    # Checkout flow
    page.click("button[data-test='checkout']")
    page.fill("input[data-test='firstName']", "John")
    page.fill("input[data-test='lastName']", "Doe")
    page.fill("input[data-test='postalCode']", "12345")
    page.click("input[data-test='continue']")
    page.click("button[data-test='finish']")

    # Confirmation
    confirmation = page.locator(".complete-header")
    try:
        assert confirmation.is_visible(), "Order confirmation not visible after checkout"
        assert "thank you for your order" in confirmation.text_content().lower(), \
            f"Unexpected confirmation message: {confirmation.text_content()}"
    except AssertionError:
        take_screenshot_on_failure(page, "order_confirmation")
        raise
