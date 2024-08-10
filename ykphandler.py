import os
import sys
import hashlib
import shutil
import random
import string
import subprocess

from PySide6.QtCore import Qt, QFile, QStandardPaths, QDir

from ykpdatabase import BasicConfig, Database


class Commands:
    def __init__(self):
        super(Commands, self).__init__()
        self.basic_config = BasicConfig()
        self.database = Database()

    def read_database_path(self):
        database_path = self.database.read_db_path()
        return database_path
