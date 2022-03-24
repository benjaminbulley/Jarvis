import sqlite3
from audio_player import player
"""
Interface to a SQLite3 database.
Note that sqlite3 is thread safe, for reading, but requires
check_same_thread=False is set in calls to connect().  By
default check_same_thread is True, so we leave it this way
and only access the DB from one thread.
"""


def get_content(cur, sound: str) -> bytes:
    cur.execute('SELECT description, content FROM sounds WHERE description=?', (sound,))
    row = cur.fetchone()
    return (row[0], row[1])


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


def play_audio(play_request: str):
    con = sqlite3.connect('sounds.db')
    cur = con.cursor()
    try:
        if "play loud" in play_request.lower():
            name, blob = loud_clip(cur)
            print(f"about to play:{name}")
            player.player_thread(blob)
        elif "play music" in play_request.lower():
            name, blob = music_clip(cur)
            print(f"about to play:{name}")
            player.player_thread(blob)
        else:
            what_to_play()

    except sqlite3.OperationalError:
        print("Could not find sound")
        couldnt_find()


def didnt_understand():
    with open("../wav_files/didnt_understand.wav", "rb") as file:
        player.player_thread(file)


def couldnt_find():
    with open("../wav_files/couldnt_find.wav", "rb") as file:
        player.player_thread(file)


def what_to_play():
    with open("../wav_files/what_to_play.wav", "rb") as file:
        player.player_thread(file)

