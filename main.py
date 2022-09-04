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
        super().__init__()
        self.setGeometry(300,300,300,300)
        self.setWindowTitle("DONT LET THE COLD GET TO YOU")
        self.stokefire = Button(6,"Stoke Fire", (0,30))
        self.inventory = Button(0,"Inventory", (0,60))
        self.getwood = Button(10,"Get Wood", (0,90))
        self.warmth = 100
        self.warmthmeter = QLabel(f"Warm: {self.warmth}",self)
        self.show()
        self.main()
    
    def coldness(self):
        while self.warmth > 0:
            self.warmth -= 2
            time.sleep(1)
            self.warmthmeter.setText(f"Warm: {self.warmth}")
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
        self.setLayout(win)
        self.setWindowTitle("Inventory")
        self.setGeometry(300,300,300,300)
        self.show()


class Button:
    def __init__(self, cooldown, text, pos):
        self.butt = QPushButton(text,window)
        self.butt.move(*pos)
        self.text = text
        self.pos = pos
        self.cooldown = self.orgcooldown= cooldown
        self.butt.clicked.connect(self.clicked)
        self.cooldownstate = True

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