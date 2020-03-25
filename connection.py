from sqlite3 import connect


class Connection:
    __prepare_db_stmt = """CREATE TABLE IF NOT EXISTS `tracks` ( `id` VARCHAR(191) NOT NULL , `performance_id` VARCHAR(191) NOT NULL , `artist` VARCHAR(191) NOT NULL, `title` VARCHAR(191) NOT NULL , PRIMARY KEY (`performance_id`));
        CREATE TABLE IF NOT EXISTS `plays` ( `user_id` VARCHAR(191) NOT NULL , `track_id` VARCHAR(191) NOT NULL , `timestamp` INT(12) NOT NULL );
        CREATE INDEX IF NOT EXISTS "plays_track_id_index" ON "plays" ("track_id");
        CREATE INDEX IF NOT EXISTS "tracks_id_index" ON "tracks" ("id");"""

    def __init__(self, target_file: str):
        self.__connection = connect(target_file)

    def init(self, tracks_file: str, plays_file: str):
        print('*** Preparing database...')

        with self.__connection:
            self.__connection.executescript(self.__prepare_db_stmt)

            with open(tracks_file, 'r', encoding='ISO-8859-1') as tfd:
                for line in tfd:
                    performance_id, track_id, artist, title = line.split('<SEP>')
                    self.__connection.execute('INSERT INTO tracks VALUES (?, ?, ?, ?)', (track_id, performance_id, artist, title))

            with open(plays_file, 'r', encoding='ISO-8859-1') as pfd:
                for line in pfd:
                    self.__connection.execute('INSERT INTO plays VALUES (?, ?, ?)', line.split('<SEP>'))

        print('*** Database prepared\n\n')

    @property
    def connection(self):
        return self.__connection

    def disconnect(self):
        self.__connection.close()
