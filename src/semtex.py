'''
Created on 20 Jan 2012

@author: nic
'''
import os, commands

# Clean up
def cleanUp():
    file_list = commands.getoutput('ls temp.*')
    if file_list != 'ls: cannot access temp.*: No such file or directory':
        file_list = file_list.split('\n')
        for row in file_list:
            os.remove(row)

# Misc Variables
hist = [] # Buffer for recent history of commands
hist_len = 5 # Number of equations to save to history


if __name__ == '__main__':
    # Clean up files
    cleanUp()
    
    # Check For Resources: dvipng, latex
    try:
        latex_check = commands.getoutput('which latex')
        dvipng_check = commands.getoutput('which dvipng')
        
        if (latex_check == '' or dvipng_check == ''):
            'Missing resources, please make sure you have latex and dvipng installed'
            quit()
    except Exception, e:
        print 'Error - failed search for resources'
        print 'Details -', e
        quit()
        
    try:
        # Check For History, Create History
        hist_file = file('.hist','r')
    
        # Display Previous Equations
        print 'Previous equations:'
    
        for row in hist_file:
            hist.append(row.strip())
            print '\t',row.strip()
    except IOError, e:
        print 'Error - accessing history'
        print 'Details -', e
    finally:
        hist_file.close()
    
    # Ask For Equation
    try:
        inp = raw_input('Please enter an equation:')
        hist.append(inp)
    except IOError, e:
        print 'Error - asking for equation'
        print 'Details -', e
        quit()
        
    # Generate LaTeX File
    try:
        eq_start = file('.start','r')
        eq_end = file('.end','r')
        
        eq = eq_start.read() + hist[-1] + eq_end.read()
        
        temp = file('temp.tex','w')
        temp.write(eq)
    except Exception, e:
        print 'Error - creating .tex file'
        print 'Details -', e
        cleanUp()
        quit()
    finally:
        eq_start.close()
        eq_end.close()
        temp.close()
        
    # Compile LaTeX
    try:
        os.system('latex temp.tex')
    except Exception, e:
        print 'Error - compiling .tex file'
        print 'Details -', e
        cleanUp()
        quit()
    
    # PNG Conversion
    try:
        os.system('dvipng -T tight -x 1200 -z 9 -bg transparent -o temp.png temp.dvi')
    except Exception, e:
        print 'Error - converting to png'
        print 'Details -', e
        cleanUp()
        
    # Save History
    try:
        while '\n' in hist:
            i = hist.index('\n')
            hist.pop(i)
        hist = [z+'\n' for z in hist[-hist_len:]] # Last five entries only, add endl to each
        hist_file = file('.hist','w')
        for row in hist:
            hist_file.write(row)
    except IOError, e:
        print e
    finally:
        hist_file.close()
        quit()