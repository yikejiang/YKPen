import os
import sys
import sqlite3


class BasicConfig:
    def __init__(self):
        super(BasicConfig, self).__init__()

    @staticmethod
    def read_profile_folder_path():
        if os.name == 'nt':
            profile_path = os.path.join(os.environ['LOCALAPPDATA'], 'YKPen')
        elif sys.platform == 'darwin':
            profile_path = os.path.join(os.environ['HOME'], '.YKPen')
        else:
            profile_path = os.path.join(os.environ['HOME'], '.config/YKPen')

        profile_path = os.path.normpath(profile_path)

        if os.path.exists(profile_path) is False:
            os.mkdir(profile_path)

        return profile_path


class Database:
    def __init__(self):
        super(Database, self).__init__()

        self.basicconfig = BasicConfig()
        self.db = None
        self.db_cursor = None

        self.profile_folder_path = self.basicconfig.read_profile_folder_path()

        self.initialize_db()

    def read_db_path(self):
        db_path = os.path.join(self.profile_folder_path, 'YKPen_database.db')
        return db_path

    def initialize_db(self):
        self.open_db()

        self.db_cursor.execute(
            'CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'title, text, creation_time, last_modified_time, file_path)'
        )

        self.close_db()

    def open_db(self):
        db_path = self.read_db_path()
        self.db = sqlite3.connect(db_path)
        self.db_cursor = self.db.cursor()

    def close_db(self):
        self.db.commit()
        self.db.close()

    # Add a record
    def insert_record(self, title, text, creation_time, last_modified_time, file_path):
        self.open_db()

        db_command = 'INSERT INTO data (title, text, creation_time, last_modified_time, file_path) ' \
                     'VALUES (?, ?, ?, ?, ?)'

        self.db_cursor.execute(
            db_command, (title, text, creation_time, last_modified_time, file_path)
        )

        self.close_db()

    # Read ids
    def read_ids(self):
        self.open_db()

        db_command = 'SELECT id, creation_time FROM data ORDER BY id DESC'
        self.db_cursor.execute(db_command)
        result = self.db_cursor.fetchall()

        if result:
            id_list, creation_time_list = zip(*result)
            id_list = list(id_list)
            creation_time_list = list(creation_time_list)
        else:
            id_list = []
            creation_time_list = []

        self.close_db()

        return id_list, creation_time_list

    # Read a record from id
    def read_record_from_id(self, id_number):
        self.open_db()

        db_command = 'SELECT title, text, creation_time, last_modified_time, file_path FROM data WHERE id = ?'
        self.db_cursor.execute(db_command, (id_number,))
        result = self.db_cursor.fetchall()

        self.close_db()

        record = result[0]

        title = record[0]
        text = record[1]
        creation_time = record[2]
        last_modified_time = record[3]
        file_path = record[4]

        return title, text, creation_time, last_modified_time, file_path

    # Update a record from id
    def update_record_from_id(self, id_number, title, text, last_modified_time, file_path):
        self.open_db()
        db_command = 'UPDATE data SET title = ?, text = ?, last_modified_time = ?, file_path = ? WHERE id = ?'
        self.db_cursor.execute(db_command, (title, text, last_modified_time, file_path, id_number))
        self.close_db()

    # Remove a record from id
    def remove_record_from_id(self, id_number):
        self.open_db()
        self.db_cursor.execute('DELETE FROM data WHERE id = ?', (id_number,))
        self.close_db()

        self.open_db()
        self.db_cursor.execute('VACUUM')
        self.close_db()
