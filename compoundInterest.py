import sys
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Form(QDialog):




    def __init__(self, parent=None):
        super(Form,self).__init__(parent)


        self.principal=QDoubleSpinBox()
        self.rate=QDoubleSpinBox()
        self.years=QSpinBox()
        self.amount=QLabel("")
        self.principal.setRange(0,100000)
        
        self.years.setValue(2)
        self.rate.setValue(5.25)
        self.principal.setValue(2000)
        self.amount.setText("2215.51")
        
        self.years.setSuffix(" years")
        self.principal.setSuffix(" $")
        self.rate.setSuffix(" %")
        
        aLabel=QLabel("Amount")
        pLabel= QLabel("Principal:")
        rLabel= QLabel("Rate:")
        yLabel= QLabel("Years:")

        layout=QGridLayout()
        layout.addWidget(pLabel,0,0)
        layout.addWidget(rLabel,1,0)
        layout.addWidget(yLabel,2,0)
        layout.addWidget(aLabel,3,0)

        layout.addWidget(self.principal,0,1)
        layout.addWidget(self.rate,1,1)
        layout.addWidget(self.years,2,1)
        layout.addWidget(self.amount,3,1)

        self.setLayout(layout)

        self.connect(self.principal,SIGNAL("valueChanged(double)"),self.UiUpdate)
        self.connect(self.years,SIGNAL("valueChanged(int)"),self.UiUpdate)
        self.connect(self.rate,SIGNAL("valueChanged(double)"),self.UiUpdate)
        
        self.setWindowTitle("Interest")


    def UiUpdate(self):
        s=str( self.principal.value()*(1+(self.rate.value()/100))**self.years.value())
        s,t=s.split('.')
        s=s+"."+t[0:2]
        self.amount.setText(s)



app=QApplication(sys.argv)
form=Form()
form.show()
app.exec_()
