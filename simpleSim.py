import sys
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class infoMessage(QDialog):

    def __init__(self,node,parent=None):
        super(infoMessage,self).__init__(parent)

        layout = QHBoxLayout()
        okB=QPushButton("&OK")
        layout.addWidget(okB)
        self.setWindowTitle("Info:")


        L = QVBoxLayout()
        label=QLabel(str(node))
        L.addWidget(label)
        L.addLayout(layout)
        self.setLayout(L)

        self.connect(okB,SIGNAL("clicked()"),self.okClicked)


    def okClicked(self):
        self.accept()





class Example(QWidget):

    def __init__(self,stuff):
        super(Example, self).__init__()
        self.info=stuff
        self.initUI()
        
    def initUI(self):
        
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Simple Test')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        
    def drawPoints(self, qp):
      
        size = self.size()
        for s in self.info:
            x=int(s[0])
            y=int(s[1])
            q=QRect(x,y,5,5)
            brush=QBrush(Qt.SolidPattern)
            if(self.info[s].status=="ON"):
                brush.setColor(Qt.black)
            else:
                brush.setColor(Qt.red)
            qp.setBrush(brush)
            qp.fillRect(q,brush)
    def mousePressEvent(self,event):
        for s in self.info:
            if s[0]<=event.x()<=s[0]+5 and s[1]<=event.y()<=s[1]+5:
                b=infoMessage(self.info[s])
                b.exec_()

    def keyPressEvent(self,event):
        key=event.key()
        if(key == Qt.Key_Return):
            print "hey"



class Node():

    def __init__(self,pos,rssi,euid,status):
        s=pos.split(",")
        self.x=s[0]
        self.y=s[1]
        self.rssi=rssi
        self.euid=euid
        self.status=status

    def __str__(self):
        s=""
        s+="X: "+self.x+" Y: "+self.y+" RSSI: "+str(self.rssi)+" EUID: "+str(self.euid)+"\n\tThis node is "+self.status
        return s

if __name__ == '__main__':    
    app = QApplication(sys.argv)
    stuff={(30,15):Node("30,15",-12,"100200","ON"),(30,45):Node("30,45",-14,"243427u","OFF"),(150,55):Node("150,55",-9,"2h23727u","ON")}
    ex = Example(stuff)
    sys.exit(app.exec_())
