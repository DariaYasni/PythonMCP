from mcp.server.fastmcp import FastMCP
import subprocess
import os

# Создаем сервер под именем вашего проекта
mcp = FastMCP("QA-Python-Assistant")

@mcp.tool()
def run_tests():
    """Запускает все 45 тестов Playwright. Используй это, чтобы проверить текущее состояние проекта."""
    # Команда для запуска pytest
    result = subprocess.run(["pytest", "--alluredir=allure-results"], capture_output=True, text=True)
    return f"Результаты тестов:\n{result.stdout}\n{result.stderr}"

@mcp.tool()
def list_test_files():
    """Показывает список всех файлов с тестами в папке tests."""
    files = os.listdir("tests")
    return f"Файлы в папке tests: {', '.join(files)}"

@mcp.tool()
def get_ci_config():
    """Читает файл конфигурации CI (GitHub Actions), чтобы ИИ мог найти ошибки в настройках."""
    path = ".github/workflows/tests.yml" # проверьте имя вашего yml файла
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return "Файл CI не найден."

if __name__ == "__main__":
    mcp.run()