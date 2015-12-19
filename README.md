# SemTeX: Equations Made using LaTeX

Created by Nic Roland.

Equation editor for Linux that takes LaTeX code and copies the resulting png to
your clipboard.

## Dependancies

Python 2.7.x - www.python.org
PyQt4 - http://www.riverbankcomputing.co.uk/software/pyqt/download
LaTeX - www.latex-project.org
dvipng - www.sourceforge.net/projects/dvipng/

## How to

* Make sure you're using python 2.7 or greater.
* Install dependencies (this will take a long time, pyqt4 takes ages).
    - sudo apt-get install texlive-full dvipng python-qt4
* Run `python semtex.py`
* Enter some LaTeX code and press refresh to render the code.
* Click on the rendered image to copy it to your clipboard.

## Contributing

If you would like to contribute in the form of documentation corrections, new
features or bug fixes, please open a pull request and I will attend to it as
soon as possible.

### UI changes

If you're planning on changing the UI, you should install `pyqt4-dev-tools`.

Open the specific `.ui` file you want to change with QtCreator. When you're
finished you need to build a new python module for that UI:

```
pyuic4 input.ui -o output.py
```

When you've tested everything, please remember to include both the `.ui` file
and `.py` file in your pull request.

## Upcoming Features

* Package SemTeX up with dependencies to make installable
* Auto create ~/.semtex folder to store cache/ and res/
* LaTeX Cheet Sheet
* Auto-determinatnt to Matrix editor
* Edit matrix from a context menu
