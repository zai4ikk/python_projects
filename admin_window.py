from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QPixmap, QIcon
import mysql.connector
import pandas as pd
import os
import sys


class AdminWindow(QtWidgets.QMainWindow):  # Исправлено
    def __init__(self, user_id, full_name):
        super().__init__()
        uic.loadUi("admin.ui", self)
        self.setWindowIcon(QIcon("logo.png"))
        self.user_id = user_id
        self.full_name = full_name
        self.connection = self.connect_db()

        self.label_name.setText(self.full_name)
        self.load_photo()

        self.pushButton_logi.clicked.connect(self.load_analyzers)
        self.pushButton.clicked.connect(self.logout)
        self.show()

    def connect_db(self):
        """Подключение к базе данных"""
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="sas",
                database="lab_management",
                auth_plugin="mysql_native_password"
            )
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка", f"Ошибка подключения к БД: {err}")
            return None

    def load_photo(self):
        """Загрузка фото исследователя"""
        photo_path = os.path.join(os.getcwd(), "admin.png")
        if os.path.exists(photo_path):
            pixmap = QPixmap(photo_path)
            self.label_photo.setPixmap(pixmap)
            self.label_photo.setScaledContents(True)

    #def load_analyzers(self):

    def logout(self):
        """Выход и открытие окна входа"""
        if self.connection:
            self.connection.close()
        self.close()
        from session1 import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
