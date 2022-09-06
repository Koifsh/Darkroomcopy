from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
from threading import Thread
import csv

inventory = {"gold":0,"wood":0}

class Screen(QMainWindow):
    def __init__(self):
        super(Screen,self).__init__()
        self.setGeometry(300,300,600,600)
        self.setWindowTitle("DONT LET THE COLD GET TO YOU")
        self.setStyleSheet("background: #161219;")
        self.widgets = {
            "title": QLabel(self),
            "play": Button(0,"Play",(200,200),self)}

        self.widgets["title"].setPixmap(QPixmap("image.png"))
        self.widgets["title"].setFixedSize(450,200)
        self.widgets["title"].move(100,0)
        self.show()
    
    def mainscreen(self):
        self.warmth = 100
        self.widgets = {"warmthmeter" : QLabel(f"Warm: {self.warmth}",self),
                        "stoke fire" : Button(6,"Stoke Fire", (0,20),self),
                        "inventory" : Button(0,"Inventory", (0,120),self),
                        "getwood" : Button(6,"Get Wood", (0,230),self)}
    
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
        for key,value in self.widgets.items():
            value.show()

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
    
    def inventoryscreen(self):
        for key,value in inventory.items():
            self.widgets[key] = 



    



class InventoryScreen(QWidget):
    def __init__(self):
        super().__init__()
        win = QVBoxLayout()
        for key,value in inventory.items(): 
            win.addWidget(QLabel(f"{key}:{value}"))

class Text(QLabel):
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
            
            
class Button(QPushButton):
    def __init__(self, cooldown, text,pos,window):
        super().__init__(text,window)
        self.win = window
        self.texte = text
        self.move(*pos)
        self.cooldown = self.orgcooldown= cooldown
        self.cooldownstate = True
        self.setFixedSize(200,100)
        self.setStyleSheet(
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
        
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.clicked.connect(self.clicker)

    def clicker(self):
        if self.cooldownstate:
            match self.texte:
                case "Stoke Fire":
                    if inventory["wood"] > 0:
                        inventory["wood"] -= 1
                        self.win.warmth = 100
                    else:
                        def nowood():
                            self.cooldownstate = False
                            self.setText("not enough wood")
                            time.sleep(1)
                            self.setText("Stoke Fire")
                            self.cooldownstate = True
                        Thread(target=nowood, daemon = True).start()
                        return

                case "Inventory":
                    self.win.inventoryscreen()

                case "Get Wood":
                    inventory["wood"] += 1

                case "Play":
                    self.win.clearscreen()
                    self.win.mainscreen()
                    
            Thread(target=self.timer,daemon=True).start()


    def timer(self):
        self.cooldownstate = False
        while self.cooldown > 0:
            self.setText(f"{self.cooldown}")
            time.sleep(1)
            self.cooldown -= 1
        self.cooldownstate = True
        self.setText(self.texte)
        self.cooldown = self.orgcooldown

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = Screen()
    sys.exit(app.exec_())