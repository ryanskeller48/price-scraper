import logging
import sqlite3

from sqlite3 import Error as SQLiteError


LOG = logging.getLogger(__name__)


class PricesDB:
    

    def __init__(self, file_loc):

        self.db = self.create_db(file_loc)


    def create_db(self, db_file):
        """ Create DB connection. """

        db = None
        try:
            db = sqlite3.connect(db_file)
        except SQLiteError as e:
            LOG.error(e)
        finally:
            if db:
                return db


    def create_table(self, name):
        """ Create table for db. """

        clean_table_sql = f"DROP TABLE IF EXISTS {name}"
        prices_table_sql = \
            f""" CREATE TABLE IF NOT EXISTS {name} (
                    id integer PRIMARY KEY,
                    name text NOT NULL,
                    description text,
                    price real NOT NULL,
                    sale_price real,
                    out_of_stock integer NOT NULL,
                    url text
                ); """
        try:
            cursor = self.db.cursor()
            # Delete old table
            cursor.execute(clean_table_sql)
            # Make new table
            cursor.execute(prices_table_sql)
        except SQLiteError as e:
            LOG.error(e)


    def insert_row(self, row):
        """ Insert row into db. """

        insert_sql = """INSERT INTO prices(name, description, price, sale_price, out_of_stock, url)
                        VALUES(?, ?, ?, ?, ?, ?)"""

        try:
            cursor = self.db.cursor()
            cursor.execute(insert_sql, row)
            self.db.commit()
        except SQLiteError as e:
            LOG.error(e)


    def query_db(self, sql):
        """ Send query to DB and return rows. """

        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
        except SQLiteError as e:
            LOG.error(e)
        return rows


    def close(self):
        """ Clean up. """

        self.db.close()
