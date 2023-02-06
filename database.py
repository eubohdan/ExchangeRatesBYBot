import sqlite3 as sq


def start_db():
    with sq.connect('data_cur.db') as con:
        cur = con.cursor()
        print('[INFO] SQLite database was connected.')
        cur.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER, first_name TEXT, last_name TEXT, username TEXT, reg_date TEXT)')
        cur.close()


def new_user(user_id: int, first_name: str | None, last_name: str | None, username: str | None, reg_date: str) -> None:
    with sq.connect('data_cur.db') as con:
        cur = con.cursor()
        result = cur.execute(f'''SELECT "user_id" FROM users WHERE "user_id" = {user_id}''').fetchone()
        if result is None:
            cur.execute('INSERT INTO users (user_id, first_name, last_name, username, reg_date) VALUES (?, ?, ?, ?, ?)', (user_id, first_name, last_name, username, reg_date))
        cur.close()
