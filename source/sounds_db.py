import sqlite3
import logging

logger = logging.getLogger(__name__)


class SoundDB:
    """
    Interface to a SQLite3 database.
    Note that sqlite3 is thread safe, for reading, but requires
    check_same_thread=False is set in calls to connect().  By
    default check_same_thread is True, so we leave it this way
    and only access the DB from one thread.
    """
    def __init__(self, con: str) -> None:
        """
        :param con: a valid URI, e.g. "file:sounds.db?mode=rw"
        :type con: str
        """
        self.uri = con
        self.verify_db()
        pass

    def verify_db(self):
        """Ensure connection to the database is possible.
        """
        con = sqlite3.connect(self.uri, uri=True)
        con.close()
        pass

    def get_content(self, sound: str) -> bytes:
        with sqlite3.connect(self.uri, uri=True) as con:
            cur = con.cursor()
            cur.execute('SELECT content FROM sounds WHERE name=?', (sound,))
            row = cur.fetchone()
            return row[0]

    def get_music(self, cur: sqlite3.Cursor) -> str:
        # Pick one clip at random
        with sqlite3.connect(self.uri, uri=True) as con:
            cur.execute('SELECT content FROM sounds WHERE music=1, ORDER BY random() LIMIT 1')
            row = cur.fetchone()
            return row[0]

    def get_loud_sound(self, cur: sqlite3.Cursor) -> str:
        # Pick one clip at random
        with sqlite3.connect(self.uri, uri=True) as con:
            cur.execute('SELECT description, content FROM sounds WHERE loud=1, ORDER BY random() LIMIT 1')
            row = cur.fetchone()
            print("row:::::", row[0])
            return (row[0], row[1])


# SoundDB("file:sounds.db?mode=ro")

SoundDB.get_content()
