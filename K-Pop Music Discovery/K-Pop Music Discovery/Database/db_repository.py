import sqlite3

DATABASE_NAME = "kpop_discovery.db"

class DatabaseRepository:

    def __init__(self):
        self.database_name = DATABASE_NAME

    def initialize_database(self):
        connections = sqlite3.connect(self.database_name)
        connection.close()
        