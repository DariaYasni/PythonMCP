from pages.home_page import HomePage

# Просто добавьте аргумент 'page'. 
# Pytest-playwright сам создаст браузер и передаст его сюда.
def test_home_has_books(page):
    # 1. Создаем объект страницы, передавая готовую фикстуру page
    home = HomePage(page)
    
    # 2. Используем ваши методы (они остаются синхронными, это нормально)
    home.open()
    titles = home.get_all_article_titles()
    
    # 3. Проверки
    assert len(titles) > 0, "На главной нет карточек со статьями!"
    
    # Печать сработает, если запустить pytest с флагом -s
    print(f"\n✓ Найдено статей: {len(titles)}")
    print(f"✓ Примеры заголовков: {titles[:3]}")

    