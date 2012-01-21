'''
Created on 20 Jan 2012

@author: nic
'''
import os, commands, sys
from PyQt4 import QtGui # TODO: Reduce scope of imports

# Misc
logo_path = 'logo.png'

class Semtex(QtGui.QWidget):

    # Misc Variables
    hist = [] # Buffer for recent history of commands
    
    def __init__(self):
        super(Semtex, self).__init__()
    
        self.initUi()
        self.checkDependancies()
        self.loadHistory()
        self.setLast()
        
    def initUi(self):
        # --- Set Up Window ---
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('SemTeX: Equations Made using laTEX')
        self.setWindowIcon(QtGui.QIcon(logo_path)) # TODO: Test this later

        # --- TextEdits ---
        self.teInput = QtGui.QTextEdit()
        self.teInput.resize(20,10) 

        # --- Create Button ---
        bRefresh = QtGui.QPushButton('Refresh')
        bRefresh.clicked.connect(self.refresh)

        # --- Create Label ---
        self.lEquation = QtGui.QLabel(self)
        self.lEquation.setPixmap(QtGui.QPixmap(logo_path))
        self.lEquation.setGeometry(160, 40, 80, 30)

        # --- Sort Layout ---
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.teInput)
        vbox.addWidget(bRefresh)
        
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
        self.generateLatex()
        self.compileLatex()
        self.convertPng()
        self.cleanUp()
        self.displayPng()
        
    def loadHistory(self):
        """
        Get last 5 entries in history, print to terminal
        """
        try:
            # Check For History, Create History
            hist_file = file('.hist','r')
        
            # Display Previous Equations in terminal
            print 'Previous equations:'
        
            for row in hist_file:
                self.hist.append(row.strip())
                print '\t',row.strip()
        except IOError, e:
            print 'Error - accessing history'
            print 'Details -', e
        finally:
            hist_file.close()

    def setLast(self):
        """
        Check last entry in history, insert into teInput
        """
        self.teInput.setText(self.hist[-1])
        
    def generateLatex(self):
        """
        Generate LaTeX File
        """
        # Generate LaTeX File
        try:
            eq_start = file('.start','r')
            eq_end = file('.end','r')
            
            eq = eq_start.read() + self.teInput.toPlainText() + eq_end.read()
            
            temp = file('temp.tex','w')
            temp.write(eq)
        except Exception, e:
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
        # Compile LaTeX
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
    
    # Clean up
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

    def displayPng(self):
        """
        Show image
        """
        # TODO: Set to logo for when there is no equation
        self.lEquation.setPixmap(QtGui.QPixmap('temp.png'))
        
#    # Save History
#    try:
#        while '\n' in hist:
#            i = hist.index('\n')
#            hist.pop(i)
#        hist = [z+'\n' for z in hist[-hist_len:]] # Last five entries only, add endl to each
#        hist_file = file('.hist','w')
#        for row in hist:
#            hist_file.write(row)
#    except IOError, e:
#        print e
#    finally:
#        hist_file.close()
#        quit()

def main():
    app = QtGui.QApplication(sys.argv)
    root = Semtex()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()