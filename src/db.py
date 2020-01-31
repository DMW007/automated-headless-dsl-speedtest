import sqlite3

class DB:
    __con: sqlite3.Connection = None
    def __init__(self):
        self.__con = sqlite3.connect('db/speedtests.db')
        self.__con.row_factory = sqlite3.Row

        self.__con.execute('''
            CREATE TABLE IF NOT EXISTS speedtests(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                date DATETIME NOT NULL,
                download INTEGER NOT NULL,
                upload INTEGER NOT NULL,
                ping INTEGER NOT NULL
            );
        ''')

    def __exit__(self, exc_type, exc_value, traceback):
        print(self.__con)
        self.__con.close()

    def save(self, download, upload, ping):
        q = 'insert into speedtests(date,download,upload,ping) values(datetime("now"), ?, ?, ?)'
        self.__con.execute(q, (download, upload, ping,))
        self.__con.commit()

    def get(self):
        c = self.__con.execute('select * from speedtests order by date desc')
        rows = c.fetchall()
        return rows