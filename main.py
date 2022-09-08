from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,os,time,csv
from threading import Thread

inventory = {"gold":0,"wood":0}

class Screen(QMainWindow):
    def __init__(self):
        super(Screen,self).__init__()
        self.mainscreenran = False
        self.setGeometry(300,300,600,600)
        self.setWindowTitle("DONT LET THE COLD GET TO YOU")
        self.setStyleSheet("background: #161219;")
        self.warmth = 100
        self.widgets = {
            "title": QLabel(self),
            "play": Button(self,0,"Play",(200,200))}

        self.widgets["title"].setPixmap(QPixmap("image.png"))
        self.widgets["title"].setFixedSize(450,200)
        self.widgets["title"].move(100,0)
        self.show()
    
    def mainscreen(self):
        self.reset = False
        self.widgets = {
                        
                        "warmthmeter": Progressbar(self, (200,10),"Warmth"),
                        "stoke fire" : Button(self,6,"Stoke Fire", (200,60)),
                        "inventory" : Button(self,0,"Inventory", (200,140)),
                        "getwood" : Button(self,10,"Get Wood", (200,220))}



        for value in self.widgets.values():
            value.show()
        
        if not self.mainscreenran:
            self.mainloop()
        
        self.mainscreenran = True
        self.show()

    def clearscreen(self,exceptions=[],remove = True):
        if remove:
            tempwidgets = dict(self.widgets)
            for key,value in self.widgets.items():
                if exceptions != [] and value in exceptions:
                    continue
                value.hide()
                del tempwidgets[key]
                
            self.widgets = tempwidgets
        else:
            for value in self.widgets.values():
                value.hide()
                
            
    def mainloop(self):
        self.widgets["warmthmeter"].setValue(self.warmth)
        self.widgets["warmthmeter"].timer.start()
            

    def inventoryscreen(self):
        self.clearscreen(remove=False)
        self.widgets["warmthmeter"].hide()
        self.widgets["back"] = Button(self,0,"Back",(10,10))
        self.widgets["back"].show()
        count = 0
        for key,value in inventory.items():
            count += 1
            self.widgets[key] = Text(self,f"{key} : {value}",(10,100+25*count),10)
            self.widgets[key].show()

class Progressbar(QProgressBar):
    def __init__(self,window, pos,text= "", backgroundcolor = "orange", barcolor = "red", min = 0, max = 100):
        super().__init__(window)
        self.win = window
        self.setMinimum(min)
        self.setMaximum(max)
        self.move(*pos)
        self.setFixedSize(200,30)
        self.setFormat(text)
        self.setStyleSheet("QProgressBar {"
                           f"background-color: {backgroundcolor};"
                           "color: white;"
                           "border-color: orange;"
                           "border-radius: 2px;"
                           "text-align: center; }"

                           "QProgressBar::chunk {"
                           "border-radius: 2px;"
                           f"background-color: {barcolor};"+"}")
        
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.counter)
        
    def counter(self):
        self.win.warmth -= 2
        print(self.win.warmth)
        self.win.widgets["warmthmeter"].setValue(self.win.warmth)
        
class Text(QLabel):
    def __init__(self,window, text,pos,size):
        super().__init__(text,window)
        self.move(*pos)
        self.setStyleSheet(
            "*{"+
            f'''color: white;
            font-family: 'shanti';
            font-size: {size}px;
            border-radius: 40px;
            padding: 15px 0;
            margin-top: 20px'''
            +"}")
        self.setFixedSize(size*25,size+23)         
class Button(QPushButton):
    def __init__(self,window, cooldown, text,pos,size = (200,70)):
        super().__init__(text,window)
        self.win = window
        self.texte = text
        self.move(*pos)
        self.cooldown = self.orgcooldown= cooldown
        self.cooldownstate = False
        self.setFixedSize(*size)
        self.setStyleSheet(
        #setting variable margins
        '''
        QPushButton {
        border: 4px solid #737373;
        color: white;
        font-family: shanti;
        font-size: 15px;
        border-radius: 4px;
        padding: 15px 0;
        margin-top: 0px}
        
        QPushButton::hover{
            background: #737373;
        }
        ''')
        self.qtimer = QTimer()
        self.qtimer.setInterval(1000)
        self.qtimer.timeout.connect(self.timer)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.clicked.connect(self.clicker)

    def clicker(self):
        if  not self.cooldownstate:
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
                    
                case "Back":
                    self.win.clearscreen([self.win.widgets["warmthmeter"],self.win.widgets["stoke fire"],self.win.widgets["getwood"]])
                    self.win.mainscreen()
                    
            if self.cooldown > 0:
                self.setText(str(self.cooldown))
                self.qtimer.start()

    def timer(self):
        self.cooldownstate = True
        self.cooldown -= 1
        self.setText(str(self.cooldown))
        print(self.cooldown)
        if self.cooldown == 0:
            self.cooldown = self.orgcooldown
            self.setText(self.texte)
            self.qtimer.stop()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    screen = Screen()
    sys.exit(app.exec_())
