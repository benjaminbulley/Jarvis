
# A prototype binary file archive
#
import sqlite3
import logging
import sys

logging.basicConfig(level=logging.DEBUG)


def add_blob(cursor, path:str, content:any, size:int, music:bool, loud:bool) -> bool:
    logging.debug(f'add_blob({path})')
    sql_insert = 'INSERT INTO "sounds" ("path", "content", "size", "music", "loud") VALUES (?, ?, ?, ?, ?)'
    cursor.execute(sql_insert, (path, content, size, music, loud))
    return True


if __name__ == '__main__':
    try:
        path = sys.argv[1]
        con = sqlite3.connect('sounds.db')
        cur = con.cursor()
    except IndexError:
        sys.exit("Usage: add_blob.py music/loud/tune-name.wav")

    try:
        # Convert DOS style path to Unix style
        path = path.replace('\\','/')
        title = path.split('/')[-1]
        vol = path.split('/')[-2]
        cat = path.split('/')[-3]
    except IndexError as ex:
        logging.error(ex)
        sys.exit('Invalid path')

    # Use boolean values for category and volume.
    music = (cat == "music")
    loud = (vol == "loud")
    logging.debug(f'music:{music} loud:{loud}')

    with open(path, "rb") as f:
        data = f.read()
        size = len(data)
        logging.info(f'category:{cat} volume:{vol} size:{size} {title}')
        add_blob(cur, title, data, size, music, loud)
        con.commit()

    con.close()

