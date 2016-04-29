import sys, ctypes, win32api, functools, csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QMenu, QAction

class F2HabitBreaker(QMainWindow):
    def __init__(self):
            super().__init__() 

            self.availableMonitors=[]
            monitors = win32api.EnumDisplayMonitors()
            for monitor in monitors:    
                # monitor[2] => (0, 0, 1920, 1080)    [ x start, y start, x end, y end ]    
                
                # get the resolution so we can find the correct position
                X = monitor[2][2] - monitor[2][0]
                Y = monitor[2][3] - monitor[2][1]
                resolution=str(X)+"x"+str(Y)
                
                # offsets to add to button position to put it on the right monitor
                xOffset=monitor[2][0]
                yOffset=monitor[2][1]
                
                self.availableMonitors.append({'resolution': resolution, 'xOffset': xOffset, 'yOffset': yOffset})
                

            self.placeWindow(0)
            
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
            self.show()
            
            
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        for monitor in self.availableMonitors:
            menu.addAction(QAction(str(self.availableMonitors.index(monitor))+": "+monitor['resolution'], self, triggered=functools.partial(self.placeWindow, self.availableMonitors.index(monitor))))
                
        menu.addSection('')
        menu.addAction(QAction("Quit", self, triggered=self.quit))
        menu.exec_(event.globalPos())
    
    
    def getPositions(self): 
        positions=[]
        with open('F2HabitBreaker.csv', 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                positions.append({ 'resolution': row[0], 'x': int(row[1]), 'y': int(row[2]), 'xOffset': int(row[3]), 'yOffset': int(row[4]) })
        return positions
        
    def placeWindow(self, monitorId):
        # find the right position for this resolution
        position=None
        for f2Position in self.getPositions():
            if f2Position['resolution']==self.availableMonitors[monitorId]['resolution']:
                position=f2Position
        
        # if we havent found it then we need to quit                  (uh quitting probably isnt actually the best option?)
        if position==None:
            print('Unsupported resolution: ')
            
            QMessageBox.information(self, 'Message',
                "Unsupported Resolution: "+self.availableMonitors[monitorId]['resolution'], QMessageBox.Ok)
            self.quit()
        # or if we have found it, we can move/resize the window into place
        else:
            self.resize(position['x'],
                        position['y'])
            self.move(position['xOffset'] + self.availableMonitors[monitorId]['xOffset'],
                        position['yOffset'] + self.availableMonitors[monitorId]['yOffset'])


    def quit(self):
        sys.exit()     

        
if __name__ == '__main__':   
    app = QtWidgets.QApplication([])
    F2=F2HabitBreaker()
    app.exec_()
