import os
import sqlite3
from datetime import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)
print("Starting the bot...")
# Попытка подключить автоматический экспорт, если есть export_data.py
try:
    from export_data import export_to_csv
    AUTO_EXPORT = True
    print("Export_data импортирован успешно.")
except ImportError:
    AUTO_EXPORT = False
    print("Не удалось импортировать export_data")

# Папка для БД и сам файл
DATA_DIR = os.getenv('DATA_DIR', 'data')
DB_PATH = os.path.join(DATA_DIR, 'requests.db')


def find_nearest_fibonacci(target: float) -> int:
    a, b = 0, 1
    prev_fib = 0
    # находим ближайшее к target из чисел Фибоначчи
    while b <= target * 2:
        if abs(b - target) < abs(prev_fib - target):
            prev_fib = b
        a, b = b, a + b
    # сравниваем последний шаг
    return prev_fib if abs(prev_fib - target) < abs(a - target) else a


def init_db() -> None:
    """Создаёт папку и таблицу requests, если их нет."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            input_text TEXT NOT NULL,
            number REAL,
            response REAL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL
                CHECK(status IN ('success', 'invalid_number', 'negative', 'error'))
        );
    ''')
    conn.commit()
    conn.close()

    if AUTO_EXPORT: 
        export_to_csv()


def save_request(
    user_id: int,
    username: str | None,
    input_text: str,
    number: float | None,
    response: float | None,
    status: str
) -> None:
    """Сохраняет одну строку запроса в БД."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests
            (user_id, username, input_text, number, response, timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    ''', (
        user_id,
        username,
        input_text,
        number,
        response,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        status
    ))
    conn.commit()
    conn.close()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает любое текстовое сообщение от пользователя."""
    text = update.message.text.strip()
    user = update.message.from_user
    print(f"Получено сообщение: {update.message.text}")

    # Парсим число
    try:
        num = float(text)
        if num < 0:
            save_request(user.id, user.username, text, None, None, 'negative')
            await update.message.reply_text('Ошибка: введите положительное число!')
            return

        fib = find_nearest_fibonacci(num)
        save_request(user.id, user.username, text, num, fib, 'success')
        await update.message.reply_text(f'Ближайшее число Фибоначчи к {num} — {fib}')

    except ValueError:
        save_request(user.id, user.username, text, None, None, 'invalid_number')
        await update.message.reply_text('Ошибка: введите число, а не текст!')

    # Если подключён export_data.py — обновляем CSV
    if AUTO_EXPORT:
        try:
            export_to_csv()
        except Exception as e:
            # Ошибки экспорта логируем в консоль, но не ломаем бота
            print('Ошибка при автоматическом экспорте CSV:', e)


def main() -> None:
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print('ОШИБКА: переменная окружения TELEGRAM_BOT_TOKEN не задана.')
        return

    init_db()

    app = ApplicationBuilder().token(token).build()
    # Фильтруем только текст, без команд
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print('Бот запущен и готов к работе!')
    app.run_polling()


if __name__ == '__main__':
    main()
