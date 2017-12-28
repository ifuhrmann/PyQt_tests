import sys
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *



import sys, random
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Points')
        self.show()

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        
    def drawPoints(self, qp):
      
        qp.setPen(QtCore.Qt.black)
        size = self.size()
        for i in range(10):
            for j in range(20):
                x=i*60+30
                y=j*30+15
                print x,y
                q=QRect(x,y,5,5)
                qp.fillRect(q,Qt.SolidPattern)    
                
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
