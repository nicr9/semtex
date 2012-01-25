'''
Created on 20 Jan 2012

@author: nic
'''
import os, commands, sys
from PyQt4 import QtGui, QtCore # TODO: Reduce scope of imports

# Misc
logo_path = 'logo.png'

class Semtex(QtGui.QWidget):

    # Misc Variables
    hist = [] # Buffer for recent history of commands
    hist_len = 5 # max length of buffer
    welcome_message = "Welcome to SemTeX, please enter your equation here"
    
    def __init__(self, clipboard):
        super(Semtex, self).__init__()
    
        self.initUi()
        self.checkDependancies()
        self.loadHistory()
        self.setLast()
        
        self.clip = clipboard
        
    def initUi(self):
        # --- Set Up Window ---
        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('SemTeX: Equations Made using laTEX')
        self.setWindowIcon(QtGui.QIcon(logo_path))

        # --- TextEdits ---
        self.teInput = QtGui.QTextEdit()
        self.teInput.resize(20,10) 

        # --- Create Button ---
        bRefresh = QtGui.QPushButton('Refresh')
        bRefresh.clicked.connect(self.refresh)
        
        bSave = QtGui.QPushButton('Save')
        bSave.clicked.connect(self.save)

        # --- Create Image Button ---
        self.lEquation = QtGui.QPushButton(self)
        self.displayPng(logo_path)
        self.lEquation.clicked.connect(self.copyToClipboard)
        #self.lEquation.setPixmap(QtGui.QPixmap(logo_path))

        # --- Sort Layout ---
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.teInput)
        vbox.addWidget(bRefresh)
        vbox.addWidget(bSave)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addWidget(self.lEquation)
        
        self.setLayout(hbox)

        self.show()
    
    def refresh(self):
        """
        Takes the equation from the TextEdit, compiles and converts to PNG
        """
        eq = self.getInput()
        if eq != None:
            self.generateLatex(eq)
            self.compileLatex()
            self.convertPng()
            self.cleanUp()
            self.displayPng('temp.png')
        else:
            self.displayPng(logo_path)
        

    def displayHistory(self):
        """
        Display previously saved equations in terminal
        """
        print 'Previous equations:'
        for row in self.hist:
            print '\t', row.strip()

    def loadHistory(self):
        """
        Get last 5 entries in history, print to terminal
        """
        try:
            # Check for history file or create history file
            hist_file = file('.hist','r')
            
            # Load history from file
            self.hist = []
            for row in hist_file:
                self.hist.append(row.strip())
        
            self.displayHistory()
        except IOError, e:
            print 'Error - accessing history'
            print 'Details -', e
        finally:
            hist_file.close()

    def setLast(self):
        """
        Check last entry in history, insert into teInput
        """
        if self.hist != []:
            self.teInput.setText(self.hist[-1])
        else:
            self.teInput.setText(self.welcome_message)
        

    def getInput(self):
        inp = self.teInput.toPlainText()
        if inp != self.welcome_message and inp != '':
            return inp
        else:
            return None

    def generateLatex(self, inp):
        """
        Generate LaTeX File
        """
        # Generate LaTeX File
        try:
            eq_start = file('.start','r')
            eq_end = file('.end','r')
            
            eq = eq_start.read() + inp + eq_end.read()
            
            temp = file('temp.tex','w')
            temp.write(eq)
        except IOError, e:
            print 'Error - creating .tex file'
            print 'Details -', e
        finally:
            eq_start.close()
            eq_end.close()
            temp.close()
        
    def compileLatex(self):
        """
        Use LaTeX to compile .tex file
        """
        # TODO: Suppress output?
        try:
            os.system('latex temp.tex')
        except Exception, e:
            print 'Error - compiling .tex file'
            print 'Details -', e
            
    def convertPng(self):
        """
        Converts dvi file created by latex to png
        """
        # TODO: Suppress output?
        try:
            os.system('dvipng -T tight -x 1200 -z 9 -bg transparent -o temp.png temp.dvi')
        except Exception, e:
            print 'Error - converting to png'
            print 'Details -', e
            
    def checkDependancies(self):
        """
        Check For Resources: dvipng, latex
        """
        try:
            latex_check = commands.getoutput('which latex')
            dvipng_check = commands.getoutput('which dvipng')
    
            if (latex_check == '' or dvipng_check == ''):
                print 'Missing resources, please make sure you have latex and dvipng installed'
                quit() # TODO: change to throwing an exception
        except Exception, e:
            print 'Error - failed search for resources'
            print 'Details -', e
            quit()
    
    def cleanUp(self):
        """
        Get rid of unneccessary files
        """
        file_list = commands.getoutput('ls temp.*')
        if file_list != 'ls: cannot access temp.*: No such file or directory': # TODO: Find a cleaner way
            file_list = file_list.split('\n')
            
            png = file_list.index('temp.png')
            file_list.pop(png) # We don't want to remove the image
            
            for row in file_list:
                os.remove(row)

    def displayPng(self, icon):
        """
        Show equation as an image.
        """
        icon = QtGui.QIcon(icon)
        self.lEquation.setIcon(icon)
        self.lEquation.setIconSize(QtCore.QSize(100,100))
        
    def save(self):
        try:
            # Add contents of textEdit to history
            self.hist.append(str(self.getInput()))
            
            # Remove 'endl's from history
            while '\n' in self.hist:
                i = self.hist.index('\n')
                self.hist.pop(i)
            
            # Last five entries only, add endl to each
            hist = [z+'\n' for z in self.hist[-self.hist_len:]]
            
            # Open history, update
            hist_file = file('.hist','w')
            for row in hist:
                hist_file.write(row)
                
            # Print new history to terminal
            self.displayHistory()
        except IOError, e:
            print e
        finally:
            hist_file.close()
    
    def copyToClipboard(self):
        """
        Copies the image 'temp.png' to the clipboard.
        """
        # TODO Do something else if no equation
        self.clip.setPixmap(QtGui.QPixmap('temp.png'), mode = self.clip.Clipboard)
        print 'Copied to clipboard'

def main():
    app = QtGui.QApplication(sys.argv)
    root = Semtex(app.clipboard()) #@UnusedVariable
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()