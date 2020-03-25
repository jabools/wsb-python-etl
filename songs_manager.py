from sqlite3 import Connection


class SongsManager:
    def __init__(self, connection: Connection):
        self.__connection = connection

    def best_artist(self):
        with self.__connection:
            return self.__connection.execute("""SELECT p.artist, p.plays FROM (
                SELECT t.artist as artist, count(*) as plays FROM tracks t
                JOIN plays ON plays.track_id = t.id
                GROUP BY artist
                ORDER BY plays DESC
                LIMIT 1
            ) p""").fetchone()

    def top_listened_songs(self):
        with self.__connection:
            return self.__connection.execute("""SELECT artist, title, count(*) as song_plays
                FROM tracks
                JOIN plays on plays.track_id = tracks.id
                GROUP BY tracks.id
                ORDER BY song_plays DESC
                LIMIT 5
            """)
