import pyaudio
import wave
import io
import sqlite3


class Player:
    CHUNK = 1024

    def random_clip(cur: sqlite3.Cursor) -> str:
        # Pick one clip at random
        cur.execute('SELECT path, content FROM clips ORDER BY random() LIMIT 1')
        row = cur.fetchone()
        print("row:::::", row)
        return (row[0], row[1])


    def play(audio_in: any):
        """
        audio_in is either a path to a WAV file or bytes containing WAV audio.
        """
        p = pyaudio.PyAudio()

        if type(audio_in) == type(b''):
            wf = wave.open(io.BytesIO(audio_in), 'rb')
        else:
            wf = wave.open(audio_in, 'rb')

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

        # read data
        data = wf.readframes(Player.CHUNK)

        # play stream
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(Player.CHUNK)

        # stop stream
        stream.stop_stream()
        stream.close()

        # close PyAudio
        p.terminate()


if __name__ == "__main__":
    p = Player()
    with open("path_of_file.wav", "rb") as f:
        p.play()
