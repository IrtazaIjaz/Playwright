import pytest
from pages.login_page import LoginPage
from utils.helpers import assert_text_contains

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

    # Robust checks
    # 1) page URL shows checkout complete
    assert "/checkout-complete.html" in page.url, f"Not on checkout complete page, current url: {page.url}"

    # 2) normalized confirmation text contains expected words (case/punctuation insensitive)
    confirmation_text = page.locator(".complete-header").text_content()
    assert_text_contains(confirmation_text, "thank you for your order", f"Unexpected confirmation message: {confirmation_text}")
