import sys
from PyQt4 import QtGui
from semtex.gui import Main

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    root = Main(app) #@UnusedVariable
    root.show()
    sys.exit(app.exec_())
