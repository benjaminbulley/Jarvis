import sqlite3
import player

p = player.Player()


def music_clip(cur: sqlite3.Cursor) -> str:
    # Pick one clip at random
    cur.execute('SELECT description, content FROM sounds WHERE music=1 ORDER BY random() LIMIT 1')
    row = cur.fetchone()
    return (row[0], row[1])


def loud_clip(cur: sqlite3.Cursor) -> str:
    # Pick one clip at random
    cur.execute('SELECT description, content FROM sounds WHERE loud=1 ORDER BY random() LIMIT 1')
    row = cur.fetchone()
    return (row[0], row[1])


def quiet_clip(cur: sqlite3.Cursor) -> str:
    # Pick one clip at random
    cur.execute('SELECT description, content FROM sounds WHERE quiet=1 ORDER BY random() LIMIT 1')
    row = cur.fetchone()
    return (row[0], row[1])


def noise_clip(cur: sqlite3.Cursor) -> str:
    # Pick one clip at random
    cur.execute('SELECT description, content FROM sounds WHERE noise=1 ORDER BY random() LIMIT 1')
    row = cur.fetchone()
    return (row[0], row[1])


def play_random_music():
    con = sqlite3.connect('sounds.db')
    cur = con.cursor()

    name, blob = music_clip(cur)
    print(f"about to play:{name}")

    p.play(blob)
