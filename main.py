from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
from threading import Thread
import csv

inventory = {"gold":0,"wood":0}

global window

class Screen(QMainWindow):
    def start(self):
        super(Screen,self).__init__()
        self.setGeometry(300,300,600,600)
        self.setWindowTitle("DONT LET THE COLD GET TO YOU")
        self.setStyleSheet("background: #161219;")
        self.widgets = {"play": Button(0,"Play",(200,200)).butt}

        self.show()
    
    def mainscreen(self):
        self.warmth = 100
        self.widgets = {"warmthmeter" : QLabel(f"Warm: {self.warmth}",self),
                        "stoke fire" : Button(6,"Stoke Fire", (0,20)).butt,
                        "inventory" : Button(0,"Inventory", (0,120)).butt,
                        "getwood" : Button(6,"Get Wood", (0,230)).butt}
    
        self.widgets["warmthmeter"].setStyleSheet(
                   '''
            *{
            color: white;
            font-family: 'shanti';
            font-size: 10px;
            border-radius: 40px;
            padding: 15px 0;
            margin-top: 20px}
            '''
        )
        self.show()
        self.main()
    
    def clearscreen(self):
        for key, value in self.widgets.items():
            value.hide()
        self.widgets = {}
        
    def coldness(self):
        while self.warmth > 0:
            self.warmth -= 2
            time.sleep(1)
            self.widgets["warmthmeter"].setText(f"Warm: {self.warmth}")
        self.close()

    def main(self):
        Thread(target=self.coldness,daemon=True).start()

    

app = QApplication(sys.argv)
window = Screen()
class InventoryScreen(QWidget):
    def __init__(self):
        super().__init__()
        win = QVBoxLayout()
#the first tuple of (key,value) defines the variables to return, the second assigns them to the key and value in said dictionary
        for key,value in inventory.items(): 
            win.addWidget(QLabel(f"{key}:{value}"))

class Text:
    def __init__(self, text,pos,size):
        self.label = QLabel(text,window)
        self.label.move(*pos)
        self.label.setStyleSheet(
            "*{"+
            f'''color: white;
            font-family: 'shanti';
            font-size: {size}px;
            border-radius: 40px;
            padding: 15px 0;
            margin-top: 20px'''
            +"}")
        self.label.setFixedSize(size*4,size*4)
            
            
class Button():
    def __init__(self, cooldown, text,pos):
        self.butt = QPushButton(text,window)
        
        self.text = text
        self.butt.move(*pos)
        self.cooldown = self.orgcooldown= cooldown
        self.cooldownstate = True
        self.butt.setFixedSize(200,100)
        self.butt.setStyleSheet(
        #setting variable margins
        '''
        *{border: 4px solid '#BC006C';
        color: white;
        font-family: 'shanti';
        font-size: 15px;
        border-radius: 40px;
        padding: 15px 0;
        margin-top: 20px}
        *:hover{
            background: '#BC006C'
        }
        '''
        )
        
        self.butt.setCursor(QCursor(Qt.PointingHandCursor))
        self.butt.clicked.connect(self.clicked)
    
    def clicked(self):
        if self.cooldownstate:
            match self.text:
                case "Stoke Fire":
                    if inventory["wood"] > 0:
                        inventory["wood"] -= 1
                        window.warmth = 100
                    else:
                        def nowood():
                            self.cooldownstate = False
                            self.butt.setText("not enough wood")
                            time.sleep(1)
                            self.butt.setText("Stoke Fire")
                            self.cooldownstate = True
                        Thread(target=nowood, daemon = True).start()
                        return

                case "Inventory":
                    window.inventorywin = InventoryScreen()

                case "Get Wood":
                    inventory["wood"] += 1

                case "Play":
                    window.clearscreen()
                    window.mainscreen()
                    
            Thread(target=self.timer,daemon=True).start()

    def timer(self):
        self.cooldownstate = False
        while self.cooldown > 0:
            self.butt.setText(f"{self.cooldown}")
            time.sleep(1)
            self.cooldown -= 1
        self.cooldownstate = True
        self.butt.setText(self.text)
        self.cooldown = self.orgcooldown

if __name__ == "__main__":
    window.start()
    sys.exit(app.exec_())