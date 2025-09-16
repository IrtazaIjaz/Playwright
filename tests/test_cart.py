import pytest
from pages.login_page import LoginPage

def test_add_item_to_cart(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("standard_user", "secret_sauce")
    # Add first product to cart
    page.locator(".inventory_item button").first.click()
    # Assert cart badge count is 1
    cart_badge = page.locator(".shopping_cart_badge")
    assert cart_badge.is_visible(), "Cart badge not visible after adding product"
    assert cart_badge.text_content() == "1", f"Cart count is not 1, got {cart_badge.text_content()}"
    # Go to cart
    page.locator(".shopping_cart_link").click()
    # Assert product is in cart
    assert page.locator(".cart_item").is_visible(), "Product not added to cart"
