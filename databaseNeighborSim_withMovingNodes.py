import sys
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import requests
from pprint import pprint
import json
import random
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DBNode(Base):
    __tablename__ = 'sim_devices'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=func.now())
    EUID = Column(Text, nullable=False)
    x = Column(Integer, nullable=True)
    y = Column(Integer, nullable=True)


def populateNeighbors(nodes):
    for n in nodes:
        l={}
        for n1 in nodes:
            if n != n1 :
                l[100*sqrt( (n1.x-n.x)**2 +  (n1.y-n.y)**2 )+(10**(-14))*n1.euid]=n1 #note: we add the euid so distances are unique
        sort=sorted(l)
        tot=[]
        for i in range(16):
            tot.append(l[sort[i]])
        n.neighbors=tot
        n.setSignalLoss()
            
def getData():
    r=requests.get('http://localhost:8080/fixtures')
    fixtures=r.json()
    l=[]
    x=-30
    y=10
    for s in fixtures:
        l.append(Node(None,None,s))
    
    for s in l:
        node = session.query(DBNode).filter_by(EUID=s.euid).first()
        s.x=node.x
        s.y=node.y

    populateNeighbors(l)

    return ( l )



def updateData(data): #using this rather than getData tries to keep the nodes the same throughout the program
    r=requests.get('http://localhost:8080/fixtures') #also, it avoids recalculating neighbors
    fixtures=r.json()
    l=[]
    for s in fixtures:
        l.append(Node(None,None,s))

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
        self.label=QLabel(node.toString())
        L.addWidget(self.label)
        L.addLayout(layout)
        self.setLayout(L)

        self.connect(okB,SIGNAL("clicked()"),self.okClicked)
        

    def okClicked(self):
        self.accept()
        



class testMenu(QDialog):

    def __init__(self,parent=None):
        super(testMenu,self).__init__(parent)

        self.noTestClicked=False
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
        self.r3=QRadioButton("Man Walking: Random Path")
        radio.addWidget(self.r1)
        radio.addWidget(self.r2)
        radio.addWidget(self.r3)
        L.addLayout(radio)
        L.addLayout(layout)
        self.setLayout(L)

        self.connect(okB,SIGNAL("clicked()"),self.okClicked)
        self.connect(cancel,SIGNAL("clicked()"),self.cancelClicked)

    def okClicked(self):
        self.accept()
    def cancelClicked(self):
        self.noTestClicked=True
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
        self.moveNode=None

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
        if self.man[0]==3:
            theta=2*pi*random.random()
            self.man[1]+=7*cos(theta)
            self.man[2]+=7*sin(theta)

        self.time=(self.time+1)%3
        if self.man[0]==1 or self.man[0]==2 or self.man[0]==3:
            for s in self.info:
                if  sqrt( (s.x-self.man[1])**2 + (s.y-self.man[2])**2 ) < 75:
                    s.motion+=10
                if s.motion > 100:
                    s.motion = 100
        for s in self.info:
            if self.time==0:
                s.motion-=10
                if s.motion < 0:
                    s.motion=0

        x=[]
        if self.time==0:
            for n in self.info:
                x.append({"euid":n.euid,"neighbors":n.neighborLoss,"motion":n.motion})
            requests.post('http://localhost:8080/fixtures',json.dumps(x))
        self.timer.start(5,self)

    def paintEvent(self, e): #this is called every self.repaint(), and basically every time the window is changed.
        qp=QPainter()        #calling paintEvent as a method directly does not draw anything, repaint has to be used
        qp.begin(self)

        br=QBrush(Qt.SolidPattern)
        br.setColor(Qt.white)
        r=QRect(0,0,1000,1000)
        qp.fillRect(r,br)
        if self.state==0: #self.state refers to whether or not to note neighbors, 0 means don't, 1 means do
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
                
        elif self.state==1:
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
        

    
    def mousePressEvent(self,event): #event.button() returns 1 on left click, 2 on right, and 4 on middle mouse
        self.moveNode=None
        if event.button()==1 :
            for s in self.info:
                if sqrt( (s.x-event.x() )**2+ (s.y-event.y())**2 ) <=10:
                    self.state=1
                    self.node=s
                    self.repaint()
                    b=infoMessage(s)
                    b.exec_()
                    break
                else:
                    self.node = None
                    self.state=0
        if event.button()==2:
            b=testMenu()
            if b.exec_():
                if b.r1.isChecked():
                    self.man=[1,300,0]
                if b.r2.isChecked():
                    self.man=[2,500,300,0]
                if b.r3.isChecked():
                    self.man=[3,300,300]
            else:
                if b.noTestClicked:
                    self.man=[False,0,0]

        if event.button()==4:
            for s in self.info:
                if sqrt( (s.x-event.x() )**2+ (s.y-event.y())**2 ) <=10:
                    self.moveNode=s
    

    def mouseReleaseEvent(self,event): #this gets called on all clicks, not just click & drags
        if self.moveNode is not None:
            if  sqrt( (self.moveNode.x-event.x() )**2+ (self.moveNode.y-event.y())**2 ) <=10:
                pass
            else:
                self.moveNode.x=event.x()
                self.moveNode.y=event.y()
                node = session.query(DBNode).filter_by(EUID=self.moveNode.euid).first()
                node.x=self.moveNode.x
                node.y=self.moveNode.y
                session.commit()
                populateNeighbors(self.info)
                self.repaint()

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
        self.neighborLoss={}

    def update(self,other):
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


    def setSignalLoss(self):
        for i in self.neighbors:
            loss= 20*log10( sqrt( (self.x/6-i.x/6)**2  + (self.y/6-i.y/6)**2  )  ) +20*log10(2.4*(10**9)) + 20*log10(4*pi/(3*(10**8)))
            self.neighborLoss[i.euid]=loss
        
    def __cmp__(self,other):
        return cmp(self.euid,other.euid)

    def toString(self):
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

    def __str__(self):
        return(str(self.euid))

if __name__ == '__main__':
    db_path = "sim.db"
    engine = create_engine('sqlite:///' + db_path)
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    session = DBSession()

    Base.metadata.create_all(engine)

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
