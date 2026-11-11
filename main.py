from src.loader import Loader
from src.parser import ForumParser
from src.database import DatabaseRepository
from config import TARGET_URL, DB_PATH


def main():
    print("Запуск парсера форума (режим сети)...")
   
    print(f"Загрузка страницы: {TARGET_URL}")
    try:
        html_content = Loader.load(TARGET_URL)
        print("Страница успешно загружена!")
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return
    
    print("\nИзвлечение комментариев...")
    comments = ForumParser.parse_page(html_content)
    print(f"Найдено комментариев: {len(comments)}")
    
    if comments:
        print("\nПервые 5 комментариев:")
        for c in comments[:5]:
            msg_preview = c.message[:60].replace('\n', ' ')
            print(f"  - [{c.comment_id}] {c.name}: {msg_preview}...")
  
    print(f"\nСохранение в БД ({DB_PATH})...")
    repo = DatabaseRepository(DB_PATH)
    ForumParser.save_to_db(comments, repo)
    
    saved_count = len(repo.get_by_name("Anonymous"))
    print(f"Проверка: найдено записей для Anonymous: {saved_count}")
    print("\nГотово!")


if __name__ == "__main__":
    main()