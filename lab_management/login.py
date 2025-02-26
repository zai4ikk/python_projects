# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(387, 383)
        MainWindow.setStyleSheet("background-color: rgb(219, 239, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_photo = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_photo.setGeometry(QtCore.QRect(10, 10, 111, 81))
        self.label_photo.setText("")
        self.label_photo.setObjectName("label_photo")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(210, 140, 151, 161))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_captcha = QtWidgets.QLabel(parent=self.widget)
        self.label_captcha.setText("")
        self.label_captcha.setObjectName("label_captcha")
        self.verticalLayout_3.addWidget(self.label_captcha)
        self.label_3 = QtWidgets.QLabel(parent=self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.lineEdit_captcha = QtWidgets.QLineEdit(parent=self.widget)
        self.lineEdit_captcha.setStyleSheet("background-color: rgb(254, 255, 172);")
        self.lineEdit_captcha.setObjectName("lineEdit_captcha")
        self.verticalLayout_3.addWidget(self.lineEdit_captcha)
        self.btn_refresh_captcha = QtWidgets.QPushButton(parent=self.widget)
        self.btn_refresh_captcha.setStyleSheet("background-color: rgb(255, 193, 220);")
        self.btn_refresh_captcha.setObjectName("btn_refresh_captcha")
        self.verticalLayout_3.addWidget(self.btn_refresh_captcha)
        self.widget1 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(10, 100, 181, 201))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.widget1)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit_login = QtWidgets.QLineEdit(parent=self.widget1)
        self.lineEdit_login.setStyleSheet("background-color: rgb(254, 255, 172);")
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.verticalLayout.addWidget(self.lineEdit_login)
        self.label_2 = QtWidgets.QLabel(parent=self.widget1)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit_password = QtWidgets.QLineEdit(parent=self.widget1)
        self.lineEdit_password.setStyleSheet("background-color: rgb(254, 255, 172);")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.verticalLayout.addWidget(self.lineEdit_password)
        self.btn_login = QtWidgets.QPushButton(parent=self.widget1)
        self.btn_login.setStyleSheet("background-color: rgb(255, 193, 220);")
        self.btn_login.setObjectName("btn_login")
        self.verticalLayout.addWidget(self.btn_login)
        self.checkBox_show_password = QtWidgets.QCheckBox(parent=self.widget1)
        self.checkBox_show_password.setObjectName("checkBox_show_password")
        self.verticalLayout.addWidget(self.checkBox_show_password)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label_error = QtWidgets.QLabel(parent=self.widget1)
        self.label_error.setText("")
        self.label_error.setObjectName("label_error")
        self.verticalLayout_2.addWidget(self.label_error)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 387, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Введите капчу"))
        self.btn_refresh_captcha.setText(_translate("MainWindow", "Обновить"))
        self.label.setText(_translate("MainWindow", "Введите логин:"))
        self.label_2.setText(_translate("MainWindow", "Введите пароль:"))
        self.btn_login.setText(_translate("MainWindow", "Войти"))
        self.checkBox_show_password.setText(_translate("MainWindow", "Посмотреть пароль"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
