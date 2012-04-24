# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'matrix.ui'
#
# Created: Tue Apr 24 17:34:00 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Matrix(object):
    def setupUi(self, Matrix):
        Matrix.setObjectName(_fromUtf8("Matrix"))
        Matrix.resize(307, 160)
        Matrix.setWindowTitle(QtGui.QApplication.translate("Matrix", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.widget = QtGui.QWidget(Matrix)
        self.widget.setGeometry(QtCore.QRect(1, 11, 296, 139))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setText(QtGui.QApplication.translate("Matrix", "Enter matrix in matlab format: e.g. [1,2,3;4,5,6;7,8,9]", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setText(QtGui.QApplication.translate("Matrix", "[]", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setText(QtGui.QApplication.translate("Matrix", "Select a matrix format", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.comboBox = QtGui.QComboBox(self.widget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Matrix", "[]", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("Matrix", "{}", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("Matrix", "()", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(3, QtGui.QApplication.translate("Matrix", "||", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout.addWidget(self.comboBox)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Matrix)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Matrix.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Matrix.accept)
        QtCore.QMetaObject.connectSlotsByName(Matrix)

    def retranslateUi(self, Matrix):
        pass

