import sys
from PyQt4 import QtGui, QtCore #@UnusedImport
#from semtex_gui.editor import * #@UnusedWildImport
from semtex.gui import Main

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    root = Main(app.clipboard()) #@UnusedVariable
    root.show()
    sys.exit(app.exec_())
