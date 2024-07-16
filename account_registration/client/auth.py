import sys
import hashlib
import mysql.connector
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class LoginRegistrationForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Авторизация")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.login_label = QLabel("Логин:")
        self.login_edit = QLineEdit()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_edit)

        self.password_label = QLabel("Пароль:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.message_label = QLabel()
        layout.addWidget(self.message_label)

        self.setLayout(layout)

        # Подключение к базе данных
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sas",
            database="aut"
        )

    def login(self):
        cursor = self.db.cursor()
        query = "SELECT * FROM `users` WHERE `username` = %s"
        cursor.execute(query, (self.login_edit.text(),))
        user = cursor.fetchone()

        if user:
            password_hash = hashlib.sha1((self.password_edit.text() + user[3]).encode()).hexdigest()
            if password_hash == user[2]:
                self.message_label.setText(f"Добро пожаловать, {user[1]}")
            else:
                self.message_label.setText("Неверно введен пароль")
        else:
            self.message_label.setText("Пользователь не найден")

        cursor.close()

    def register(self):
        cursor = self.db.cursor()
        password = self.password_edit.text()
        is_valid_password = self.check_password_requirements(password)

        if not is_valid_password:
            self.message_label.setText("Введите пароль, удовлетворяющий требованиям...")
            return

        try:
            # Добавлены пустые email и phone в вызов процедуры
            cursor.callproc('AddUser', (self.login_edit.text(), password, '', '', ''))
            self.db.commit()
            result = cursor.fetchone()
            if result:
                self.message_label.setText(result[0])
        except mysql.connector.Error as err:
            self.message_label.setText(str(err))

        cursor.close()

    def check_password_requirements(self, password):
        return bool(password and len(password) > 8 and any(char.isdigit() for char in password))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginRegistrationForm()
    window.show()
    sys.exit(app.exec())

