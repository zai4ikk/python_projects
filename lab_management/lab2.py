# Form implementation generated from reading ui file 'lab2.ui'
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
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 320, 75, 24))
        self.pushButton.setStyleSheet("background-color: rgb(255, 193, 220)")
        self.pushButton.setObjectName("pushButton")
        self.splitter = QtWidgets.QSplitter(parent=self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(10, 10, 341, 81))
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label_photo = QtWidgets.QLabel(parent=self.splitter)
        self.label_photo.setText("")
        self.label_photo.setObjectName("label_photo")
        self.layoutWidget = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_name = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_name.setText("")
        self.label_name.setObjectName("label_name")
        self.verticalLayout.addWidget(self.label_name)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 290, 75, 24))
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 193, 220)")
        self.pushButton_2.setObjectName("pushButton_2")
        self.splitter_2 = QtWidgets.QSplitter(parent=self.centralwidget)
        self.splitter_2.setGeometry(QtCore.QRect(10, 130, 351, 141))
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.widget = QtWidgets.QWidget(parent=self.splitter_2)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(parent=self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(parent=self.widget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(parent=self.widget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(parent=self.widget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.widget1 = QtWidgets.QWidget(parent=self.splitter_2)
        self.widget1.setObjectName("widget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.widget1)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_3.addWidget(self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.widget1)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_3.addWidget(self.lineEdit_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.widget1)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_3.addWidget(self.lineEdit_3)
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.widget1)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout_3.addWidget(self.lineEdit_4)
        self.lineEdit_5 = QtWidgets.QLineEdit(parent=self.widget1)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.verticalLayout_3.addWidget(self.lineEdit_5)
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
        self.pushButton.setText(_translate("MainWindow", "Выйти"))
        self.label.setText(_translate("MainWindow", "Полное имя:"))
        self.pushButton_2.setText(_translate("MainWindow", "Добавить"))
        self.label_2.setText(_translate("MainWindow", "Введите название"))
        self.label_3.setText(_translate("MainWindow", "Введите стоимость"))
        self.label_4.setText(_translate("MainWindow", "Введите код"))
        self.label_5.setText(_translate("MainWindow", "Введите продолжительность"))
        self.label_6.setText(_translate("MainWindow", "Введите отклонение"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
