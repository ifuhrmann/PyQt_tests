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
        self.man=[False,0,0]
        self.initUI()
        self.timer=QBasicTimer()
        self.timer.start(100,self)


        

    def initUI(self):
        
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Simple Test')
        self.show()


    def timerEvent(self,event):
        self.info[(30,15)].status="OFF"
        self.repaint()
        if self.man[0]:
            self.man[2]+=5
        else:
            if self.man[2]>=600:
                self.man=[False,0,0]
        self.timer.start(50,self)

    def paintEvent(self, e):
        qp=QPainter()
        qp.begin(self)

        br=QBrush(Qt.SolidPattern)
        br.setColor(Qt.white)
        r=QRect(0,0,1000,1000)
        qp.fillRect(r,br)
        
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

        if self.man[0]:
            m=QRect(self.man[1],self.man[2],10,4)
            brush=QBrush(Qt.SolidPattern)
            brush.setColor(Qt.green)
            qp.fillRect(m,brush)

        qp.end()
        

    
    def mousePressEvent(self,event):
        for s in self.info:
            if s[0]<=event.x()<=s[0]+5 and s[1]<=event.y()<=s[1]+5:
                b=infoMessage(self.info[s])
                b.exec_()

    def keyPressEvent(self,event):
        key=event.key()
        if(key == Qt.Key_Return):
            self.man=[True,300,0]



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
