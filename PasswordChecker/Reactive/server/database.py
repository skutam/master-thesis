import configparser
import sys
from os.path import realpath
from typing import Union, Optional

import mysql.connector
from mysql.connector import errorcode, CMySQLConnection, MySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor


class Database:
    def __init__(self):
        self._cnx: Optional[Union[CMySQLConnection, MySQLConnection]] = None
        self._cursor: Optional[CMySQLCursor] = None
        self._db_data = {}
        self._get_config_data()

    def _get_config_data(self):
        db_config = configparser.ConfigParser()
        db_config.read(realpath('../credentials/db.ini'))

        self._db_data['HOST'] = db_config['DB']['HOST']
        self._db_data['USER'] = db_config['DB']['USER']
        self._db_data['PASS'] = db_config['DB']['PASS']
        self._db_data['PORT'] = db_config['DB']['PORT']
        self._db_data['NAME'] = db_config['DB']['NAME']

    def get_passwords(self, _from: int, limit: int):
        # Connect to database
        self._connect()

        if self._cnx is None:
            return []

        sql_select_query = 'SELECT * FROM passwords ORDER BY count DESC LIMIT %s, %s'

        # Execute select query
        self._cursor = self._cnx.cursor()
        self._cursor.execute(sql_select_query, (_from, limit))

        # Get first found value
        record = self._cursor.fetchall()

        # Disconnect from database
        self._close_connection()
        
        return record

    def _connect(self):
        """
            Create connection to database
        """
        try:
            # Create connection to database
            self._cnx = mysql.connector.connect(
                host=self._db_data['HOST'],
                user=self._db_data['USER'],
                password=self._db_data['PASS'],
                port=int(self._db_data['PORT']),
                database=self._db_data['NAME']
            )

        # Expect one of the following errors
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password", file=sys.stderr)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist", file=sys.stderr)
            else:
                print(err, file=sys.stderr)

            # On error clear cnx
            self._cnx = None

    def _close_connection(self):
        """
            Close connection to database and close cursor
        """
        # When we are connected to database, clear connection
        if self._cnx is not None and self._cnx.is_connected():
            # When cursor is set clear cursor
            if self._cursor is not None:
                self._cursor.close()
                self._cursor = None

            self._cnx.close()
            self._cnx = None
