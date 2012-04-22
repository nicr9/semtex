# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout.ui'
#
# Created: Sun Apr 22 16:18:43 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(480, 246)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 457, 193))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.text_equation = QtGui.QTextEdit(self.layoutWidget)
        self.text_equation.setMaximumSize(QtCore.QSize(16777215, 121))
        self.text_equation.setHtml(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Enter LaTeX code here</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.text_equation.setObjectName(_fromUtf8("text_equation"))
        self.verticalLayout.addWidget(self.text_equation)
        self.push_refresh = QtGui.QPushButton(self.layoutWidget)
        self.push_refresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.push_refresh.setObjectName(_fromUtf8("push_refresh"))
        self.verticalLayout.addWidget(self.push_refresh)
        self.push_history = QtGui.QPushButton(self.layoutWidget)
        self.push_history.setText(QtGui.QApplication.translate("MainWindow", "Save to History", None, QtGui.QApplication.UnicodeUTF8))
        self.push_history.setObjectName(_fromUtf8("push_history"))
        self.verticalLayout.addWidget(self.push_history)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.push_equation = QtGui.QPushButton(self.layoutWidget)
        self.push_equation.setMinimumSize(QtCore.QSize(191, 191))
        self.push_equation.setMaximumSize(QtCore.QSize(191, 191))
        self.push_equation.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Logo/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.push_equation.setIcon(icon)
        self.push_equation.setIconSize(QtCore.QSize(250, 250))
        self.push_equation.setObjectName(_fromUtf8("push_equation"))
        self.horizontalLayout.addWidget(self.push_equation)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_history = QtGui.QMenu(self.menubar)
        self.menu_history.setTitle(QtGui.QApplication.translate("MainWindow", "History", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_history.setObjectName(_fromUtf8("menu_history"))
        self.menu_help = QtGui.QMenu(self.menubar)
        self.menu_help.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_help.setObjectName(_fromUtf8("menu_help"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_about = QtGui.QAction(MainWindow)
        self.action_about.setText(QtGui.QApplication.translate("MainWindow", "About SemTeX", None, QtGui.QApplication.UnicodeUTF8))
        self.action_about.setObjectName(_fromUtf8("action_about"))
        self.action_matrix = QtGui.QAction(MainWindow)
        self.action_matrix.setText(QtGui.QApplication.translate("MainWindow", "Enter Matrix", None, QtGui.QApplication.UnicodeUTF8))
        self.action_matrix.setObjectName(_fromUtf8("action_matrix"))
        self.menu_help.addAction(self.action_about)
        self.menu_help.addAction(self.action_matrix)
        self.menubar.addAction(self.menu_history.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

