# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(509, 800)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 650, 514, 140))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.main_menu = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.main_menu.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.main_menu.setContentsMargins(0, 0, 0, 0)
        self.main_menu.setSpacing(0)
        self.main_menu.setObjectName("main_menu")
        self.menu_button1 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.menu_button1.setMinimumSize(QtCore.QSize(128, 128))
        self.menu_button1.setMaximumSize(QtCore.QSize(128, 128))
        self.menu_button1.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon1_menu.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_button1.setIcon(icon)
        self.menu_button1.setIconSize(QtCore.QSize(160, 160))
        self.menu_button1.setFlat(True)
        self.menu_button1.setObjectName("menu_button1")
        self.main_menu.addWidget(self.menu_button1)
        self.menu_button2 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.menu_button2.setMinimumSize(QtCore.QSize(128, 128))
        self.menu_button2.setMaximumSize(QtCore.QSize(128, 128))
        self.menu_button2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icon2_menu.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_button2.setIcon(icon1)
        self.menu_button2.setIconSize(QtCore.QSize(160, 160))
        self.menu_button2.setFlat(True)
        self.menu_button2.setObjectName("menu_button2")
        self.main_menu.addWidget(self.menu_button2)
        self.menu_button3 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.menu_button3.setMinimumSize(QtCore.QSize(128, 128))
        self.menu_button3.setMaximumSize(QtCore.QSize(128, 128))
        self.menu_button3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../icon3_menu.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_button3.setIcon(icon2)
        self.menu_button3.setIconSize(QtCore.QSize(160, 160))
        self.menu_button3.setFlat(True)
        self.menu_button3.setObjectName("menu_button3")
        self.main_menu.addWidget(self.menu_button3)
        self.menu_button4 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.menu_button4.setMinimumSize(QtCore.QSize(128, 128))
        self.menu_button4.setMaximumSize(QtCore.QSize(128, 128))
        self.menu_button4.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../icon4_menu.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menu_button4.setIcon(icon3)
        self.menu_button4.setIconSize(QtCore.QSize(160, 160))
        self.menu_button4.setFlat(True)
        self.menu_button4.setObjectName("menu_button4")
        self.main_menu.addWidget(self.menu_button4)
        self.money_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.money_label.setGeometry(QtCore.QRect(20, 40, 471, 91))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(80)
        font.setStrikeOut(False)
        self.money_label.setFont(font)
        self.money_label.setStatusTip("")
        self.money_label.setAccessibleName("")
        self.money_label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.money_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.money_label.setObjectName("money_label")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(80, 130, 348, 80))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.pm_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.pm_layout.setContentsMargins(0, 0, 0, 0)
        self.pm_layout.setSpacing(200)
        self.pm_layout.setObjectName("pm_layout")
        self.plus_btn = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.plus_btn.setMinimumSize(QtCore.QSize(80, 80))
        self.plus_btn.setMaximumSize(QtCore.QSize(80, 80))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(50)
        font.setBold(True)
        font.setWeight(75)
        self.plus_btn.setFont(font)
        self.plus_btn.setDefault(False)
        self.plus_btn.setFlat(False)
        self.plus_btn.setObjectName("plus_btn")
        self.pm_layout.addWidget(self.plus_btn)
        self.minus_btn = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.minus_btn.setMinimumSize(QtCore.QSize(80, 80))
        self.minus_btn.setMaximumSize(QtCore.QSize(80, 80))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(50)
        font.setBold(True)
        font.setWeight(75)
        self.minus_btn.setFont(font)
        self.minus_btn.setFlat(False)
        self.minus_btn.setObjectName("minus_btn")
        self.pm_layout.addWidget(self.minus_btn)
        self.date_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.date_label.setGeometry(QtCore.QRect(210, 20, 81, 16))
        self.date_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.date_label.setObjectName("date_label")
        self.tip_plain = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.tip_plain.setGeometry(QtCore.QRect(30, 350, 451, 221))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.tip_plain.setFont(font)
        self.tip_plain.setReadOnly(True)
        self.tip_plain.setObjectName("tip_plain")
        self.tip_title_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.tip_title_label.setGeometry(QtCore.QRect(30, 330, 81, 16))
        self.tip_title_label.setObjectName("tip_title_label")
        self.new_tip = QtWidgets.QPushButton(parent=self.centralwidget)
        self.new_tip.setGeometry(QtCore.QRect(450, 330, 31, 21))
        self.new_tip.setMinimumSize(QtCore.QSize(31, 21))
        self.new_tip.setMaximumSize(QtCore.QSize(31, 21))
        self.new_tip.setObjectName("new_tip")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.money_label.setText(_translate("MainWindow", "99999₽"))
        self.plus_btn.setText(_translate("MainWindow", "-"))
        self.minus_btn.setText(_translate("MainWindow", "+"))
        self.date_label.setText(_translate("MainWindow", "13.11.2024"))
        self.tip_plain.setPlainText(_translate("MainWindow", "бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла-бла"))
        self.tip_title_label.setText(_translate("MainWindow", "💡Совет"))
        self.new_tip.setText(_translate("MainWindow", "🔄"))
