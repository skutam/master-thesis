import configparser
from os.path import realpath
from typing import Union, Optional, List, Tuple

import mysql.connector
from mysql.connector import errorcode, CMySQLConnection, MySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor

from src.PasswordChecker.Database.Password import Password


class Connector:
    def __init__(self):
        self._cnx: Optional[Union[CMySQLConnection, MySQLConnection]] = None
        self._cursor: Optional[CMySQLCursor] = None
        self._db_data = {}
        self._get_config_data()

    def _get_config_data(self):
        db_config = configparser.ConfigParser()
        db_config.read(realpath('credentials/db.ini'))  # TODO rewrite to use constants

        self._db_data['HOST'] = db_config['DB']['HOST']
        self._db_data['USER'] = db_config['DB']['USER']
        self._db_data['PASS'] = db_config['DB']['PASS']
        self._db_data['PORT'] = db_config['DB']['PORT']
        self._db_data['NAME'] = db_config['DB']['NAME']

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
                port=self._db_data['PORT'],
                database=self._db_data['NAME']
            )

        # Expect one of the following errors
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

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

    def insert_passwords(self, passwords: List[Tuple[str, int, int, int]]) -> bool:
        """
            Insert multiple passwords with data into database

            Parameters
            ----------
            passwords: List[Tuple[str, int, int]]
                Password with its data to be inserted into database

            Returns
            -------
            bool
                True when inserted, False on error

        """
        # Connect to database
        self._connect()

        try:
            # Create upsert query (INSERT or UPDATE) TODO update when inserting from guesses
            sql_insert_query = """INSERT INTO passwords (
            password, count, tool_generated_dataset, gen_count
            ) VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE gen_count=gen_count+VALUES(gen_count), tool_generated_dataset=tool_generated_dataset|VALUES(tool_generated_dataset);"""

            # Execute insert many in database
            self._cursor = self._cnx.cursor()
            self._cursor.executemany(sql_insert_query, passwords)

            # Commit changes
            self._cnx.commit()
        except mysql.connector.Error as error:
            print(error)
            self._close_connection()
            return False
        except AttributeError:
            print("\nATTRIBUTE ERROR\n")
            self._cnx = None
            self._cursor = None
            return False

        # Close connection
        self._close_connection()
        return True

    def get_passwords(self, _from: int, limit: int):
        # Connect to database
        self._connect()

        sql_select_query = 'SELECT * FROM passwords ORDER BY count LIMIT %s, %s'

        # Execute select query
        self._cursor = self._cnx.cursor()
        self._cursor.execute(sql_select_query, (_from, limit))

        # Get first found value
        record = self._cursor.fetchall()

        print(record)

        # Disconnect from database
        self._close_connection()
        pass

    def get_password_data(self, password: str) -> Union[Password, None, bool]:
        """
            Get data on given password

            Parameters
            ----------
            password: str
                Password to be searched for

            Returns
            -------
            Union[Password, None, bool]
                Password object, when data has been found, None when nothing was found, False on error
        """
        # Connect to database
        self._connect()

        try:
            # Create select query
            sql_select_query = 'SELECT * FROM passwords WHERE password=%s;'

            # Execute select query
            self._cursor = self._cnx.cursor()
            self._cursor.execute(sql_select_query, (password,))

            # Get first found value
            record = self._cursor.fetchone()

            # Close connection
            self._close_connection()

            # When nothing found, return None
            if record is None:
                return None

            # Data found, convert to Password object
            return Password(record)
        except mysql.connector.Error as error:
            print('Failed to select password from database'.format(error))
            self._close_connection()
            return False
        except AttributeError:
            self._cnx = None
            self._cursor = None
            return False
