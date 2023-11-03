from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from tools import *
import sys
inventory = {"gold":75,"wood":0}
shop = {
    "axes": {
    "basic axe": 5,
    "silver axe": 20,
    "gold axe": 40,
    }
    
}

class Screen(QMainWindow):
    def __init__(self):
        super(Screen,self).__init__()
        self.setGeometry(300,300,600,600)
        self.setWindowTitle("DONT LET THE COLD GET TO YOU")
        self.setStyleSheet("background: #161219;")
        self.warmth = 100
        self.mainloopran = False
        self.warmthtimer = QTimer()
        self.warmthtimer.setInterval(2000)
        self.warmthtimer.timeout.connect(self.mainloop)
        self.widgets = {
            "title": QLabel(self),
            "play": Button(self,"Play",(200,200),func=self.mainscreen)
            }
        self.forests = ["Oak Forest","Spruce Forest","Max"]
        self.forestlevel = 0
        self.widgets["title"].setPixmap(QPixmap("image.png"))
        self.widgets["title"].setFixedSize(450,200)
        self.widgets["title"].move(100,0)
        self.show()
        
        
    def screen(func):#This updates the different frames so that each widget can be seen
        def wrapper(self):
            self.clearscreen()
            func(self)
            self.update()
        return wrapper


    #region MAIN SCREEN
    def mainscreen(self):
        self.clearscreen()
        if not self.mainloopran:
            
            self.warmthtimer.start()
            self.mainloopran = True
            self.mainwidgets = {
                            "forest":Text(self,self.forests[self.forestlevel],(125,10),15),
                            "warmthmeter": Progressbar(self, (200,60),"Warmth"),
                            "stoke fire" : Button(self,"Stoke Fire", (200,110),func=self.stokeFire),
                            "getwood" : Button(self,"Get Wood", (200,190),func=self.getWood),
                            "inventory" : Button(self,"Inventory", (200,270),func=self.inventoryscreen),
                            "shop": Button(self,"Shop",(200,350),func=self.shopscreen),
            }
        self.update(True)
        

    #MAINSCREEN BUTTON FUNCS
    def stokeFire(self):
        def stoke():
            self.warmth = 100

        if inventory["wood"] > 0:
            inventory["wood"] -= 1
        else:
            self.mainwidgets["stoke fire"].notice(1,"Not Enough Wood")
            return
        self.mainwidgets["stoke fire"].on_Cooldown(3, "Stoking Fire")
        self.mainwidgets["stoke fire"].worker.finished.connect(lambda:self.mainwidgets["warmthmeter"].setValue(100))
        self.mainwidgets["stoke fire"].worker.finished.connect(stoke)

        
            
    def getWood(self):
        def add_wood(): inventory["wood"] += 1
        cooldown = 10
        for index,i in enumerate(shop["axes"].keys()):
            if i not in inventory.keys():
                break
            cooldown -= (index+1)*1.5
            print(cooldown)
            
        self.mainwidgets["getwood"].on_Cooldown(cooldown, "Gathering Wood")
        self.mainwidgets["getwood"].worker.finished.connect(add_wood)
    
    #endregion MAIN SCREEN
        
    @screen
    def inventoryscreen(self):
        self.widgets = {"back": Button(self,"Back",(10,10),func=self.mainscreen),
                        "inventoryscrollbox" : Scrollbox(self,(10,90),(580,500))}
        self.widgets["inventoryscrollbox"].addText([f"{value} {key}" for key,value in inventory.items()])
        
            

    @screen
    def shopscreen(self):
        self.widgets = {
            "back":Button(self,"Back",(10,10),size=(100,50),func=self.mainscreen),
            "sellwood" : Button(self,"Sell Wood",(290,10),func=self.sellWood),
            "shopbox" : Scrollbox(self,(10,90),(580,500)),

        }
        axe = self.getAxe()
        self.shopboxwidgets = {
            "upgrade axe": [Text(self,"Upgrade Axe"),Button(self,"Max Upgrade Reached" if axe == "max" else f"{axe.capitalize()}: {shop['axes'][axe]} Gold",func=self.upgradeAxe)],
            #"upgrade forest" : [Text(self,"Upgrade Forest"), Button(self,"Forest",func=self.forest)]
        }
        if axe == "max":
            self.shopboxwidgets["upgrade axe"][1].resetStyleSheet("#737373",hover=False)
            self.shopboxwidgets["upgrade axe"][1].setEnabled(False)
        for row in self.shopboxwidgets.values():
            self.widgets["shopbox"].layout.addRow(*row)
    
    def sellWood(self):
        if inventory["wood"] > 0:
            gold = 2 ** self.forestlevel
            inventory["wood"] -= 1
            inventory["gold"] += gold
            self.widgets["sellwood"].notice(0.5,f"Gold + {gold}")
        
        else:
            self.widgets["sellwood"].notice(1,"Not Enough Wood")
    
    def upgradeAxe(self):
        axe = self.getAxe()
        upgradeaxe = lambda: self.shopboxwidgets["upgrade axe"][1]
        if axe == "max":
            upgradeaxe().notice(0.5,"Max Upgrade Reached")
            return
        inventory[axe] = 1
        newaxe = self.getAxe()
        if newaxe == "max":
            upgradeaxe().setText("Max Upgrade Reached")
            upgradeaxe().resetStyleSheet("#737373",False)
            upgradeaxe().setEnabled(False)
            return
        
        upgradeaxe().notice(0.5,"Axe Upgraded",f"{newaxe.capitalize()}: {shop['axes'][newaxe]} Gold")
        
    def forest(self):
        if self.forests[self.forestlevel + 1] == "Max":
            self.widgets["upgrade forest"].notice(0.5,"Max Forest Reached")
            return
        
        self.forestlevel += 1
        if self.forests[self.forestlevel + 1] == "Max":
            self.widgets["upgrade forest"].notice(0.5,"Max Forest Reached")
            return
        
        self.widgets["upgrade forest"].notice(0.5,"Forest Upgraded",f"Upgrade Forest: {10 + 10*self.forestlevel}")
    
    def getAxe(self):
        for axename in shop["axes"].keys():
            if axename in inventory:
                continue
            return axename
        return "max"
        
    @screen
    def losescreen(self):
        self.setStyleSheet("background: black;")
        self.widgets = {
            "title": QLabel(self),
            "exit" : Button(self,"Exit", (100,260),func=quit)
        }
        self.widgets["title"].setPixmap(QPixmap("you died.png"))
        self.widgets["title"].setFixedSize(450,200)
        self.widgets["title"].move(100,0)
        
        
    def mainloop(self):
        self.warmth -= 4
        if self.warmth <= 0:
            self.warmthtimer.stop()
            self.losescreen()
        self.mainwidgets["warmthmeter"].setValue(self.warmth)
    
    
        
    def clearscreen(self):# This clears the screen and ensures that it has been deleted from the widget dictionary
        print("screen cleared")
        for value in self.widgets.values():
            value.setParent(None) # deletes the widget from the screen
        self.widgets = {} # deletes the entire widget dictionary
    
    def update(self, showmain = False):
        for key, widget in self.widgets.items():
            print(key) # To check what widgets have been loaded
            widget.show()
            
        for key,widget in self.mainwidgets.items():
            print(key)
            if showmain:
                widget.show()
            else:
                widget.hide()
        
        print()

             

                
        

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    screen = Screen()
    sys.exit(app.exec_())