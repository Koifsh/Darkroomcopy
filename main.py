from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from tools import *
import sys
inventory = {"gold":75,"wood":0}

class Screen(QMainWindow):
    def __init__(self):
        super(Screen,self).__init__()
        self.setGeometry(300,300,600,600)
        self.setWindowTitle("DONT LET THE COLD GET TO YOU")
        self.setStyleSheet("background: #161219;")
        self.warmth = 100
        self.widgets = {
            "title": QLabel(self),
            "play": Button(self,"Play",(200,200),func=self.mainscreen)
            }
        self.widgets["play"].clicked.connect(self.mainloop())
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
    @screen
    def mainscreen(self):
        self.widgets = {
                        "forest":Text(self,self.forests[self.forestlevel],(125,10),15),
                        "warmthmeter": Progressbar(self, (200,60),"Warmth"),
                        "stoke fire" : Button(self,"Stoke Fire", (200,110),func=self.stokeFire),
                        "getwood" : Button(self,"Get Wood", (200,190),func=self.getWood),
                        "inventory" : Button(self,"Inventory", (200,270),func=self.inventoryscreen),
                        "shop": Button(self,"Shop",(200,350),func=self.shopscreen),
        }
    #MAINSCREEN BUTTON FUNCS
    def stokeFire(self):
        if inventory["wood"] > 0:
            inventory["wood"] -= 1
            self.warmth = 100
        else:
            self.widgets["stoke fire"].notice(1,"Not Enough Wood")
        self.widgets["stoke fire"].on_Cooldown(5)
        
            
    def getWood(self):
        inventory["wood"] += 1
        if "basic axe" in inventory:
            self.cooldown,self.orgcooldown = 6,6
        self.widgets["getwood"].on_Cooldown(3)
    
    #endregion MAIN SCREEN
        
    @screen
    def inventoryscreen(self):
        self.widgets = {
            {"back": Button(self,"Back",(10,10),func=self.mainscreen)} | 
            {key : Text(self,f"{key} : {value}",(150,50+25*index),10) for index,(key,value) in enumerate(inventory.items())}
            }

    @screen
    def shopscreen(self):
        self.widgets = {
            "back":Button(self,"Back",(10,10),func=self.mainscreen),
            "sellwood" : Button(self,"Sell Wood",(10,520),func=self.sellWood),
            "upgrade axe": Button(self,"Axe",(100,100),func=self.getAxe),
            "upgrade forest" : Button(self,0,"Forest",(390,520))
        }
    
    def sellWood(self):
        if inventory["wood"] > 0:
            gold = 2 ** self.forestlevel
            inventory["wood"] -= 1
            inventory["gold"] += gold
            self.widgets["sellwood"].notice(0.5,f"Gold + {gold}")
        
        else:
            self.notice(1,"Not Enough Wood")
    
    def upgradeAxe(self):
        self.widgets["upgrade axe"].setText(self.getItem("Axe"))
        print(inventory)
        if self.axename == "Max":
            self.notice(0.5,"Max Upgrade Reached","Max")
    

    
    #
    
    
    def getAxe(self,type):
        for index,i in enumerate(["Basic Axe", "Bronze Axe", "Silver Axe","Max"]):
            if i not in inventory:
                self.axename = i
                self.cost = 5 * (2 ** index)
                if self.axename != "Max":
                    return f"{self.axename}: {self.cost}"
                else:
                    self.cooldownstate = True
                    return "Max"
            
    def mainloop(self):
        self.widgets["warmthmeter"].setValue(self.warmth)
        self.widgets["warmthmeter"].timer.start()
        
    def clearscreen(self):# This clears the screen and ensures that it has been deleted from the widget dictionary
        print("screen cleared")
        for value in self.widgets.values():
            value.setParent(None) # deletes the widget from the screen
        self.widgets = {} # deletes the entire widget dictionary
    
    def update(self):
        for key, widget in self.widgets.items():
            print(key) # To check what widgets have been loaded
            widget.show()
        print()

             

                    

            #     case "Axe":
            #         self.setText(self.getItem("Axe"))
            #         print(inventory)
            #         if self.axename == "Max":
            #             self.notice(0.5,"Max Upgrade Reached","Max")
                    
            #         elif inventory["gold"] < self.cost:
            #             self.notice(1,"Not Enough Gold",self.getItem("Axe"))

            #         else:
            #             inventory[self.axename] = 1
            #             self.win.widgets["getwood"].orgcooldown -= 2
            #             inventory["gold"] -= self.cost
            #             self.notice(0.5,"Bought",self.getItem("Axe"))
                
            #     case "Forest":
            #         if self.win.forests[self.win.forestlevel + 1] == "Max":
            #             self.notice(0.5,"Max Forest Reached","Max Forest")
            #         else:
            #             self.win.forestlevel += 1
            #             if self.win.forests[self.win.forestlevel + 1] == "Max":
            #                 self.notice(0.5,"Max Forest Reached","Max Forest")
            #             else:
            #                 self.notice(0.5,"Forest Upgraded",f"Upgrade Forest: {10 + 10*self.win.forestlevel}")
                    
            # if self.cooldown > 0:
            #     self.setText(str(self.cooldown))
            #     self.qtimer.start()
        

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    screen = Screen()
    sys.exit(app.exec_())