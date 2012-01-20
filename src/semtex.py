'''
Created on 20 Jan 2012

@author: nic
'''
import os

if __name__ == '__main__':
    # Ask For Equation
    try:
        inp = raw_input('Please enter an equation:')
    except IOError, e:
        print 'Error - asking for equation'
        print 'Details -', e
        quit()
        
    # Generate LaTeX File
    try:
        eq_start = file('.start','r')
        eq_end = file('.end','r')
        
        eq = eq_start.read() + inp + eq_end.read()
        
        temp = file('temp.tex','w')
        temp.write(eq)
    except Exception, e:
        print 'Error - creating .tex file'
        print 'Details -', e
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
        quit()
    
    # PNG Conversion
    try:
        os.system('dvipng -T tight -x 1200 -z 9 -bg transparent -o temp.png temp.dvi')
    except Exception, e:
        print 'Error - converting to png'
        print 'Details -', e
        quit()