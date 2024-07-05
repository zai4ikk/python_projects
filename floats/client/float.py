import sys  # Импортируем модуль sys для управления параметрами и функциями Python
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, \
    QLabel  # Импортируем необходимые классы из PyQt6
import mysql.connector  # Импортируем mysql.connector для работы с базой данных MySQL


class MyApp(QWidget):  # Создаём класс MyApp, наследующийся от QWidget
    def __init__(self):  # Конструктор класса
        super().__init__()  # Инициализируем родительский класс QWidget

        # Устанавливаем заголовок окна
        self.setWindowTitle('Квартиры')

        # Создаём вертикальный layout для размещения виджетов
        self.layout = QVBoxLayout()

        # Создаём QLabel для отображения текста и добавляем его в layout
        self.label = QLabel('Нажмите кнопку для получения количества квартир(от 40 кв.м и цена от 2 млн до 2.5 млн)', self)
        self.layout.addWidget(self.label)

        # Создаём QPushButton и подключаем его к методу fetch_data
        self.button = QPushButton('Получить данные', self)
        self.button.clicked.connect(self.fetch_data)
        self.layout.addWidget(self.button)

        # Устанавливаем layout для главного окна
        self.setLayout(self.layout)

    def fetch_data(self):  # Метод для получения данных из базы данных
        # Подключаемся к базе данных MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sas",
            database="floatv"
        )

        cursor = connection.cursor()  # Создаём курсор для выполнения SQL-запросов
        cursor.execute("SELECT * FROM v1")  # Выполняем SQL-запрос для получения данных из представления v1
        result = cursor.fetchall()  # Получаем все строки результата запроса

        display_text = ''  # Инициализируем переменную для накопления текста
        # Обрабатываем каждую строку результата и добавляем её в display_text
        for row in result:
            display_text += f'Количество записей: {row[0]}, День: {row[1]}\n'

        self.label.setText(display_text)  # Устанавливаем текст метки с данными из базы данных

        cursor.close()  # Закрываем курсор
        connection.close()  # Закрываем подключение к базе данных


if __name__ == '__main__':  # Проверяем, запущен ли скрипт напрямую
    app = QApplication(sys.argv)  # Создаём экземпляр QApplication
    ex = MyApp()  # Создаём экземпляр нашего приложения
    ex.show()  # Показываем главное окно приложения
    sys.exit(app.exec())  # Запускаем основной цикл обработки событий
