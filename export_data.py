import sqlite3
import csv
import os

# Путь к папке с данными, можно переопределить через DATA_DIR
DATA_DIR = os.getenv('DATA_DIR', 'data')
DB_PATH = os.path.join(DATA_DIR, 'requests.db')
# Убедимся, что папка для данных существует
os.makedirs(DATA_DIR, exist_ok=True)


def export_to_csv():
    # Подключаемся к базе данных
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Топ-10 запрашиваемых чисел
    cursor.execute('''
        SELECT number, COUNT(*) as request_count 
        FROM requests 
        WHERE status = 'success' AND number IS NOT NULL
        GROUP BY number 
        ORDER BY request_count DESC 
        LIMIT 10
    ''')
    top10 = cursor.fetchall()

    # Сохраняем в CSV
    file_top10 = os.path.join(DATA_DIR, 'top10_numbers.csv')
    with open(file_top10, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Число', 'Количество запросов'])
        writer.writerows(top10)

    # 2. 20 последних запросов
    cursor.execute('''
        SELECT
            timestamp,
            username,
            input_text,
            response,
            status
        FROM requests
        ORDER BY timestamp DESC
        LIMIT 20
    ''')
    last20 = cursor.fetchall()

    # Сохраняем в CSV
    file_last20 = os.path.join(DATA_DIR, 'last20_requests.csv')
    with open(file_last20, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Время запроса', 'Имя пользователя', 'Введенный текст', 'Ответ бота', 'Статус'])
        writer.writerows(last20)

    # Закрываем соединение
    conn.close()

    print("Данные успешно экспортированы:")
    print(f"- {file_top10}")
    print(f"- {file_last20}")


if __name__ == '__main__':
    export_to_csv()
