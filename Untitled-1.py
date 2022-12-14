from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,time
from threading import Thread

order = {"starters":{
            "Halloumi Sticks":{
                "cost":4.25,
                "amount":0},
            "Spicy Mixed Olives":{
                "cost":3.75,
                "amount":0},},
        "chicken":{},
        "burgers":{}}

class Screen(QMainWindow):
    def __init__(self):
        super(Screen,self).__init__()
        self.setGeometry(300,300,600,600)
        self.setWindowTitle("Nando")
        self.setStyleSheet("background: #161219;")
        self.mainscreen()
        self.show()
    
    def mainscreen(self):
        self.widgets = {
            "title" : Text(self,"Nando's Menu",(225,10),15),
            "starters": Button(self,"Starters",(200,60)),
            "burgers": Button(self,"Burgers",(200,140)),
            "order": Button(self,"View Order",(200,220))
        }
        for value in self.widgets.values():
            value.show()
        

    def starterscreen(self):
        self.widgets = {
            "back" : Button(self,"Back",(10,10),(100,70)),
            "title" : Text(self,"Nando's starters                          Amount",(225,10),15),
            
        }
        count = 0
        for item,value in order["starters"].items():
            self.widgets[item] = Button(self,f"{item}: £{value['cost']}",(200,60 + 80*count))
            self.widgets[f"{item} amount"] = Text(self, order["starters"][item]["amount"])
            count += 1


        for value in self.widgets.values():
            value.show()
    
    def chickenscreen(self):
        pass
    
    def burgerscreen(self):
        pass
    
    def orderscreen(self):
        pass
    
    def clearscreen(self):
        tempwidgets = dict(self.widgets)
        for key,value in self.widgets.items():
            value.hide()
            del tempwidgets[key]

class Text(QLabel):
    def __init__(self,window, text,pos,size):
        super().__init__(text,window)
        self.move(*pos)
        self.setAlignment(Qt.AlignVCenter)
        self.setStyleSheet(
            "*{"+
            f'''color: white;
            font-family: 'shanti';
            font-size: {size}px;
            padding: 15px 0;
            margin-top: 20px'''
            +"}")
        self.setFixedSize(size*len(text),size+23)    
             

class Button(QPushButton):
    def __init__(self,window, text,pos,size = (200,70)):
        super().__init__(text,window)
        self.win = window
        self.message = text
        self.move(*pos)
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
        self.clicked.connect(self.buttfunctions)

    def buttfunctions(self):
        if not self.cooldownstate:
            match self.message:
                case "Starters":
                    self.win.clearscreen()
                    self.win.starterscreen()
                case "Chickens":
                    self.win.clearscreen()
                    self.win.chickenscreen()
                case "Burgers":
                    self.win.clearscreen()
                    self.win.burgerscreen()
                case "View Order":
                    self.win.clearscreen()
                    self.win.orderscreen()
                case "Back":
                    self.win.clearscreen()
                    self.win.mainscreen()
                case _:
                    name = self.message.split(":")[0]
                    for course,item in order.items():
                        for dish in item.keys():
                            if name == dish:
                                order[course][dish]["amount"] += 1
                                break
                            


    def notice(self, sleeptime, message, orgmessage):
        def noticethread():
            self.cooldownstate = True
            self.setText(message)
            time.sleep(sleeptime)
            self.setText(orgmessage)
            self.cooldownstate = False
        Thread(target=noticethread, daemon = True).start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = Screen()
    sys.exit(app.exec_())