import sqlite3

# путь к вашей базе данных (локально — в папке data)
db_path = 'data/requests.db'

def show_requests(limit=20):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # выбираем поля: время, пользователь, вопрос, ответ, статус
    cur.execute("""
        SELECT
            timestamp,
            username,
            input_text,
            response,
            status
        FROM requests
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    rows = cur.fetchall()
    conn.close()
    
    print(f"Последние {limit} запросов:")
    for idx, (ts, user, inp, resp, st) in enumerate(rows, 1):
        print(f"{idx:2d}. [{ts}] @{user or '—'} — \"{inp}\" → {resp} ({st})")

if __name__ == '__main__':
    show_requests(20)
