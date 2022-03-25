"""
Some functions that interfaces with the database and plays local files
"""
import sqlite3
import player


def music_clip(cur: sqlite3.Cursor) -> str:
    """
    Collects blob from database where music is True
    :param cur- Connection to database
    :returns: description and content
    """
    # Pick one clip at random
    cur.execute('SELECT description, content FROM sounds WHERE music=1 ORDER BY random() LIMIT 1')
    row = cur.fetchone()
    return (row[0], row[1])


def loud_clip(cur: sqlite3.Cursor) -> str:
    """
    Collects blob from database where loud is True
    :param cur- Connection to database
    :returns description and content
    """
    # Pick one clip at random
    cur.execute('SELECT description, content FROM sounds WHERE loud=1 ORDER BY random() LIMIT 1')
    row = cur.fetchone()
    return (row[0], row[1])


def play_audio(play_request: str):
    """
    logic for what kind of audio is played
    :param play_request (str)- returned string from Speech to text
    """
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
        player.player_thread_local(file)


def couldnt_find():
    with open("../wav_files/couldnt_find.wav", "rb") as file:
        player.player_thread_local(file)


def what_to_play():
    with open("../wav_files/what_to_play.wav", "rb") as file:
        player.player_thread_local(file)
