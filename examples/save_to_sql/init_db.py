import sqlite3


def init_db():
    conn = sqlite3.connect("/tmp/example.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE logs(id INTEGER AUTO_INCREMENT, message);''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
