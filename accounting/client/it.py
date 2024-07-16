import sys
from PyQt6.QtWidgets import *
import mysql.connector


class Buh(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Калькулятор страховых взносов")
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout(self)

        # Initialize db connection
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="sas",
                database="buh"
            )
        except mysql.connector.Error as err:
            print("Database connection error:", err)
            sys.exit(1)

        # Текст: Должность
        self.position_label = QLabel("Должность")
        self.layout.addWidget(self.position_label)

        # Combobox для выбора должности из БД
        self.position_combobox = QComboBox()
        self.populate_positions_combobox()
        self.layout.addWidget(self.position_combobox)
        self.position_combobox.currentIndexChanged.connect(self.display_salary)
        self.position_combobox.currentIndexChanged.connect(self.populate_insurance_checkboxes)

        # Вывод зарплаты из БД в зависимости от выбора профессии
        self.salary_label = QLabel("Зарплата:")
        self.layout.addWidget(self.salary_label)
        self.salary_value = QLabel()
        self.layout.addWidget(self.salary_value)

        # Текст: Выплачиваемые страховые взносы
        self.insurance_label = QLabel("Выплачиваемые страховые взносы")
        self.layout.addWidget(self.insurance_label)

        # Checkbox для выбора взносов из БД
        self.insurance_checkboxes_widget = QWidget()
        self.layout.addWidget(self.insurance_checkboxes_widget)
        self.insurance_checkboxes_layout = QVBoxLayout(self.insurance_checkboxes_widget)

        # Общая сумма при выборе должности и взносов
        self.total_amount_label = QLabel("Общая сумма:")
        self.layout.addWidget(self.total_amount_label)
        self.total_amount_value = QLabel()
        self.layout.addWidget(self.total_amount_value)

        # Текст: Тип операции
        self.operation_label = QLabel("Тип операции")
        self.layout.addWidget(self.operation_label)

        # Checkbox для выбора типа операции из БД
        self.operation_combobox = QComboBox()
        self.populate_operation_combobox()
        self.layout.addWidget(self.operation_combobox)

        # Кнопки Рассчитать и Записать
        self.calculate_button = QPushButton("Рассчитать")
        self.layout.addWidget(self.calculate_button)
        self.calculate_button.clicked.connect(self.calculate_total_amount)

        self.save_button = QPushButton("Записать")
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_to_database)

    def populate_positions_combobox(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT p_name FROM positions")
            positions = cursor.fetchall()
            for position in positions:
                self.position_combobox.addItem(position[0])
        except mysql.connector.Error as err:
            print("Database query error:", err)

    def display_salary(self, index):
        try:
            cursor = self.db.cursor()
            position = self.position_combobox.currentText()
            cursor.execute("SELECT p_salary FROM positions WHERE p_name = %s", (position,))
            salary = cursor.fetchone()[0]
            self.salary_value.setText(str(salary))
            cursor.fetchall()  # Ensure all results are fetched
        except mysql.connector.Error as err:
            print("Database query error:", err)

    def populate_insurance_checkboxes(self, index):
        self.clear_layout(self.insurance_checkboxes_layout)
        try:
            cursor = self.db.cursor()
            position = self.position_combobox.currentText()
            cursor.execute("""
                SELECT d.d_name 
                FROM donations_type d
                INNER JOIN position_donations pd ON d.id = pd.id_donat
                INNER JOIN positions p ON pd.id_positions = p.id
                WHERE p.p_name = %s
            """, (position,))
            insurances = cursor.fetchall()
            for insurance in insurances:
                checkbox = QCheckBox(insurance[0])
                self.insurance_checkboxes_layout.addWidget(checkbox)
            cursor.fetchall()  # Ensure all results are fetched
        except mysql.connector.Error as err:
            print("Database query error:", err)

    def populate_operation_combobox(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT op_name FROM operation_type")
            operations = cursor.fetchall()
            for operation in operations:
                self.operation_combobox.addItem(operation[0])
        except mysql.connector.Error as err:
            print("Database query error:", err)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def calculate_total_amount(self):
        try:
            position = self.position_combobox.currentText()
            operation = self.operation_combobox.currentText()

            cursor = self.db.cursor()
            cursor.execute("""
                SELECT calculate_amount(p.id, d.id, o.id) 
                FROM positions p 
                CROSS JOIN donations_type d 
                CROSS JOIN operation_type o 
                WHERE p.p_name = %s AND o.op_name = %s
            """, (position, operation))

            total_amount = cursor.fetchone()[0]
            self.total_amount_value.setText(str(total_amount))
            cursor.fetchall()  # Ensure all results are fetched
        except mysql.connector.Error as err:
            print("Database query error:", err)

    def save_to_database(self):
        try:
            position = self.position_combobox.currentText()
            operation = self.operation_combobox.currentText()

            # Получаем ID должности
            cursor = self.db.cursor()
            cursor.execute("SELECT id FROM positions WHERE p_name = %s", (position,))
            position_id = cursor.fetchone()[0]

            # Получаем ID типа операции
            cursor.execute("SELECT id FROM operation_type WHERE op_name = %s", (operation,))
            operation_id = cursor.fetchone()[0]

            # Получаем ID выбранных страховых взносов
            insurance_ids = []
            for i in range(self.insurance_checkboxes_layout.count()):
                checkbox = self.insurance_checkboxes_layout.itemAt(i).widget()
                if checkbox.isChecked():
                    cursor.execute("SELECT id FROM donations_type WHERE d_name = %s", (checkbox.text(),))
                    insurance_ids.append(cursor.fetchone()[0])

            # Вызываем процедуру и сохраняем результат
            out_total = cursor.callproc("calculate_amount_procedure", (position_id, insurance_ids[0], operation_id, 0))
            total_amount = out_total[3]

            self.db.commit()

            QMessageBox.information(self, "Success",
                                    f"Результат успешно записан в базу данных.\nОбщая сумма: {total_amount}")
        except mysql.connector.Error as err:
            print("Database query error:", err)
            self.db.rollback()


if __name__ == "__main__":
    app = QApplication([])
    window = Buh()
    window.show()
    sys.exit(app.exec())
