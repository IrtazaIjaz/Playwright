import pytest
from pages.login_page import LoginPage

def test_checkout_flow(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")
    # Add first product to cart
    page.locator(".inventory_item button").first.click()
    page.locator(".shopping_cart_link").click()
    assert page.locator(".cart_item").is_visible(), "Product not added to cart"
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
    assert confirmation.is_visible(), "Order confirmation not visible after checkout"
    assert "thank you for your order" in confirmation.text_content().lower(), \
        f"Unexpected confirmation message: {confirmation.text_content()}"
