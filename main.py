import os
from src.parser import ForumParser
from src.database import DatabaseRepository
from config import DB_PATH

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "tests", "fixtures", "page.html")


def main():
    print("Запуск парсера форума (локальный режим)...")
   
    print(f"Загрузка страницы из: {FIXTURE_PATH}")
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()
    print("Страница успешно загружена!")
    
    print("Извлечение комментариев...")
    comments = ForumParser.parse_page(html_content)
    print(f"Найдено комментариев: {len(comments)}")
    
    for c in comments:
        print(f"  - [{c.comment_id}] {c.name}: {c.message[:50]}...")
    
    print(f"\nСохранение в БД ({DB_PATH})...")
    repo = DatabaseRepository(DB_PATH)
    ForumParser.save_to_db(comments, repo)
    
    saved = repo.get_by_name("Mila")
    print(f"Проверка: найдено записей для Mila: {len(saved)}")
    print("Готово!")


if __name__ == "__main__":
    main()