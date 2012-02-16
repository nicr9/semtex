import os, sys, shlex #@UnusedImport
import subprocess as sp #@UnusedImport
from PyQt4 import QtGui, QtCore #@UnusedImport
from semtex_gui.editor import * #@UnusedWildImport

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    root = Editor(app.clipboard()) #@UnusedVariable
    sys.exit(app.exec_())
