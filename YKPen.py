import sys
from PySide6.QtCore import Qt, QStandardPaths, QFile, QFileInfo, QTextStream, QIODevice, QDir, QDateTime, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QGridLayout,
                               QLabel, QLineEdit, QTextEdit, QComboBox, QMessageBox)

from ykphandler import Commands
from ykpdatabase import Database
from ykpsettings import Settings


class YKPen(QWidget):
    def __init__(self):
        super(YKPen, self).__init__()

        self.commands = Commands()
        self.database = Database()
        self.settings_panel = Settings()

        self.main_layout = QVBoxLayout()

        self.top_layout = QHBoxLayout()
        self.top_left_layout = QHBoxLayout()
        self.file_operations_layout = QHBoxLayout()
        self.database_operations_layout = QHBoxLayout()
        self.settings_layout = QHBoxLayout()

        self.title_layout = QHBoxLayout()
        self.editor_layout = QGridLayout()

        self.bottom_layout = QHBoxLayout()
        self.time_layout = QHBoxLayout()
        self.file_path_layout = QHBoxLayout()

        self.file_operations_label = QLabel()
        self.open_button = QPushButton()
        self.save_file_button = QPushButton()

        self.database_operations_label = QLabel()
        self.save_data_button = QPushButton()
        self.remove_data_button = QPushButton()
        self.backup_database_button = QPushButton()
        self.replace_database_button = QPushButton()

        self.settings_button = QPushButton()

        self.text_list_combobox = QComboBox()

        self.title_entry = QLineEdit()
        self.editor = QTextEdit()

        self.creation_time_label = QLabel()
        self.last_modified_time_label = QLabel()

        self.file_path_entry = QLineEdit()

        self.open_file_status = False
        self.file_text_changes_status = False
        self.new_text_changes_status = False

        screen = app.primaryScreen()
        screen_width = screen.availableSize().width()
        screen_height = screen.availableSize().height()

        if screen_height < 1080:
            self.setGeometry(int((screen_width - 1080) / 2), int((screen_height - 600) / 2), 1080, 600)
        else:
            self.setGeometry(int((screen_width - 1080) / 2), int((screen_height - 900) / 2), 1080, 900)

        self.setLayout(self.main_layout)

        self.setWindowTitle('YKPen')
        self.setWindowIcon(QIcon("icons/logo.png"))

        # Dark theme -- begin
        self.setStyleSheet("background: black; color: white")

        dark_theme_style = 'QPushButton {border: 1px solid rgb(100, 100, 100); border-radius: 5px; color: white} ' \
                           'QPushButton::hover {border: 1px solid rgb(100, 100, 100); border-radius: 5px; ' \
                           'background: rgb(80, 80, 80); color: white} '

        self.open_button.setStyleSheet(dark_theme_style)
        self.save_file_button.setStyleSheet(dark_theme_style)
        self.save_data_button.setStyleSheet(dark_theme_style)
        self.remove_data_button.setStyleSheet(dark_theme_style)
        self.backup_database_button.setStyleSheet(dark_theme_style)
        self.replace_database_button.setStyleSheet(dark_theme_style)
        self.settings_button.setStyleSheet(dark_theme_style)

        self.text_list_combobox.setStyleSheet(
            'QComboBox {border: 1px solid rgb(100, 100, 100); border-radius: 2px; color: white} '
            'QComboBox QAbstractItemView {border: 1px solid rgb(100, 100, 100); border-radius: 5px; color: white} '
            'QComboBox QAbstractItemView::item {height: 26px} '
            'QComboBox QAbstractItemView::item::selected {background: rgb(50, 50, 50)}')

        self.title_entry.setStyleSheet('border:1px solid rgb(100, 100, 100); border-radius: 2px; '
                                       'background: rgb(30, 30, 30); color: white; font-size: 11pt')
        self.editor.setStyleSheet('border:1px solid rgb(60, 60, 60); border-radius: 2px; background: rgb(30, 30, 30); '
                                  'color: white; font-size: 11pt')
        self.file_path_entry.setStyleSheet('border:1px solid rgb(60, 60, 60); border-radius: 2px; background: black; '
                                           'color: white')
        # Dark theme -- end

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setContentsMargins(10, 5, 10, 0)
        self.title_layout.setContentsMargins(10, 0, 10, 0)
        self.editor_layout.setContentsMargins(2, 0, 2, 0)
        self.bottom_layout.setContentsMargins(10, 0, 10, 5)

        self.main_layout.addLayout(self.top_layout)

        self.top_layout.addLayout(self.top_left_layout)
        self.top_left_layout.addLayout(self.file_operations_layout)
        self.top_left_layout.addLayout(self.database_operations_layout)
        self.top_layout.addLayout(self.settings_layout)

        self.top_left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settings_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(self.title_layout)
        self.main_layout.addLayout(self.editor_layout)
        self.main_layout.addLayout(self.bottom_layout)

        self.file_operations_label.setText("File")

        self.open_button.setIcon(QIcon("icons/open-a-file.png"))
        self.open_button.setIconSize(QSize(20, 20))
        self.open_button.setToolTip("Open a file")
        self.open_button.setFixedSize(30, 30)

        self.save_file_button.setIcon(QIcon("icons/save-as-a-file.png"))
        self.save_file_button.setIconSize(QSize(20, 20))
        self.save_file_button.setToolTip("Save as a file")
        self.save_file_button.setFixedSize(30, 30)

        self.file_operations_layout.addWidget(self.file_operations_label)
        self.file_operations_layout.addWidget(self.open_button)
        self.file_operations_layout.addWidget(self.save_file_button)

        self.database_operations_label.setText("Database")

        self.save_data_button.setIcon(QIcon("icons/save-to-database.png"))
        self.save_data_button.setIconSize(QSize(20, 20))
        self.save_data_button.setToolTip("Save to database")
        self.save_data_button.setFixedSize(30, 30)

        self.remove_data_button.setIcon(QIcon("icons/remove-from-database.png"))
        self.remove_data_button.setIconSize(QSize(20, 20))
        self.remove_data_button.setToolTip("Remove from database")
        self.remove_data_button.setFixedSize(30, 30)

        self.backup_database_button.setIcon(QIcon("icons/backup-database.png"))
        self.backup_database_button.setIconSize(QSize(20, 20))
        self.backup_database_button.setToolTip("Backup database")
        self.backup_database_button.setFixedSize(30, 30)

        self.replace_database_button.setIcon(QIcon("icons/replace-database.png"))
        self.replace_database_button.setIconSize(QSize(20, 20))
        self.replace_database_button.setToolTip("Replace database")
        self.replace_database_button.setFixedSize(30, 30)

        self.database_operations_layout.addWidget(self.database_operations_label)
        self.database_operations_layout.addWidget(self.save_data_button)
        self.database_operations_layout.addWidget(self.remove_data_button)
        self.database_operations_layout.addWidget(self.backup_database_button)
        self.database_operations_layout.addWidget(self.replace_database_button)

        self.settings_button.setIcon(QIcon("icons/settings.png"))
        self.settings_button.setIconSize(QSize(20, 20))
        self.settings_button.setToolTip("About YKPen")
        self.settings_button.setFixedSize(30, 30)

        self.settings_layout.addWidget(self.settings_button)

        self.text_list = self.read_text_list()
        self.text_list_combobox.addItems(self.text_list)
        self.text_list_combobox.setEditable(False)
        self.text_list_combobox.setFixedSize(145, 30)
        self.text_list_combobox.setCurrentText("New")

        self.title_entry.setFixedSize(750, 30)

        self.title_layout.setAlignment(Qt.AlignLeft)
        self.title_layout.addWidget(self.text_list_combobox)
        self.title_layout.addWidget(self.title_entry)

        self.editor_layout.addWidget(self.editor)

        self.time_layout.setAlignment(Qt.AlignLeft)
        self.file_path_layout.setAlignment(Qt.AlignRight)

        self.creation_time_label.setFixedWidth(250)
        self.last_modified_time_label.setFixedWidth(250)

        self.file_path_entry.setFixedSize(500, 25)
        self.file_path_entry.setReadOnly(True)

        self.time_layout.addWidget(self.creation_time_label)
        self.time_layout.addWidget(self.last_modified_time_label)
        self.file_path_layout.addWidget(self.file_path_entry)
        self.bottom_layout.addLayout(self.time_layout)
        self.bottom_layout.addLayout(self.file_path_layout)

        self.open_button.clicked.connect(self.open_file)
        self.save_file_button.clicked.connect(self.save_file)
        self.save_data_button.clicked.connect(self.save_data)
        self.remove_data_button.clicked.connect(self.remove_data)

        self.backup_database_button.clicked.connect(self.backup_database)
        self.replace_database_button.clicked.connect(self.replace_database)

        self.settings_button.clicked.connect(self.open_settings)

        self.text_list_combobox.activated.connect(self.load_database)

        self.title_entry.textChanged.connect(self.auto_save_data)
        self.editor.textChanged.connect(self.auto_save_data)
        self.file_path_entry.textChanged.connect(self.auto_save_data)

    def open_file(self):
        default_folder_path = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
        get_info = QFileDialog.getOpenFileName(self, 'Please choose a file', default_folder_path,
                                               'Text file (*.txt);; HTML file (*.htm);; HTML file (*.html)')

        file_path = get_info[0]
        if file_path != "":
            self.text_list_combobox.setCurrentText("File")

            file = QFile(file_path)
            file.open(QIODevice.ReadOnly)
            file_text = QTextStream(file)
            self.editor.setPlainText(file_text.readAll())
            file.close()

            file_info = QFileInfo(file_path)
            title = file_info.completeBaseName()
            creation_time = file_info.birthTime().toString("yyyy-MM-dd hh:mm:ss")
            last_modified_time = file_info.lastModified().toString("yyyy-MM-dd hh:mm:ss")

            self.title_entry.setText(title)
            self.creation_time_label.setText('Created at ' + creation_time)
            if last_modified_time:
                self.last_modified_time_label.setText('Last modified at ' + last_modified_time)
            self.file_path_entry.setText(file_path)

            self.open_file_status = True
            self.file_text_changes_status = False

    def read_text_list(self):
        _, creation_time_list = self.database.read_ids()
        text_list = creation_time_list
        text_list.insert(0, "New")
        text_list.insert(1, "File")

        return text_list

    def creation_time_to_id(self, creation_time):
        id_list, creation_time_list = self.database.read_ids()

        i = creation_time_list.index(creation_time)

        id_number = id_list[i]

        return id_number

    def load_database(self):
        text_option = self.text_list_combobox.currentText()
        text = self.editor.toPlainText()
        current_file_path = self.file_path_entry.text()

        if self.new_text_changes_status:
            self.text_list_combobox.setCurrentText('New')

            exit_box = QMessageBox()
            exit_box.setText("The text is not saved.\nDo you want to save it to database?")
            save_button = exit_box.addButton(QMessageBox.Save)
            discard_button = exit_box.addButton(QMessageBox.Discard)
            cancel_button = exit_box.addButton(QMessageBox.Cancel)
            exit_box.exec()
            if exit_box.clickedButton() == save_button:
                self.save_data()
                self.text_list_combobox.setCurrentText(text_option)

            if exit_box.clickedButton() == discard_button:
                self.new_text_changes_status = False
                self.text_list_combobox.setCurrentText(text_option)

            if exit_box.clickedButton() == cancel_button:
                return

        creation_time = self.creation_time_label.text()
        if text_option == 'File' and text and not creation_time:
            self.file_text_changes_status = True

        if self.open_file_status and not QFile.exists(current_file_path):
            self.file_text_changes_status = True

        if self.file_text_changes_status and text_option != 'File':
            self.text_list_combobox.setCurrentText("File")

            exit_box = QMessageBox()

            if current_file_path == "" or not QFile.exists(current_file_path):
                exit_box.setText("The text is not saved.\nDo you want to save it as a file?")
            else:
                exit_box.setText("The file's text has been modified.\nDo you want to save it?")

            save_button = exit_box.addButton(QMessageBox.Save)
            discard_button = exit_box.addButton(QMessageBox.Discard)
            cancel_button = exit_box.addButton(QMessageBox.Cancel)
            exit_box.exec()
            if exit_box.clickedButton() == save_button:
                self.save_file()
                if self.file_text_changes_status:
                    return
                else:
                    self.file_text_changes_status = False
                    self.text_list_combobox.setCurrentText(text_option)

            if exit_box.clickedButton() == discard_button:
                self.file_text_changes_status = False
                self.text_list_combobox.setCurrentText(text_option)

            if exit_box.clickedButton() == cancel_button:
                return

        if text_option == "New" and not self.new_text_changes_status and not self.file_text_changes_status:
            self.clear_all_contents()
            self.open_file_status = False

        if text_option != "New" and text_option != "File":
            id_number = self.creation_time_to_id(text_option)
            title, text, creation_time, last_modified_time, file_path = self.database.read_record_from_id(id_number)

            self.title_entry.setText(title)
            self.editor.setPlainText(text)
            self.creation_time_label.setText('Created at ' + creation_time)
            if last_modified_time:
                self.last_modified_time_label.setText('Last modified at ' + last_modified_time)
            self.file_path_entry.setText(file_path)

            self.open_file_status = False

    def save_file(self):
        text_option = self.text_list_combobox.currentText()
        current_file_path = self.file_path_entry.text()
        if current_file_path != "":
            file = QFile(current_file_path)
            file.open(QIODevice.WriteOnly | QIODevice.Truncate)
            file_text = QTextStream(file)
            file_text << self.editor.toPlainText()
            file.close()

            if text_option == 'New':
                self.new_text_changes_status = False
            if text_option == 'File':
                self.file_text_changes_status = False

            file_info = QFileInfo(current_file_path)
            creation_time = file_info.birthTime().toString("yyyy-MM-dd hh:mm:ss")
            last_modified_time = file_info.lastModified().toString("yyyy-MM-dd hh:mm:ss")

            self.creation_time_label.setText('Created at ' + creation_time)
            if last_modified_time:
                self.last_modified_time_label.setText('Last modified at ' + last_modified_time)

            return

        default_folder_path = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
        default_folder = QDir(default_folder_path)
        title = self.title_entry.text()
        default_file_path = default_folder.absoluteFilePath(title)

        get_info = QFileDialog.getSaveFileName(self, 'Save as', default_file_path,
                                               'Text file (*.txt);; HTML file (*.htm);; HTML file (*.html);; '
                                               'All files (*.*)')

        file_path = get_info[0]
        if file_path != '':
            file = QFile(file_path)
            file.open(QIODevice.WriteOnly | QIODevice.Truncate)
            file_text = QTextStream(file)
            file_text << self.editor.toPlainText()
            file.close()

            self.file_path_entry.setText(file_path)

            if text_option == 'New':
                self.new_text_changes_status = False
            if text_option == 'File':
                self.file_text_changes_status = False

            file_info = QFileInfo(file_path)
            creation_time = file_info.birthTime().toString("yyyy-MM-dd hh:mm:ss")
            last_modified_time = file_info.lastModified().toString("yyyy-MM-dd hh:mm:ss")
            self.creation_time_label.setText('Created at ' + creation_time)
            if last_modified_time:
                self.last_modified_time_label.setText('Last modified at ' + last_modified_time)

    def save_data(self):
        text_option = self.text_list_combobox.currentText()

        if text_option != "New" and text_option != "File":
            self.update_data()
            return

        title = self.title_entry.text()
        text = self.editor.toPlainText()

        if not title and not text:
            return

        current_time = QDateTime.currentDateTime()
        creation_time = current_time.toString("yyyy-MM-dd hh:mm:ss")
        last_modified_time = ""
        file_path = self.file_path_entry.text()

        self.database.insert_record(title, text, creation_time, last_modified_time, file_path)

        self.new_text_changes_status = False

        text_list = self.read_text_list()

        self.text_list_combobox.clear()
        self.text_list_combobox.addItems(text_list)
        self.text_list_combobox.setEditable(False)
        self.text_list_combobox.setCurrentText(creation_time)
        self.creation_time_label.setText('Created at ' + creation_time)

    def update_data(self):
        text_option = self.text_list_combobox.currentText()
        id_number = self.creation_time_to_id(text_option)
        title = self.title_entry.text()
        text = self.editor.toPlainText()
        current_time = QDateTime.currentDateTime()
        last_modified_time = current_time.toString("yyyy-MM-dd hh:mm:ss")
        file_path = self.file_path_entry.text()

        self.last_modified_time_label.setText('Last modified at ' + last_modified_time)

        self.database.update_record_from_id(id_number, title, text, last_modified_time, file_path)

    def auto_save_data(self):
        title = self.title_entry.text()
        text = self.editor.toPlainText()

        text_option = self.text_list_combobox.currentText()

        if text_option == "File":
            if text:
                self.file_text_changes_status = True

            current_file_path = self.file_path_entry.text()
            if not text and not current_file_path:
                self.file_text_changes_status = False

            return

        if text_option == "New" and not text:
            self.new_text_changes_status = False

        if text_option == "New" and text:
            self.new_text_changes_status = True

        if text_option == "New" and title and text:
            self.save_data()

        if text_option != "New" and text_option != 'File':
            self.update_data()

    def remove_data(self):
        text_option = self.text_list_combobox.currentText()

        if text_option != "New" and text_option != "File":
            id_number = self.creation_time_to_id(text_option)
            self.database.remove_record_from_id(id_number)

            text_list = self.read_text_list()
            self.text_list_combobox.clear()
            self.text_list_combobox.addItems(text_list)
            self.text_list_combobox.setEditable(False)
            self.text_list_combobox.setCurrentText("New")

            self.clear_all_contents()

    def backup_database(self):
        default_folder_path = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
        default_folder = QDir(default_folder_path)
        backup_db_name = "YKPen_database_backup"
        default_file_path = default_folder.absoluteFilePath(backup_db_name)

        get_info = QFileDialog.getSaveFileName(self, 'Save as', default_file_path, 'SQLite database (*.db)')

        file_path = get_info[0]
        if file_path != "":
            if QFile.exists(file_path):
                QFile.remove(file_path)

            database_path = self.commands.read_database_path()
            QFile.copy(database_path, file_path)

    def replace_database(self):
        default_folder_path = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
        get_info = QFileDialog.getOpenFileName(self, 'Please choose a file', default_folder_path,
                                               'SQLite database (*.db)')

        file_path = get_info[0]
        if file_path != "":
            exit_box = QMessageBox()
            exit_box.setText("Are you sure you want to replace database? Data in default database will be lost.")
            yes_button = exit_box.addButton(QMessageBox.Yes)
            no_button = exit_box.addButton(QMessageBox.No)
            exit_box.exec()
            if exit_box.clickedButton() == yes_button:
                database_path = self.commands.read_database_path()
                QFile.remove(database_path)
                QFile.copy(file_path, database_path)

                text_list = self.read_text_list()
                self.text_list_combobox.clear()
                self.text_list_combobox.addItems(text_list)
                self.text_list_combobox.setEditable(False)

    def open_settings(self):
        x = self.geometry().x()
        y = self.geometry().y()
        width = self.geometry().width()
        self.settings_panel.move(x + width - 550, y + 50)
        self.settings_panel.show()

    def clear_all_contents(self):
        self.title_entry.setText("")
        self.editor.setPlainText("")
        self.creation_time_label.setText("")
        self.last_modified_time_label.setText("")
        self.file_path_entry.setText("")

    def handle_new_text_changes(self, event):
        exit_box = QMessageBox()
        exit_box.setText("The text is not saved.\nDo you want to save it to database?")
        save_button = exit_box.addButton(QMessageBox.Save)
        discard_button = exit_box.addButton(QMessageBox.Discard)
        cancel_button = exit_box.addButton(QMessageBox.Cancel)
        exit_box.exec()
        if exit_box.clickedButton() == save_button:
            self.save_data()
            if event:
                event.accept()
        if exit_box.clickedButton() == discard_button:
            if event:
                event.accept()
        if exit_box.clickedButton() == cancel_button:
            if event:
                event.ignore()

    def handle_file_text_changes(self, event, status):
        exit_box = QMessageBox()
        if status == 'not saved':
            exit_box.setText("The text is not saved.\nDo you want to save it as a file?")
        if status == 'modified':
            exit_box.setText("The file's text has been modified.\nDo you want to save it?")
        save_button = exit_box.addButton(QMessageBox.Save)
        discard_button = exit_box.addButton(QMessageBox.Discard)
        cancel_button = exit_box.addButton(QMessageBox.Cancel)
        exit_box.exec()
        if exit_box.clickedButton() == save_button:
            self.save_file()
            if not self.file_text_changes_status:
                event.accept()
            else:
                event.ignore()
        if exit_box.clickedButton() == discard_button:
            event.accept()
        if exit_box.clickedButton() == cancel_button:
            event.ignore()

    def closeEvent(self, event):
        text_option = self.text_list_combobox.currentText()

        if text_option == "New" and self.new_text_changes_status:
            self.handle_new_text_changes(event)
            return

        text = self.editor.toPlainText()
        creation_time = self.creation_time_label.text()
        if text_option == "File" and text and not creation_time:
            self.file_text_changes_status = True
            self.handle_file_text_changes(event, 'not saved')
            return

        if text_option == "File" and text and self.file_text_changes_status:
            self.handle_file_text_changes(event, 'modified')


if __name__ == '__main__':
    app = QApplication([])
    main_window = YKPen()
    main_window.show()
    sys.exit(app.exec())
