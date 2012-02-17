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

# Dev mode enabled
DEV_MODE = True

# File paths
CACHE_PATH = 'semtex_gui/cache/'
RES_PATH = 'semtex_gui/res/'
APP_LOGO_PATH = RES_PATH + 'logo.png'
STDOUT_PATH = CACHE_PATH + '.outp'
HISTORY_PATH = CACHE_PATH + '.hist'
HEADER_PATH = RES_PATH + '.start'
FOOTER_PATH = RES_PATH + '.end'
LATEX_CODE_PATH = CACHE_PATH + 'temp.tex'
LATEX_OUTP_PATH = CACHE_PATH + 'temp.dvi'
PNG_DISP_PATH = CACHE_PATH + 'temp.png'
PNG_CLIP_PATH = CACHE_PATH + 'clip.png'

class Editor(QtGui.QWidget):
    """
    Main window of the SemTeX Equation Editor.
    Consists of a text box to enter a LaTeX formatted equation, refresh and saveToHistory buttons and an image button to display the equation in.
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
        super(Editor, self).__init__()
    
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
        self.setWindowIcon(QtGui.QIcon(APP_LOGO_PATH))

        # --- TextEdits ---
        self.teInput = QtGui.QTextEdit()
        self.teInput.resize(20,10) 

        # --- Create Button ---
        bRefresh = QtGui.QPushButton('Refresh')
        bRefresh.clicked.connect(self.refresh)
        
        bSave = QtGui.QPushButton('Save')
        bSave.clicked.connect(self.saveToHistory)

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
                self.convertPng('transparent', PNG_DISP_PATH)
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
            with open(HISTORY_PATH,'r') as hist_file:
                # Clear previous history
                self.equation_history = []
                
                # Load equations from file
                for row in hist_file:
                    self.equation_history.append(row.strip())
            
            if DEV_MODE:
                self.printHistory()
        except IOError, e:
            print 'Error - accessing history'
            print 'Details -', e

    def setFromHistory(self, index):
        """
        Check last entry in history, insert into teInput
        """
        # Ensure the index is within the list bounds
        if index < len(self.equation_history) and index > 0:
            
            # If history isn't empty...
            if self.equation_history is not []:
                # ... display equation from history...
                self.teInput.setText(self.equation_history[-index])
            else:
                # ... otherwise display welcome message.
                self.teInput.setText(self.WELCOME_MESSAGE)
    
    def getInput(self):
        """
        Read from equation editor text box.
        If box is empty or contains welcome message, return None.
        """
        try:
            # Read from equation editor text box
            inp = self.teInput.toPlainText()
            
            # Check for invalid inputs...
            if inp != self.WELCOME_MESSAGE and inp != '':
                return inp
            else:
                # ... if input is invalid, return None
                return None
        except Exception, e:
            raise e            

    def generateLatex(self, inp):
        """
        Construct LaTeX file from a combination of template files and input from the equation editor.
        """
        try:
            # Open templates and output file
            with open(HEADER_PATH,'r') as head, open(FOOTER_PATH,'r') as foot, open(LATEX_CODE_PATH,'w') as outp:
                # Concatenate LaTeX code from templates and input
                eq = head.read() + inp + foot.read()
                
                # Write code to output file 
                outp.write(eq)
        except IOError, e:
            print 'Error - creating .tex file'
            print 'Details -', e
        
    def compileLatex(self):
        """
        Use the latex command line utility to compile code to a .tex file.
        """
        try:
            # Open file to store output from latex command
            with open(STDOUT_PATH,'w') as stdout_file:
                # latex command as string
                cmd = 'latex -output-directory=%s %s' % (CACHE_PATH,LATEX_CODE_PATH)
                
                # Run command in separate process
                x = sp.call(shlex.split(cmd), stdout = stdout_file)
                
                # If latex returns a 1, raise exception
                if x:
                    raise Exception('compileLatex - subprocess call failed')
        except sp.CalledProcessError, e:
            raise e
        except Exception, e:
            raise e
            
    def convertPng(self, bg = 'rgb 1.0 1.0 1.0', outp = PNG_CLIP_PATH):
        """
        Using dvipng command line utility, creates a .png file from the .dvi file generated earlier by latex.
        """
        try:
            # Open file to store output from dvipng command
            with open(STDOUT_PATH,'w') as stdout_file:
                # dvipng command as string
                cmd = 'dvipng -T tight -x 1200 -z 9 -bg %s -o %s %s' % (bg, outp, LATEX_OUTP_PATH)
                
                # Run command in separate process
                x = sp.call(shlex.split(cmd), stdout = stdout_file)
                
                # If dvipng returns a 1, raise exception
                if x:
                    raise Exception('convertPng - subprocess call failed')
        except sp.CalledProcessError, e:
            raise e
        except Exception, e:
            raise e
            
    def checkDependancies(self):
        """
        Check for command line utilities: dvipng, latex.
        If either or both of these are not installed an exception will be raised and the program will quit.
        """
        try:
            # Open file to store output from either command
            with open(STDOUT_PATH,'w') as outp_file:
                # Commands as strings
                cmd_latex = 'which latex'
                cmd_dvipng = 'which dvipng'
                
                # Run commands in separate processes
                latex_check = sp.call(shlex.split(cmd_latex), stdout = outp_file)
                dvipng_check = sp.call(shlex.split(cmd_dvipng), stdout = outp_file)
                
                # If either is missing...
                if latex_check or dvipng_check:
                    message = ''
                    
                    # ...check which utility is missing, explain in message and...
                    if latex_check and dvipng_check:
                        message = 'Please make sure you have latex and dvipng installed'
                    else:
                        missing_resource = 'latex' if latex_check == '' else 'dvipng'
                        message = 'Command line utility % could not be found' % missing_resource
                    
                    # ...raise Exception containing the message.
                    raise Exception(message)
        except Exception, e:
            raise e
            quit()
    
    def cleanUp(self):
        """
        Delete any temporary files that were created during refresh().
        """
        try:
            # Check for any files called temp, create list
            file_list = sp.check_output('ls %stemp.*' % CACHE_PATH, shell = True)
            file_list = file_list.strip().split('\n')
            
            # Find a temp.png, remove it from list
            png = file_list.index(PNG_DISP_PATH)
            file_list.pop(png)
            
            # Delete any file remaining in the list
            for row in file_list:
                os.remove(row)
        except sp.CalledProcessError:
            pass # This probably means there aren't any files to clean up

    def displayPng(self):
        """
        Check equation editor text box, if it contains an equation display as an image. Otherwise display SemTeX logo.
        """
        # Read from equation editor text box
        eq = self.getInput()
        
        # If the box contents is invalid, use the app logo, otherwise use the equation's .png
        temp_path = APP_LOGO_PATH if eq is None else PNG_DISP_PATH
        
        # Open the image as a QIcon
        icon = QtGui.QIcon(temp_path)
        # Display in equation editor
        self.lEquation.setIcon(icon)
        self.lEquation.setIconSize(QtCore.QSize(100,100))
        
    def saveToHistory(self):
        """
        Push the current equation onto a persistently stored list.
        The max length of this list is currently limited to the value HISTORY_LENGTH.
        """
        try:
            # Append contents of text box to history
            self.equation_history.append(str(self.getInput()))
            
            # Remove newline entries from history
            while '\n' in self.equation_history:
                i = self.equation_history.index('\n')
                self.equation_history.pop(i)
            
            # Truncate history to HISTORY_LENGTH, attach '\n' to end of each
            hist = [z+'\n' for z in self.equation_history[-self.HISTORY_LENGTH:]]
            
            # Update history
            with open(HISTORY_PATH,'w') as hist_file:
                for row in hist:
                    hist_file.write(row)
                
            # Print new history to terminal
            self.printHistory()
        except IOError, e:
            raise e
        except Exception, e:
            raise e
    
    def copyToClipboard(self):
        """
        Copies the equations image to the clipboard.
        """
        # Cast png to QPixmap, add to clipboard
        if self.getInput():
            self.clipboard.setPixmap(QtGui.QPixmap(PNG_CLIP_PATH), mode = self.clipboard.Clipboard)
            if DEV_MODE:
                print 'Copied to clipboard'
        else:
            if DEV_MODE:
                print 'Nothing to copy to clipboard'

def main():
    app = QtGui.QApplication(sys.argv)
    root = Editor(app.clipboard()) #@UnusedVariable
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
