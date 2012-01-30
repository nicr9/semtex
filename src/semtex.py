'''
Created on 20 Jan 2012

@author: nic

--- Upcoming ---
* Code cleanup
* Caching of saved equations .png files
* Move all data files, cache to ~/.semtex
* Separate class for window and editor to allow more advanced features such as:
    * Menubar with history, about and settings
    * Keyboard shortcuts: ctrl+q, ctrl+r, ctrl+s
    * Statusbar for error messages
'''
import os, sys, shlex
import subprocess as sp
from PyQt4 import QtGui, QtCore

# File paths TODO: These should be constants
app_logo_path = 'logo.png'
stdout_path = '.outp'
history_path = '.hist'
head_path = '.start'
foot_path = '.end'
latex_code_path = 'temp.tex'
latex_outp_path = 'temp.dvi'
png_path = 'temp.png'

class Semtex(QtGui.QWidget):
    """
    Main window of the SemTeX Equation Editor.
    Consists of a text box to enter a LaTeX formatted equation, refresh and save buttons and an image button to display the equation in.
    """

    # Constants
    HISTORY_LENGTH = 5
    WELCOME_MESSAGE = "Welcome to SemTeX, please enter your equation here"
    
    # Misc Variables
    equation_history = [] # Buffer for saved equation strings
    
    def __init__(self, clip):
        """
        Create and initialise equation editor widget.
        """
        super(Semtex, self).__init__()
    
        # Layout UI
        self.initUi()
        
        # Ensure system requirements are met
        self.checkDependancies()
        
        # Access saved equations and set last equation in the editor text box
        self.loadHistory()
        self.setFromHistory(1)
        
        # Bind application clip TODO: move this later 
        self.clipboard = clip
        
    def initUi(self):
        """
        Create all sub widgets, layout appropriately. 
        """
        # --- Set Up Window ---
        self.setGeometry(300, 300, 350, 150)
        self.setWindowTitle('SemTeX: Equations Made using laTEX')
        self.setWindowIcon(QtGui.QIcon(app_logo_path))

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
        Takes the equation from the self.teInput, compiles and converts to PNG.
        """
        try:
            # Read from self.teInput
            eq = self.getInput()
            
            # If it contains an equation...
            if eq != None:
                # ... compile and display it...
                self.generateLatex(eq)
                self.compileLatex()
                self.convertPng()
                self.cleanUp()
                self.displayPng()
            else:
                # ... otherwise, display the semtex logo 
                self.displayPng()
        except Exception, e:
            raise e

    def printHistory(self):
        """
        Display previously saved equations in terminal for debugging purposes.
        """
        print 'Previous equations:'
        for row in self.equation_history:
            print '\t', row.strip()

    def loadHistory(self):
        """
        Load saved equations, print them to terminal.
        """
        try:
            # Open/create history file
            with open(history_path,'r') as hist_file:
                # Clear previous history
                self.equation_history = []
                
                # Load equations from file
                for row in hist_file:
                    self.equation_history.append(row.strip())
            
            # TODO: Dev only
            self.printHistory()
        except IOError, e:
            print 'Error - accessing history'
            print 'Details -', e

    def setFromHistory(self, index):
        # TODO: What happens if the buffer isn't at the max length and the index exceeds the current buffer length
        """
        Check last entry in history, insert into teInput
        """
        if index <= self.HISTORY_LENGTH and index > 0:
            if self.equation_history != []:
                self.teInput.setText(self.equation_history[-index])
            else:
                self.teInput.setText(self.WELCOME_MESSAGE)
    
    def getInput(self):
        inp = self.teInput.toPlainText()
        if inp != self.WELCOME_MESSAGE and inp != '':
            return inp
        else:
            return None

    def generateLatex(self, inp):
        """
        Generate LaTeX File
        """
        # Generate LaTeX File
        try:
            with open(head_path,'r') as head, open(foot_path,'r') as foot, open(latex_code_path,'w') as outp:
                # Concatenate LaTeX code from templates
                eq = head.read() + inp + foot.read()
                
                # Write to output 
                outp.write(eq)
        except IOError, e:
            print 'Error - creating .tex file'
            print 'Details -', e
        
    def compileLatex(self):
        """
        Use LaTeX to compile .tex file
        """
        try:
            with open(stdout_path,'w') as outp_file:
                cmd = 'latex %s' % latex_code_path
                
                x = sp.call(shlex.split(cmd), stdout = outp_file)
                
                if x:
                    raise Exception('compileLatex - subprocess call failed')
        except Exception, e:
            print 'Error - compiling .tex file'
            raise e
        except sp.CalledProcessError, e:
            raise e
            
    def convertPng(self):
        """
        Converts dvi file created by latex to png
        """
        try:
            with open(stdout_path,'w') as outp_file:
                cmd = 'dvipng -T tight -x 1200 -z 9 -bg rgb 1.0 1.0 1.0 -o %s %s' % (png_path, latex_outp_path)
                
                x = sp.call(shlex.split(cmd), stdout = outp_file)
                
                if x:
                    raise Exception('convertPng - subprocess call failed')
        except Exception, e:
            print 'Error - converting to png'
            raise e
        except sp.CalledProcessError, e:
            raise e
            
    def checkDependancies(self):
        """
        Check For Resources: dvipng, latex
        """
        try:
            with open(stdout_path,'w') as outp_file:
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
    
    def cleanUp(self):
        """
        Get rid of unnecessary files
        """
        try:
            file_list = sp.check_output('ls temp.*', shell = True)
            file_list = file_list.strip().split('\n')
            
            png = file_list.index('temp.png')
            file_list.pop(png) # We don't want to remove the image
            
            for row in file_list:
                os.remove(row)
        except sp.CalledProcessError:
            pass # This just means there aren't any files to clean up

    def displayPng(self):
        """
        Show equation as an image. Show logo if no equation
        """
        eq = self.getInput()
        icon = None
        if eq != None:
            icon = QtGui.QIcon('temp.png')
        else:
            icon = QtGui.QIcon(app_logo_path)
        self.lEquation.setIcon(icon)
        self.lEquation.setIconSize(QtCore.QSize(100,100))
        
    def save(self):
        try:
            # Add contents of textEdit to history
            self.equation_history.append(str(self.getInput()))
            
            # Remove 'endl's from history
            while '\n' in self.equation_history:
                i = self.equation_history.index('\n')
                self.equation_history.pop(i)
            
            # Last five entries only, add endl to each
            hist = [z+'\n' for z in self.equation_history[-self.HISTORY_LENGTH:]]
            
            # Update history
            with open(history_path,'w') as hist_file:
                for row in hist:
                    hist_file.write(row)
                
            # Print new history to terminal
            self.printHistory()
        except IOError, e:
            print e
    
    def copyToClipboard(self):
        """
        Copies the image 'temp.png' to the clipboard.
        """
        # TODO: Do something else if no equation
        self.clipboard.setPixmap(QtGui.QPixmap('temp.png'), mode = self.clipboard.Clipboard)
        print 'Copied to clipboard'

def main():
    app = QtGui.QApplication(sys.argv)
    root = Semtex(app.clipboard()) #@UnusedVariable
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()