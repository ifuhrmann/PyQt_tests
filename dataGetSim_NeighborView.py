import sys
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import requests
from pprint import pprint
import random

def populateNeighbors(nodes):
    for n in nodes:
        l={}
        for n1 in nodes:
            if n != n1 :
                l[100*sqrt( (n1.x-n.x)**2 +  (n1.y-n.y)**2 )+(10**(-14))*n1.euid]=n1            
        sort=sorted(l)
        tot=[]
        for i in range(16):
            tot.append(l[sort[i]])
        n.neighbors=tot
            
def getData():
    r=requests.get('http://localhost:8080/fixtures')
    fixtures=r.json()
    l=[]
    x=-30
    y=10
    for s in fixtures:
        x+=40
        if x>=580:
            x=10
            y+=40
        l.append(Node(x,y,s))

    populateNeighbors(l)
    return ( l )



def updateData(data):
    r=requests.get('http://localhost:8080/fixtures')
    fixtures=r.json()
    l=[]
    x=-30
    y=10
    for s in fixtures:
        x+=40
        if x>=580:
            x=10
            y+=40
        l.append(Node(x,y,s))

    for s in l:
        for n in data:
            if s==n:
                n.update(s)
                break
    



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



class testMenu(QDialog):

    def __init__(self,parent=None):
        super(testMenu,self).__init__(parent)


        layout = QHBoxLayout()
        okB=QPushButton("&Run this")
        cancel=QPushButton("No Test")
        layout.addWidget(okB)
        layout.addWidget(cancel)
        self.setWindowTitle("Info:")


        L = QVBoxLayout()
        label=QLabel("What test do you want to run?")
        L.addWidget(label)
        
        radio=QHBoxLayout()
        self.r1=QRadioButton("Man Walking: Straight Path")
        self.r2=QRadioButton("Man Walking: Circular Path")
        self.r3=QRadioButton("Man Walking: User Controlled Path")
        radio.addWidget(self.r1)
        radio.addWidget(self.r2)
        L.addLayout(radio)
        L.addLayout(layout)
        self.setLayout(L)

        self.connect(okB,SIGNAL("clicked()"),self.okClicked)
        self.connect(cancel,SIGNAL("clicked()"),self.cancelClicked)

    def okClicked(self):
        self.accept()
    def cancelClicked(self):
        self.reject()



class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.info=getData()
        self.man=[False,0,0]
        self.initUI()
        self.timer=QBasicTimer()
        self.timer.start(100,self)
        self.state=0
        self.node=None
        self.time=0
        

    def initUI(self):
        
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Simple Test')
        self.show()

        
    

    def timerEvent(self,event):        
        updateData(self.info)
        self.repaint()
        if self.man[0]==1:
            self.man[2]+=5
            if self.man[2]>=600:
                self.man=[False,0,0]
        if self.man[0]==2:
            self.man[3]+=.05
            self.man[1]=200*cos(self.man[3])+300
            self.man[2]=200*sin(self.man[3])+300

        self.time=(self.time+1)%3
        if self.man[0]==1 or self.man[0]==2:
            for s in self.info:
                if  sqrt( (s.x-self.man[1])**2 + (s.y-self.man[2])**2 ) < 75:
                    s.motion+=10
                if self.time==0:
                    s.motion-=10
                    if s.motion < 0:
                        s.motion=0
                if s.motion > 100:
                    s.motion = 100
        self.timer.start(15,self)

    def paintEvent(self, e):
        qp=QPainter()
        qp.begin(self)

        br=QBrush(Qt.SolidPattern)
        br.setColor(Qt.white)
        r=QRect(0,0,1000,1000)
        qp.fillRect(r,br)
        if self.state==0:
            for s in self.info:
                x=int(s.x)
                y=int(s.y)

                c=QRect(x-2.5,y-2.5,10,10)
                br.setColor(Qt.white)
                if(s.motion>0):
                    br.setColor( QColor(255,255-s.motion*2.55,0) )
                qp.setBrush(br)
                qp.drawEllipse(c)

                
                q=QRect(x,y,5,5)
                brush=QBrush(Qt.SolidPattern)
                if(s.onoff==1):
                    brush.setColor(Qt.black)
                else:
                    brush.setColor(Qt.blue)
                qp.setBrush(brush)
                qp.fillRect(q,brush)

            if self.man[0]:
                m=QRect(self.man[1],self.man[2],10,4)
                brush=QBrush(Qt.SolidPattern)
                brush.setColor(Qt.green)
                qp.fillRect(m,brush)
        else:
            for s in self.info:
                x=int(s.x)
                y=int(s.y)

                c=QRect(x-2.5,y-2.5,10,10)
                br.setColor(Qt.white)
                if(s.motion>0):
                    br.setColor( QColor(255,255-s.motion*2.55,0) )
                qp.setBrush(br)
                qp.drawEllipse(c)

                
                q=QRect(x,y,5,5)
                brush=QBrush(Qt.SolidPattern)
                if(s.onoff==1):
                    brush.setColor(Qt.black)
                else:
                    brush.setColor(Qt.blue)
                qp.setBrush(brush)
                qp.fillRect(q,brush)


                
                q=QRect(x,y,5,5)
                brush=QBrush(Qt.SolidPattern)
                if(s.onoff==1):
                    brush.setColor(Qt.black)
                else:
                    brush.setColor(Qt.blue)

                for n in self.node.neighbors:
                    if n == s:
                        brush.setColor(Qt.green)
                qp.setBrush(brush)
                qp.fillRect(q,brush)

            if self.man[0]:
                m=QRect(self.man[1],self.man[2],10,4)
                brush=QBrush(Qt.SolidPattern)
                brush.setColor(Qt.green)
                qp.fillRect(m,brush)

        qp.end()
        

    
    def mousePressEvent(self,event):
        if event.button()==1 :
            for s in self.info:
                if s.x<=event.x()<=s.x+5 and s.y<=event.y()<=s.y+5:
                    self.state=1
                    self.node=s
                    self.repaint()
                    b=infoMessage(s)
                    b.exec_()
        if event.button()==2:
            b=testMenu()
            if b.exec_():
                if b.r1.isChecked():
                    self.man=[1,300,0]
                if b.r2.isChecked():
                    self.man=[2,500,300,0]
            else:
                self.man=[False,0,0]



