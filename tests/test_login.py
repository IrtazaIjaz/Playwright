from pages.login_page import LoginPage
import pytest
import time

# Utility to take screenshot on failure
def take_screenshot_on_failure(page, name):
    page.screenshot(path=f"screenshots/{name}.png")

@pytest.mark.tryfirst
def test_valid_login(page):
    login_page = LoginPage(page)
    try:
        login_page.goto()
    except Exception as e:
        take_screenshot_on_failure(page, "valid_login_navigation_error")
        pytest.fail(f"Navigation failed: {e}")
    try:
        login_page.login("standard_user", "secret_sauce")
    except Exception as e:
        take_screenshot_on_failure(page, "valid_login_error")
        pytest.fail(f"Login failed: {e}")
    # assert we land on inventory page
    assert "inventory" in page.url
    assert page.locator(".inventory_list").is_visible(), "Inventory list is not visible after login"
    assert page.locator("#logout_sidebar_link").is_visible(), "Logout button is not visible after login"
    time.sleep(2)

@pytest.mark.tryfirst
def test_invalid_login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("wrong_user", "wrong_pass")
    # Assert error message is visible and text is correct
    error = page.locator("h3[data-test='error']")
    try:
        assert error.is_visible(), "Error message not shown for invalid credentials"
        assert "Username and password do not match" in error.text_content(), "Unexpected error message for invalid credentials"
    except AssertionError:
        take_screenshot_on_failure(page, "invalid_login")
        raise
    time.sleep(2)

@pytest.mark.tryfirst
def test_blank_fields_login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("", "")
    # Assert error message is visible and text is correct
    error = page.locator("h3[data-test='error']")
    try:
        assert error.is_visible(), "Error message not shown for blank fields"
        assert "Username is required" in error.text_content(), "Unexpected error message for blank fields"
    except AssertionError:
        take_screenshot_on_failure(page, "blank_fields_login")
        raise
    time.sleep(2)

@pytest.mark.tryfirst
def test_locked_out_user_login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("locked_out_user", "secret_sauce")
    # Assert error message is visible and text is correct
    error = page.locator("h3[data-test='error']")
    try:
        assert error.is_visible(), "Error message not shown for locked-out user"
        assert "Sorry, this user has been locked out." in error.text_content(), "Unexpected error message for locked-out user"
    except AssertionError:
        take_screenshot_on_failure(page, "locked_out_user_login")
        raise
    time.sleep(2)

@pytest.mark.tryfirst
def test_add_products_and_checkout(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")
    # Add first product to cart
    page.locator(".inventory_item button").first.click()
    # Assert cart badge count is 1
    cart_badge = page.locator(".shopping_cart_badge")
    try:
        assert cart_badge.is_visible(), "Cart badge not visible after adding product"
        assert cart_badge.text_content() == "1", f"Cart count is not 1, got {cart_badge.text_content()}"
    except AssertionError:
        take_screenshot_on_failure(page, "cart_badge_count")
        raise
    # Go to cart
    page.locator(".shopping_cart_link").click()
    # Assert product is in cart
    try:
        assert page.locator(".cart_item").is_visible(), "Product not added to cart"
    except AssertionError:
        take_screenshot_on_failure(page, "add_product_to_cart")
        raise
    # Proceed to checkout
    page.locator("button[name='checkout']").click()
    # Fill checkout details
    page.locator("input[data-test='firstName']").fill("John")
    page.locator("input[data-test='lastName']").fill("Doe")
    page.locator("input[data-test='postalCode']").fill("12345")
    page.locator("input[name='continue']").click()
    # Finish checkout
    page.locator("button[data-test='finish']").click()
    # Assert order confirmation
    confirmation = page.locator(".complete-header")
    try:
        assert confirmation.is_visible(), "Order confirmation not visible after checkout"
        assert "THANK YOU FOR YOUR ORDER" in confirmation.text_content(), "Unexpected confirmation message"
    except AssertionError:
        take_screenshot_on_failure(page, "order_confirmation")
        raise
    time.sleep(2)
