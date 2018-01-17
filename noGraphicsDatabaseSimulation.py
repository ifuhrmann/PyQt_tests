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
    nodeList=getData()

    while True:
        updateData(nodeList)
        x=[]
        for n in nodeList:
            x.append({"euid":n.euid,"neighbors":n.neighborLoss,"motion":n.motion})
        requests.post('http://localhost:8080/fixtures',json.dumps(x))
