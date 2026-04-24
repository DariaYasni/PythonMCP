def test_verify_articles_api_and_ui(api, home_page):
    # ШАГ 1: Проверяем доступность API сайта
    # На этом сайте нет открытого POST, поэтому используем GET для проверки связи
    response = api.get("") 
    assert response.ok, f"Сайт недоступен через API: {response.status}"
    
    # ШАГ 2: Открываем UI
    home_page.open()
    
    # ШАГ 3: Получаем заголовки через наш метод в HomePage
    titles = home_page.get_all_article_titles()
    
    # Проверяем, что статьи загрузились
    assert len(titles) > 0, "Список статей пуст! Проверьте локаторы в HomePage."
    
    # Проверяем наличие конкретной статьи, которая точно есть на этом сайте
    # (заголовок взят из вашего лога ошибки)
    expected_title = "When not to use AI"
    assert expected_title in titles, f"Статья '{expected_title}' не найдена. Список: {titles[:3]}"
    
    print(f"\nТест пройден! Найдено статей: {len(titles)}")
    print(f"Первый заголовок: {titles[0]}")