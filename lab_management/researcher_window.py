from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QPixmap
import mysql.connector
import pandas as pd
import os
import sys

class LabWorkerWindow(QtWidgets.QMainWindow):
    def __init__(self, user_id, full_name):
        super().__init__()
        uic.loadUi("lab1.ui", self)
        self.setWindowIcon(QIcon("logo.png"))
        self.user_id = user_id
        self.full_name = full_name
        self.connection = self.connect_db()

        self.label_name.setText(self.full_name)
        self.load_photo()

        self.pushButton_bio.clicked.connect(self.load_analyzers)
        self.pushButton_otchet.clicked.connect(self.export_to_excel)
        self.pushButton.clicked.connect(self.logout)

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
        photo_path = os.path.join(os.getcwd(), "lab2.png")
        if os.path.exists(photo_path):
            pixmap = QPixmap(photo_path)
            self.label_photo.setPixmap(pixmap)
            self.label_photo.setScaledContents(True)

    def load_analyzers(self):
        """Загрузка анализаторов, на которых работал исследователь"""
        if not self.connection:
            return
        try:
            cursor = self.connection.cursor()
            cursor.callproc("p1", (self.user_id,))

            self.tableWidget.setRowCount(0)
            for result in cursor.stored_results():
                data = result.fetchall()
                self.tableWidget.setRowCount(len(data))
                self.tableWidget.setColumnCount(3)
                self.tableWidget.setHorizontalHeaderLabels(["Название", "Стоимость", "Анализатор"])

                for row_idx, row_data in enumerate(data):
                    for col_idx, col_data in enumerate(row_data):
                        self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            cursor.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка", f"Ошибка выполнения запроса: {err}")

    def export_to_excel(self):
        """Экспорт данных в Excel"""
        if not self.connection:
            QMessageBox.critical(self, "Ошибка", "Отсутствует подключение к базе данных.")
            return
        try:
            cursor = self.connection.cursor()
            cursor.callproc("p1", (self.user_id,))

            for result in cursor.stored_results():
                data = result.fetchall()
                df = pd.DataFrame(data, columns=["Название", "Стоимость", "Анализатор"])

                file_path = os.path.join(os.getcwd(), "lab_report.xlsx")
                df.to_excel(file_path, index=False)

                QMessageBox.information(self, "Успех", f"Отчет сохранен: {file_path}")
                os.startfile(file_path)
            cursor.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка", f"Ошибка запроса к БД: {err}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка экспорта: {e}")

    def logout(self):
        """Выход и открытие окна входа"""
        if self.connection:
            self.connection.close()
        self.close()
        from session1 import LoginWindow  # ✅ ОТЛОЖЕННЫЙ ИМПОРТ
        self.login_window = LoginWindow()
        self.login_window.show()
