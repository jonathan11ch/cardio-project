#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, we position two push
buttons in the bottom-right corner 
of the window. 

author: Jan Bodnar
website: zetcode.com 
last edited: October 2011
"""

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import resources_rc

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.led = Led_widget()
        okButton = QtGui.QPushButton("OK")
        cancelButton = QtGui.QPushButton("Cancel")
        okButton.clicked.connect(lambda: self.led.set_pixmap(1))
        cancelButton.clicked.connect(lambda: self.led.set_pixmap(0))

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addWidget(self.led)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)    
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()

class Led_widget(QtGui.QLabel):


    def __init__(self):
        super(Led_widget, self).__init__()

        self.initUI()

    def initUI(self):
        print("loading image")
        self.pixmap = QtGui.QPixmap()
        self.set_pixmap(0)

        self.show()

    def set_pixmap(self, value):

        if value == 0:
            self.pixmap.load(':img/red_bulb.png')
        elif value == 1:
            self.pixmap.load(':img/orange_bulb.png')
        elif value == 2:
            self.pixmap.load(':img/green_bulb.png')

        self.pixmap = self.pixmap.scaled(20,20, QtCore.Qt.KeepAspectRatio)
        
        if self.pixmap.isNull():
            print("Null image...")
        else:
            print("Image loaded... ")

        self.setPixmap(self.pixmap)
        self.resize(self.pixmap.size())


        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex1 = Example()
    ex2 = Example()
    
    led = Led_widget()


    p = ex1.palette()
    p.setColor(ex1.backgroundRole(),QtGui.QColor('red') )
    ex1.setPalette(p)
    ex1.setAutoFillBackground(True)

    p = ex2.palette()
    p.setColor(ex2.backgroundRole(),QtGui.QColor('blue') )
    ex2.setPalette(p)
    ex2.setAutoFillBackground(True)
    
    vbox = QtGui.QVBoxLayout()
    vbox.addWidget(ex1)
    vbox.addWidget(ex2)
    vbox.addWidget(led)

    vbox.addStretch(1)


    w=QtGui.QWidget()
    w.setLayout(vbox)
    w.setGeometry(300, 300, 300, 150)
    w.setWindowTitle('Buttons')    
    w.show()

    led.set_pixmap(2)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()