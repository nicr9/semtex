from PyQt4 import QtGui, QtCore
from semtex.layout import Ui_MainWindow
import semtex.const as const
import os, shlex
import subprocess as sp

__author__ = 'nic'

class Main(QtGui.QMainWindow):
    """
    Main window for the SemTeX Equation Editor.
    """

    # Misc Variables
    equation_history = [] # Buffer for saved equation strings

    def __init__(self,clip):
        """
        Setup GUI layout, connect event handlers.
        """
        super(Main,self).__init__()

        # Ensure system requirements are met
        self.checkDependancies()

        # This is always the same
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Change title
        self.setWindowTitle('SemTeX')

        # Connect event handlers
        self.ui.push_refresh.clicked.connect(self.refresh)
        self.ui.push_history.clicked.connect(self.saveToHistory)
        self.ui.push_equation.clicked.connect(self.copyToClipboard)

        # Display application logo
        self.displayPng()

        # Access saved equations and set last equation in the editor text box
        self.loadHistory()
        self.setFromHistory(1)

        # Bind application clipboard # TODO move this later
        self.clipboard = clip

    def refresh(self):
        """
        Takes the equation from the self.teInput, compiles and converts to PNG.
        """
        try:
            # Read from self.teInput
            eq = self.getInput()

            # If it contains an equation...
            if eq is not None:
                # ... compile and display it...
                self.generateLatex(eq)
                self.compileLatex()
                self.convertPng()
                self.convertPng(const.PNG_TRANS, const.PNG_DISP_PATH)
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
            with open(const.HISTORY_PATH,'r') as hist_file:
                # Clear previous history
                self.equation_history = []

                # Load equations from file
                for row in hist_file:
                    self.equation_history.append(row.strip())

            if const.DEV_MODE:
                self.printHistory()
        except IOError, e:
            raise e # TODO Method for creating files like .hist

    def setFromHistory(self, index):
        """
        Check last entry in history, insert into teInput
        """
        # Ensure the index is within the list bounds
        if len(self.equation_history) > index > 0:

            # If history isn't empty...
            if self.equation_history is not []:
                # ... display equation from history...
                self.ui.text_equation.setText(self.equation_history[-index])
            else:
                # ... otherwise display welcome message.
                self.ui.text_equation.setText(const.WELCOME_MESSAGE)

    def getInput(self):
        """
        Read from equation editor text box.
        If box is empty or contains welcome message, return None.
        """
        try:
            # Read from equation editor text box
            inp = self.ui.text_equation.toPlainText()

            # Check for invalid inputs...
            if inp != const.WELCOME_MESSAGE and inp != '':
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
            with open(const.HEADER_PATH,'r') as head,\
                    open(const.FOOTER_PATH,'r') as foot,\
                    open(const.LATEX_CODE_PATH,'w') as outp: # TODO: Check is this PEP 8
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
            with open(const.STDOUT_PATH,'w') as stdout_file:
                # latex command as string
                cmd = 'latex -output-directory=%s %s' % (const.CACHE_PATH,const.LATEX_CODE_PATH)

                # Run command in separate process
                latex_call = sp.call(shlex.split(cmd), stdout = stdout_file)

                # If latex returns a 1, raise exception
                if latex_call:
                    raise Exception('compileLatex - subprocess call failed')
        except sp.CalledProcessError, e:
            raise e
        except Exception, e:
            raise e

    def convertPng(self, bg = 'rgb 1.0 1.0 1.0', outp = const.PNG_CLIP_PATH):
        """
        Using dvipng command line utility, creates a .png file from the .dvi file generated earlier by latex.
        """
        try:
            # Open file to store output from dvipng command
            with open(const.STDOUT_PATH,'w') as stdout_file:
                # dvipng command as string
                cmd = 'dvipng -T tight -x 1200 -z 9 -bg %s -o %s %s' % (bg, outp, const.LATEX_OUTP_PATH)

                # Run command in separate process
                dvipng_call = sp.call(shlex.split(cmd), stdout = stdout_file)

                # If dvipng returns a 1, raise exception
                if dvipng_call:
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
            with open(const.STDOUT_PATH,'w') as outp_file:
                # Commands as strings
                cmd_latex = 'which latex'
                cmd_dvipng = 'which dvipng'

                # Run commands in separate processes
                latex_check = sp.call(shlex.split(cmd_latex), stdout = outp_file)
                dvipng_check = sp.call(shlex.split(cmd_dvipng), stdout = outp_file)

                # If either is missing...
                if latex_check or dvipng_check:
                    message = '' # TODO: is it needed to pre-declare this?

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
            quit() # TODO: find an other way to do this

    def cleanUp(self):
        """
        Delete any temporary files that were created during refresh().
        """
        try:
            # Check for any files called temp, create list
            file_list = sp.check_output('ls %s' % os.path.join(const.CACHE_PATH,'temp.*'), shell = True)
            file_list = file_list.strip().split('\n')

            # Find a temp.png, remove it from list
            png = file_list.index(const.PNG_DISP_PATH)
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
        temp_path = const.APP_LOGO_PATH if eq is None else const.PNG_DISP_PATH

        # Open the image as a QIcon
        icon = QtGui.QIcon(temp_path)
        # Display in equation editor
        self.ui.push_equation.setIcon(icon)
        self.ui.push_equation.setIconSize(QtCore.QSize(100,100))

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
            hist = [z+'\n' for z in self.equation_history[-const.HISTORY_LENGTH:]]

            # Update history
            with open(const.HISTORY_PATH,'w') as hist_file:
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
            self.clipboard.setPixmap(QtGui.QPixmap(const.PNG_CLIP_PATH), mode = self.clipboard.Clipboard)
            if const.DEV_MODE:
                print 'Copied to clipboard'
        else:
            if const.DEV_MODE:
                print 'Nothing to copy to clipboard'
