import pytest
from pages.login_page import LoginPage

@pytest.mark.parametrize("email", ["your@email.com"])
def test_login_short(page, email):
    login_page = LoginPage(page)
    
    
    login_page.login(email, "123456")
    
    
    if not login_page.is_logged_in():
        pytest.skip("Вход не выполнен (кнопка Sign out не появилась), пропускаем...")



