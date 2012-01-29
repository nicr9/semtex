'''
Created on 20 Jan 2012

@author: nic
'''
import os, sys, shlex
import subprocess as sp
from PyQt4 import QtGui, QtCore

# Misc
logo_path = 'logo.png'
outp_path = '.outp'

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
        self.setFromHist(-1)
        
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
        self.displayPng()
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
            self.displayPng()
        else:
            self.displayPng()

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

    def setFromHist(self, index):
        """
        Check last entry in history, insert into teInput
        """
        if index >= -(self.hist_len) and index < 0:
            if self.hist != []:
                self.teInput.setText(self.hist[index])
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
        outp_file = None
        try:
            outp_file = open(outp_path,'w')
            cmd = 'latex temp.tex'
            
            x = sp.call(shlex.split(cmd), stdout = outp_file)
            
            if x:
                raise Exception('compileLatex - subprocess call failed')
        except Exception, e:
            print 'Error - compiling .tex file'
            raise e
        except sp.CalledProcessError, e:
            raise e
        finally:
            outp_file.close()
            
    def convertPng(self):
        """
        Converts dvi file created by latex to png
        """
        outp_file = None
        try:
            outp_file = open(outp_path,'w')
            cmd = 'dvipng -T tight -x 1200 -z 9 -bg rgb 1.0 1.0 1.0 -o temp.png temp.dvi'
            
            x = sp.call(shlex.split(cmd), stdout = outp_file)
            
            if x:
                raise Exception('convertPng - subprocess call failed')
        except Exception, e:
            print 'Error - converting to png'
            raise e
        except sp.CalledProcessError, e:
            raise e
        finally:
            outp_file.close()
            
    def checkDependancies(self):
        """
        Check For Resources: dvipng, latex
        """
        outp_file = None
        try:
            outp_file = open(outp_path,'w')
            cmd_latex = 'which latex'
            cmd_dvipng = 'which dvipng'
            
            latex_check = sp.call(shlex.split(cmd_latex), stdout = outp_file)
            dvipng_check = sp.call(shlex.split(cmd_dvipng), stdout = outp_file)
    
            if latex_check or dvipng_check:
                message = ''
                
                # Create exception message specifying the missing utility
                if latex_check and dvipng_check:
                    message = 'Please make sure you have latex and dvipng installed'
                else:
                    missing_resource = 'latex' if latex_check == '' else 'dvipng'
                    message = 'Command line utility % could not be found' % missing_resource
                    
                raise Exception(message)
        except Exception, e:
            print 'Error - failed search for resources'
            print 'Details -', e
            quit()
        finally:
            outp_file.close()
    
    def cleanUp(self):
        """
        Get rid of unnecessary files
        """
        outp_file = None
        try:
            outp_file = open(outp_path,'w')
            
            file_list = sp.check_output('ls temp.*', shell = True, stdout = outp_file)
            file_list = file_list.strip().split('\n')
            
            png = file_list.index('temp.png')
            file_list.pop(png) # We don't want to remove the image
            
            for row in file_list:
                os.remove(row)
        except sp.CalledProcessError:
            pass
        finally:
            outp_file.close()

    def displayPng(self):
        """
        Show equation as an image. Show logo if no equation
        """
        eq = self.getInput()
        icon = None
        if eq != None:
            icon = QtGui.QIcon('temp.png')
        else:
            icon = QtGui.QIcon(logo_path)
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