# Fibonacci Telegram Bot

## 📌 Описание

Этот проект — Telegram-бот, который:
- Принимает от пользователя число
- Отвечает ближайшим числом Фибоначчи
- Сохраняет все запросы в базу данных (`SQLite`)
- Автоматически экспортирует CSV-файлы:
  - `top10_numbers.csv` — Топ-10 самых частых чисел
  - `last20_requests.csv` — Последние 20 запросов

> Подходит для анализа пользовательской активности через Yandex DataLens или другие BI-инструменты.

---

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/your-username/telegram-bot.git
cd telegram-bot

Создайте файл .env в корне проекта со следующим содержимым:
TELEGRAM_BOT_TOKEN="токен скину в телеграмме"


3. Запуск с помощью Docker
Убедитесь, что установлен Docker и docker-compose.

Запустите контейнер:

bash
docker-compose up --build -d
Бот начнёт принимать сообщения и сохранять запросы в базу данных (data/requests.db). CSV-файлы обновляются автоматически.

Структура проекта
telegram-bot/
│
├── main.py                # Основная логика Telegram-бота
├── export_data.py         # Экспорт из БД в CSV
├── show_requests.py       # (опционально) Просмотр последних запросов в терминале
│
├── docker-compose.yml     # Docker-сборка
├── requirements.txt       # Python-зависимости
├── .env                   # Секреты (не добавляется в git)
│
└── data/
    ├── requests.db            # База данных SQLite
    ├── last20_requests.csv    # Последние 20 запросов
    └── top10_numbers.csv      # Топ 10 самых частых чисел
    
Ручной экспорт csv
python export_data.py 
Просмотр последних 20 запросов 
python show_requests.py


Пример работы

Вы отправляете: 50
Бот отвечает: Ближайшее число Фибоначчи к 50 — 55
