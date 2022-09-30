from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,time,csv
from threading import Thread
from functools import partial

inventory = {"gold":75,"wood":0}

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
        self.forest = "Oak Forest"
        self.widgets["title"].setPixmap(QPixmap("image.png"))
        self.widgets["title"].setFixedSize(450,200)
        self.widgets["title"].move(100,0)
        self.show()
    
    def mainscreen(self):
        self.reset = False
        if not self.mainscreenran:
            self.widgets = {
                            "forest":Text(self,self.forest,(125,10),15),
                            "warmthmeter": Progressbar(self, (200,60),"Warmth"),
                            "stoke fire" : Button(self,6,"Stoke Fire", (200,110)),
                            "getwood" : Button(self,10,"Get Wood", (200,190)),
                            "inventory" : Button(self,0,"Inventory", (200,270)),
                            "shop": Button(self,0,"Shop",(200,350))
                            }
            
            self.widglist = [value for value in self.widgets.values()]

        
        for value in self.widgets.values():
            value.show()

        if not self.mainscreenran:
            self.mainloop()
        
        self.mainscreenran = True
        self.show()

    def inventoryscreen(self):
        self.clearscreen(remove=False)
        self.widgets["back"] = Button(self,0,"Back",(10,10))
        self.widgets["back"].show()
        count = 0
        for key,value in inventory.items():
            count += 1
            self.widgets[key] = Text(self,f"{key} : {value}",(150,50+25*count),10)
            self.widgets[key].show()

    def shopscreen(self):
        self.clearscreen(remove=False)
        self.widgets["back"] = Button(self,0,"Back",(10,10))
        self.widgets["sell"] = Button(self,0,"Sell Wood",(10,520))
        self.widgets["upgrade axe"] = Button(self,0,"Axe",(100,100))
        for widget in ["back","sell","upgrade axe"]:
            self.widgets[widget].show()
        
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
        self.setValue(self.win.warmth)
        self.update()
        if self.win.warmth == 0:
            self.win.close()

class Text(QLabel):
    def __init__(self,window, text,pos,size):
        super().__init__(text,window)
        self.move(*pos)
        self.setAlignment(Qt.AlignCenter)
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
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.clicked.connect(self.clicker)
        self.qtimer.timeout.connect(self.timer)
        
        if text == "Axe":
            self.setText(self.getItem("Axe"))

    def clicker(self):
        if  not self.cooldownstate:
            match self.texte:
                case "Stoke Fire":
                    if inventory["wood"] > 0:
                        inventory["wood"] -= 1
                        self.win.warmth = 100
                    else:
                        self.notice(1,"Not Enough Wood",self.texte)
                        
                case "Inventory":
                    self.win.inventoryscreen()

                case "Get Wood":
                    inventory["wood"] += 1
                    if "basic axe" in inventory:
                        self.cooldown,self.orgcooldown = 6,6

                case "Play":
                    self.win.clearscreen()
                    self.win.mainscreen()
                    
                case "Back":
                    self.win.clearscreen(self.win.widglist)
                    self.win.mainscreen()
                    
                case "Shop":
                    self.win.shopscreen()
                
                case "Sell Wood":
                    if inventory["wood"] > 0:
                        inventory["wood"] -= 1
                        inventory["gold"] += 1
                        self.notice(0.5,"Gold + 1",self.texte)
                        
                    else:
                        self.notice(1,"Not Enough Wood",self.texte)

                case "Axe":
                    self.setText(self.getItem("Axe"))
                    print(inventory)
                    if self.axename == "Max":
                        self.notice(0.5,"Max Upgrade Reached","Max")
                    
                    elif inventory["gold"] < self.cost:
                        self.notice(1,"Not Enough Gold",self.getItem("Axe"))

                    else:
                        inventory[self.axename] = 1
                        self.win.widgets["getwood"].orgcooldown -= 2
                        inventory["gold"] -= self.cost
                        self.notice(0.5,"Bought",self.getItem("Axe"))
                        
            if self.cooldown > 0:
                self.setText(str(self.cooldown))
                self.qtimer.start()
        
    def getItem(self,type):
        if type == "Axe":
            for index,i in enumerate(["Basic Axe", "Bronze Axe", "Silver Axe","Max"]):
                if i not in inventory:
                    self.axename = i
                    self.cost = 5 * (2 ** index)
                    if self.axename != "Max":
                        return f"{self.axename}: {self.cost}"
                    else:
                        self.cooldownstate = True
                        return "Max"
                        
        
    def notice(self, sleeptime, message, orgmessage):
        def noticethread():
            self.cooldownstate = True
            self.setText(message)
            time.sleep(sleeptime)
            self.setText(orgmessage)
            self.cooldownstate = False
        Thread(target=noticethread, daemon = True).start()
        
    def timer(self):
        self.cooldownstate = True
        self.cooldown -= 1
        self.setText(str(self.cooldown))
        if self.cooldown == 0:
            self.cooldown = self.orgcooldown
            self.setText(self.texte)
            self.qtimer.stop()
            self.cooldownstate = False

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    screen = Screen()
    sys.exit(app.exec_())