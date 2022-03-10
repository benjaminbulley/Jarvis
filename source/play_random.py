import sqlite3


def random_clip(self, cur: sqlite3.Cursor) -> str:
    # Pick one clip at random
    cur.execute('SELECT path, content FROM clips ORDER BY random() LIMIT 1')
    row = cur.fetchone()
    print("row:::::", row)
    return (row[0], row[1])
