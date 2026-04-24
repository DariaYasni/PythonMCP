import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage  

def test_e2e_open_article(page: Page):
    home = HomePage(page)
    home.open()
    expected_title = home.open_first_book()
    
    expect(page.locator("h1")).to_have_text(expected_title)