class Node():

    def __init__(self,x,y,data):
        self.x=x
        self.y=y
        self.activated=data[u'activated']
        self.addr=data[u'addr']
        self.connected=data[u'connected']
        self.dimming=data[u'dimming']
        self.euid=data[u'euid']
        self.fw_version=data[u'fw_version']
        self.groups=data[u'groups']
        self.onoff=data[u'onoff']
        self.pm_fw_version=data[u'pm_fw_version']
        self.scenes=data[u'scenes']
        self.sensor_capabilities=data[u'sensor_capabilities']
        self.sensor_fw_version=data[u'sensor_fw_version']
        self.subscriptions=data[u'subscriptions']
        self.neighbors=[]
        self.motion=0

    def update(self,other):
        self.x=other.x
        self.y=other.y
        self.activated=other.activated
        self.addr=other.addr
        self.connected=other.connected
        self.dimming=other.dimming
        self.fw_version=other.fw_version
        self.groups=other.groups
        self.onoff=other.onoff
        self.pm_fw_version=other.pm_fw_version
        self.scenes=other.scenes
        self.sensor_capabilities=other.sensor_capabilities
        self.sensor_fw_version=other.sensor_fw_version
        self.subscriptions=other.subscriptions

        
    def __cmp__(self,other):
        return cmp(self.euid,other.euid)

    def __str__(self):
        s=""
        s+="X: "+str(self.x)+" Y: "+str(self.y)+"\nActivated: "+str(self.activated)+"\nAddr: "+str(self.addr)+"\nConnected: "+str(self.connected)+"  \nDimming: "+str(self.dimming)
        s+="  \nEUID: "+str(self.euid)+"  \nfw_verion: "+str(self.fw_version)+"  \ngroups: "+str(self.groups)+"  \nonoff: "+str(self.onoff)+"  \npm_fw_version: "+str(self.pm_fw_version)
        s+="  \nscenes: "+str(self.scenes)+"  \nsensor_capabilities: "+str(self.sensor_capabilities)+"  \nsensor_fw_version: "+str(self.sensor_fw_version)
        s+="  \nsubscriptions: "+str(self.subscriptions)
        s+="\nMotion Level Detected:"+str(self.motion)
        s+="\nNeighbors:"
        for i in self.neighbors:
            loss= 20*log10( sqrt( (self.x/6-i.x/6)**2  + (self.y/6-i.y/6)**2  )  ) +20*log10(2.4*(10**9)) + 20*log10(4*pi/(3*(10**8)))
            s+="\n"+str(i.euid)+"\tFSPL: "+str(loss)
        return s

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
