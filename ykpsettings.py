from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel)


class Settings(QWidget):
    def __init__(self):
        super(Settings, self).__init__()

        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        app_name_label = QLabel()
        app_version_label = QLabel()
        app_description_label = QLabel()
        app_license_label = QLabel()
        qt_description_label = QLabel()

        self.setWindowTitle("About YKPen")
        self.setGeometry(400, 400, 350, 300)
        self.setWindowIcon(QIcon("icons/logo.png"))

        # Dark theme -- begin
        self.setStyleSheet("background: black; color: white")
        # Dark theme -- end

        self.setLayout(main_layout)

        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        main_layout.addLayout(top_layout)

        top_layout.addWidget(app_name_label)
        top_layout.addWidget(app_version_label)

        main_layout.addWidget(app_description_label)
        main_layout.addWidget(app_license_label)
        main_layout.addWidget(qt_description_label)

        app_name_font = QFont()
        app_name_font.setPointSize(30)
        app_name_label.setFont(app_name_font)
        app_name_label.setContentsMargins(15, 30, 0, 10)
        app_name_label.setText("YKPen")

        app_version_label.setContentsMargins(15, 50, 0, 10)
        app_version_label.setText("1.0.0")

        app_description_label.setContentsMargins(15, 0, 0, 10)
        app_description_label.setText("YKPen is a note app.\n"
                                      "You may save text as a file, or save it to database.")

        app_license_label.setContentsMargins(15, 0, 0, 10)
        app_license_label.setText("YKPen is released as free software under GNU\n"
                                  "General Public License version 3.")
        qt_description_label.setContentsMargins(15, 0, 0, 10)
        qt_description_label.setText("YKPen uses Qt libraries dynamically under GNU\n"
                                     "Lesser General Public License version 3.\n"
                                     "There is no modification in Qt source code.")

    def changeEvent(self, event):
        if not self.isActiveWindow():
            self.close()
