# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frac.ui'
#
# Created: Tue Apr 24 17:41:16 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Frac(object):
    def setupUi(self, Frac):
        Frac.setObjectName(_fromUtf8("Frac"))
        Frac.resize(286, 164)
        Frac.setWindowTitle(QtGui.QApplication.translate("Frac", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.layoutWidget = QtGui.QWidget(Frac)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 11, 261, 141))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setText(QtGui.QApplication.translate("Frac", "Numerator:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.line_num = QtGui.QLineEdit(self.layoutWidget)
        self.line_num.setText(_fromUtf8(""))
        self.line_num.setObjectName(_fromUtf8("line_num"))
        self.verticalLayout.addWidget(self.line_num)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setText(QtGui.QApplication.translate("Frac", "Denominator:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.line_den = QtGui.QLineEdit(self.layoutWidget)
        self.line_den.setText(_fromUtf8(""))
        self.line_den.setObjectName(_fromUtf8("line_den"))
        self.verticalLayout.addWidget(self.line_den)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Frac)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Frac.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Frac.reject)
        QtCore.QMetaObject.connectSlotsByName(Frac)

    def retranslateUi(self, Frac):
        pass

