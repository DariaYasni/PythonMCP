import pytest
from pages.login_page import LoginPage


def test_account_button_is_visible_after_login(page):
    login_page = LoginPage(page)
    
   
    login_page.login("test@example.com", "123456")
    
    
    assert login_page.account_btn.is_visible(), "Кнопка 'Sign up' не видна на странице!"