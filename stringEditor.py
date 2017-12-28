import sys
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class removeDialog(QDialog):

    def __init__(self,parent=None):
        super(removeDialog,self).__init__(parent)

        layout = QHBoxLayout()
        okB=QPushButton("&OK")
        cancel = QPushButton("Cancel")
        layout.addWidget(okB)
        layout.addWidget(cancel)
        self.setWindowTitle("Alert:")


        L = QVBoxLayout()
        label=QLabel("Do you want to delete the selected item?")
        L.addWidget(label)
        L.addLayout(layout)
        self.setLayout(L)

        self.connect(okB,SIGNAL("clicked()"),self.okClicked)
        self.connect(cancel,SIGNAL("clicked()"),self.cancelClicked)


    def okClicked(self):
        self.accept()


    def cancelClicked(self):
        self.reject()




class addDialog(QDialog):

    def __init__(self,word,parent=None):
        super(addDialog,self).__init__(parent)

        layout = QHBoxLayout()
        okB=QPushButton("&OK")
        cancel = QPushButton("Cancel")
        layout.addWidget(okB)
        layout.addWidget(cancel)
        self.setWindowTitle(word)

        self.text = QLineEdit()
        L = QVBoxLayout()
        label=QLabel(word+":")
        L.addWidget(label)
        L.addWidget(self.text)
        L.addLayout(layout)
        self.setLayout(L)

        self.connect(okB,SIGNAL("clicked()"),self.okClicked)
        self.connect(cancel,SIGNAL("clicked()"),self.cancelClicked)


    def okClicked(self):
        self.accept()


    def cancelClicked(self):
        self.reject()



class StringListDialg(QDialog):

    def __init__(self,name,s,parent=None):
        super(StringListDialg,self).__init__(parent)
        self.name=name
        self.stringList=s
        self.sList=QListWidget()
        self.sList.addItems(s)
        self.sList.setCurrentRow(0)
        layout=QHBoxLayout()
        layout.addWidget(self.sList)
        buttonLayout=QVBoxLayout()

        add=QPushButton("&Add")
        edit=QPushButton("&Edit")
        rem=QPushButton("&Remove")
        up=QPushButton("&Up")
        down=QPushButton("&Down")
        sort=QPushButton("&Sort")
        close=QPushButton("&Close")

        buttonLayout.addWidget(add)
        buttonLayout.addWidget(edit)
        buttonLayout.addWidget(rem)
        buttonLayout.addWidget(up)
        buttonLayout.addWidget(down)
        buttonLayout.addWidget(sort)
        buttonLayout.addWidget(close)
        self.setWindowTitle("Edit "+name+" List")

        layout.addLayout(buttonLayout)
        self.setLayout(layout)


        self.connect(add,SIGNAL("clicked()"),self.addClicked)
        self.connect(edit,SIGNAL("clicked()"),self.editClicked)
        self.connect(rem,SIGNAL("clicked()"),self.remClicked)
        self.connect(up,SIGNAL("clicked()"),self.upClicked)
        self.connect(down,SIGNAL("clicked()"),self.downClicked)
        self.connect(sort,SIGNAL("clicked()"),self.sortClicked)
        self.connect(close,SIGNAL("clicked()"),self.closeClicked)




    def addClicked(self):
        b=addDialog("Add "+self.name)
        if b.exec_():
            self.stringList.append(b.text.text())
            self.sList.addItem(b.text.text())
            
    def editClicked(self):
        b=addDialog("Edit "+self.name)
        c=self.sList.currentRow()
        if b.exec_():
            self.stringList[c]=(b.text.text())
            self.sList.clear()
            self.sList.addItems(self.stringList)
            self.sList.setCurrentRow(c)


    def remClicked(self):
        b=removeDialog()
        if b.exec_():
            c=self.sList.currentRow()
            del(self.stringList[c])
            self.sList.clear()
            self.sList.addItems(self.stringList)
            self.sList.setCurrentRow(c)

    def upClicked(self):
        self.sList.setCurrentRow(self.sList.currentRow()-1)

    def downClicked(self):
        self.sList.setCurrentRow(self.sList.currentRow()+1)

    def sortClicked(self):
        self.sList.sortItems()
        self.stringList.sort()

    def closeClicked(self):
        self.reject()




if __name__=="__main__":
    fruit=["Banana","Apple","Guava","Mango","Honeydew Melon","Date","Orange",'Papaya','Cherry','Nectarine','Plum','Strawberry','Fig','Watermelon']
    app=QApplication(sys.argv)
    form=StringListDialg("Fruit",fruit)
    form.exec_()
    print "\n".join([unicode(x) for x in form.stringList])
