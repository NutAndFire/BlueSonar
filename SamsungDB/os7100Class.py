import sqlite3
from typing import List


class DB(object):
    def __init__(self):
        self.__file_location = str
        self.__conn = None
        self.__cursor = None
        self.__rows = []

    def connection(self, file='SamsungDB\\SamsungDB.db'):
        self.__file_location = file
        self.__conn = sqlite3.connect(self.__file_location)
        self.__cursor = self.__conn.cursor()

    def read_from_db(self):
        self.__cursor.execute("SELECT Name, IPaddress, MAC, Password, System, Patch FROM SamsungPBX WHERE NOT MAC=''")
        self.__rows = self.__cursor.fetchall()
        return self.__rows

    @staticmethod
    def list_size(box):
        return len(box)