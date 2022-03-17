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
            cur.execute('SELECT content FROM tunes WHERE name=?', (sound,))
            row = cur.fetchone()
            return row[0]


# SoundDB("file:sounds.db?mode=ro")


