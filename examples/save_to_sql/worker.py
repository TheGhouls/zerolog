import sqlite3
from zerolog.worker import BaseWorker


class MyWorker(BaseWorker):

    def __init__(self, backend, *args, **kwargs):
        super(MyWorker, self).__init__(backend, *args, **kwargs)
        self.connection = sqlite3.connect("/tmp/example.db")
        self.cursor = self.connection.cursor()

    def process_data(self, data):
        print(data)
        self.cursor.execute('''
        INSERT INTO logs (message) values (?)
        ''', [data])
        self.connection.commit()
