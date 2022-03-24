import sqlite3
import threading

from audio_player import Player

p = Player()
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


def play_audio(play_request):
    con = sqlite3.connect('sounds.db')
    cur = con.cursor()
    try:
        if play_request == "hello":
            p.play(open("../wav_files/hello.wav", "rb"))
        elif play_request == "goodbye":
            p.play(open("../wav_files/goodbye.wav", "rb"))
        elif play_request == "couldnt_find":
            p.play(open("../wav_files/couldnt_find.wav", "rb"))
        elif play_request == "didnt_understand":
            p.play(open("../wav_files/didnt_understand.wav", "rb"))
        elif play_request == "what_to_play":
            p.play(open("../wav_files/what_to_play.wav", "rb"))
        elif play_request == "cant_connect":
            p.play(open("../wav_files/cant_connect.wav", "rb"))
        elif play_request == "output":
            p.play(open("../wav_files/output.wav", "rb"))

        elif play_request[5:].startswith == "loud":
            name, blob = loud_clip(cur)
            print(f"about to play:{name}")
            p.play(blob)
        elif play_request[5:].startswith == "music":
            name, blob = music_clip(cur)
            print(f"about to play:{name}")
            p.play(blob)
        else:
            what_to_play()

    except sqlite3.OperationalError:
        print("Could not find sound")
        couldnt_find()


def player_thread(text_from_speech):
    thread = threading.Thread(target=lambda x=text_from_speech: play_audio(x), daemon=True)
    thread.start()
    return thread


def didnt_understand():
    with open("../wav_files/didnt_understand.wav", "rb") as file:
        p.play(file)


def couldnt_find():
    with open("../wav_files/couldnt_find.wav", "rb") as file:
        p.play(file)


def what_to_play():
    with open("../wav_files/what_to_play.wav", "rb") as file:
        p.play(file)
