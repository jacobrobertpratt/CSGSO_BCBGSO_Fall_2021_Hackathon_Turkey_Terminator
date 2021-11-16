import sqlite3
from sqlite3 import Error
from typing import List

from settings import database_path
from schemas import schemas, record_typing, triggers, views


class SQLController:
    instance = None

    def __init__(self):
        self.conn = None

    @staticmethod
    def get_instance():
        if SQLController.instance is None:
            SQLController.instance = SQLController()
        return SQLController.instance

    @staticmethod
    def reset_database():
        SQLController.delete_db()
        SQLController.get_instance().setup_tables()

    @staticmethod
    def delete_db():
        import os
        os.remove(database_path)

    def execute_query(self, query: str):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print('An Error occurred: {}'.format(e))

    def execute_read_query(self, query: str):
        cursor = self.conn.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print('An Error occurred: {}'.format(e))

    def connect(self):
        try:
            self.conn = sqlite3.connect(database_path)
        except Error as e:
            print('An Error occurred: {}'.format(e))

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()

    def setup_tables(self):
        self.connect()
        for schema in schemas:
            query = 'create table if not exists {}'.format(schema)
            self.execute_query(query)
        for trigger in triggers:
            query = 'create trigger if not exists {}'.format(trigger)
            self.execute_query(query)
        for view in views:
            query = 'create view if not exists {}'.format(view)
            self.execute_query(query)
        self.disconnect()

    def insert_record(self, table: str, records: List[tuple]):
        self.connect()
        query = 'insert into {} {} values {}'.format(table, record_typing[table],
                                                     ','.join(['({})'.format(', '.join(map(str, r))) for r in records]))
        self.execute_query(query)
        self.disconnect()

    def delete_record(self, table: str, identifier: str):
        self.connect()
        self.execute_query('delete from {} where {}'.format(table, identifier))
        self.disconnect()

    def delete_all(self, table: str):
        self.connect()
        self.execute_query('delete from {}'.format(table))
        self.disconnect()

    def select(self, table: str, query: str):
        self.connect()
        result = self.execute_read_query('select {} from {}'.format(query, table))
        self.disconnect()
        return result

    def select_conditional(self, table: str, query: str, conditional: str):
        self.connect()
        result = self.execute_read_query('select {} from {} where {}'.format(query, table, conditional))
        self.disconnect()
        return result

    def update_record(self, table: str, modification: str, conditional: str):
        self.connect()
        self.execute_query('update {} set {} where {}'.format(table, modification, conditional))
        self.disconnect()
