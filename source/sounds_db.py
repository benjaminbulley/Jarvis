import sqlite3
import logging

logger = logging.getLogger(__name__)


class SoundDB:

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
