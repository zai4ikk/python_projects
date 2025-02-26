from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QPixmap
import mysql.connector
import random
import string
import sys
import os


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)

        self.btn_login.clicked.connect(self.authenticate)
        self.checkBox_show_password.stateChanged.connect(self.toggle_password)
        self.btn_refresh_captcha.clicked.connect(self.generate_captcha)

        self.generate_captcha()

    def generate_captcha(self):
        """Генерация случайного текста для CAPTCHA"""
        captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        self.label_captcha.setText(captcha_text)

    def toggle_password(self):
        """Переключение отображения пароля"""
        if self.checkBox_show_password.isChecked():
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def authenticate(self):
        """Аутентификация пользователя"""
        login = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        captcha_input = self.lineEdit_captcha.text()
        captcha_real = self.label_captcha.text()

        if captcha_input != captcha_real:
            self.label_error.setText("Неверная CAPTCHA!")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="sas",
                database="lab_management",
                auth_plugin="mysql_native_password"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT full_name, role FROM users WHERE login=%s AND password=%s", (login, password))
            user = cursor.fetchone()

            if user:
                full_name, role = user
                QMessageBox.information(self, "Успешный вход", f"Добро пожаловать, {full_name} ({role})!")

                # Сопоставление ролей из БД с изображениями
                role_to_photo = {
                    "admin": "admin.png",
                    "lab_worker": "lab1.png",
                    "researcher": "lab2.png",
                    "accountant": "buh.png"
                }

                role_lower = role.lower().strip()  # Приводим роль к нижнему регистру и убираем пробелы
                photo_file = role_to_photo.get(role_lower, "default.png")  # Если роль неизвестна, подставляем default.png

                # Полный путь к изображению
                photo_path = os.path.join(os.getcwd(), photo_file)
                print(f"Попытка загрузки фото: {photo_path}")  # Для отладки

                # Проверка существования файла
                if os.path.exists(photo_path):
                    pixmap = QPixmap(photo_path)
                    if pixmap.isNull():
                        print("Ошибка: QPixmap не загрузил изображение.")
                    else:
                        self.label_photo.setPixmap(pixmap)
                        self.label_photo.setScaledContents(True)
                        print("Фото успешно загружено!")
                else:
                    print(f"Ошибка: Файл {photo_path} не найден!")

            else:
                self.label_error.setText("Неверный логин или пароль!")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка", f"Ошибка подключения к базе данных: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
