import sys, ctypes, win32api, functools, csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QMenu, QAction, QDialog, QDialogButtonBox, QColorDialog, QMainWindow
from PyQt5.QtGui import QPalette, QColor
from gui import Ui_guiDialog
from datetime import datetime

ERROR_LOG = 'error.log'

def logError(msg):
    now = datetime.now()
    print("{} {}".format(now.strftime("%Y-%m-%d %H:%M:%S"), msg), \
          file=sys.stderr)

class GuiDialog(Ui_guiDialog):
    CSV_FILENAME = 'F2HabitBreaker.csv'
    CSV_DELIMITER = ','
    CSV_QUOTE = '|'
    DEFAULT_WIDTH = 51
    DEFAULT_HEIGHT = 31
    DEFAULT_X_OFFSET = 59
    DEFAULT_Y_OFFSET = 539
    DEFAULT_RED = 0
    DEFAULT_GREEN = 0
    DEFAULT_BLUE = 0
    DEFAULT_ALPHA = 1.0
    
    def __init__(self, app, overlayWindow, csvFilename=CSV_FILENAME):
        super().__init__()
        
        self.csvFilename = csvFilename
        self.monitorIndex = 0   # The monitor on which the overlay will be placed
        self.overlayWindow = overlayWindow
        self.dialog = QDialog()
        self.setupUi(self.dialog)
        self.dialog.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint
            | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.Dialog | QtCore.Qt.MSWindowsFixedSizeDialogHint
            | QtCore.Qt.WindowTitleHint);
        self.app = app
        self.isUpdating = False  # Prevents self.updateOverlay() from being called multiple times when modifying widget values

        self.dialog.finished.connect(app.quit)
        resetButton = self.bottomButtonBox.button(QDialogButtonBox.Reset)
        applyButton = self.bottomButtonBox.button(QDialogButtonBox.Apply)
        resetButton.clicked.connect(self.reset)
        applyButton.clicked.connect(self.apply)
        
        self.availableMonitors=[]
        monitors = win32api.EnumDisplayMonitors()
        
        if len(monitors) == 0:
            logError("No monitors detected.")
        
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
        self.positions = self.loadPositions()
        
        # If additional monitors were added since the last time the settings file was modified, or
        # if we're running for the first time, then add a new overlay position for each new monitor.
        
        for i in range(len(self.positions), len(self.availableMonitors)):
            self.positions.append({
                'resolution': self.availableMonitors[i]['resolution'],
                'x': GuiDialog.DEFAULT_WIDTH,
                'y': GuiDialog.DEFAULT_HEIGHT,
                'xOffset': GuiDialog.DEFAULT_X_OFFSET,
                'yOffset': GuiDialog.DEFAULT_Y_OFFSET,
                'r': GuiDialog.DEFAULT_RED,
                'g': GuiDialog.DEFAULT_GREEN,
                'b': GuiDialog.DEFAULT_BLUE,
                'a': GuiDialog.DEFAULT_ALPHA,
            })
        
        # Add the monitors to the combo box.
        
        self.monitorComboBox.clear()
        
        for (i, monitor) in zip(range(1, 1+len(self.availableMonitors)), self.availableMonitors):
          self.monitorComboBox.addItem("{}: {}".format(i, monitor['resolution']))
        
        self.updateFields()
        
        if len(self.availableMonitors) > self.monitorIndex:
            self.overlayWindow.placeWindow(self.positions[self.monitorIndex], self.availableMonitors[self.monitorIndex])
        
        self.overlayWidthSpinBox.valueChanged.connect(self.updateOverlay)
        self.overlayHeightSpinBox.valueChanged.connect(self.updateOverlay)
        self.overlayXSpinBox.valueChanged.connect(self.updateOverlay)
        self.overlayYSpinBox.valueChanged.connect(self.updateOverlay)
        self.overlayColorButton.clicked.connect(self.setColor)
        self.monitorComboBox.currentIndexChanged.connect(self.setMonitorIndex)
        
    def show(self):
        self.dialog.show()
    
    ''' Sets the widget values from the saved position/color values. '''
    
    def updateFields(self):
        if self.isUpdating:
           return
        
        self.isUpdating = True
        
        # Set the spin box values with the settings that were loaded from the settings file.
        
        if self.monitorIndex < len(self.positions):
          position = self.positions[self.monitorIndex]
          
          self.overlayXSpinBox.setValue(position['xOffset'])
          self.overlayYSpinBox.setValue(position['yOffset'])
          self.overlayWidthSpinBox.setValue(position['x'])
          self.overlayHeightSpinBox.setValue(position['y'])
          
          # Set the background for the overlay color preview.
          
          color = QColor.fromRgb(position['r'], position['g'], position['b'], position['a']*255)
          palette = QPalette()
          palette.setColor(QPalette.Background, color)
          self.overlayColorWidget.setPalette(palette)
          self.overlayColorWidget.show()
        self.isUpdating = False
    
    def setMonitorIndex(self, value):
        if self.isUpdating:
            return
        
        self.isUpdating = True
        
        if value >= 0 and value < len(self.availableMonitors):
            self.monitorIndex = value
        else:
            self.monitorIndex = 0
        
        self.isUpdating = False
        self.updateFields()
        self.updateOverlay()
    
    ''' Applies the position and color values to the overlay and saves the overlay positions. '''
    
    def apply(self):
        self.updateOverlay()
        self.savePositions()
    
    def updateOverlay(self):
        if not self.isUpdating:
            self.positions[self.monitorIndex]['xOffset'] = self.overlayXSpinBox.value()
            self.positions[self.monitorIndex]['yOffset'] = self.overlayYSpinBox.value()
            self.positions[self.monitorIndex]['x'] = self.overlayWidthSpinBox.value()
            self.positions[self.monitorIndex]['y'] = self.overlayHeightSpinBox.value()
            self.overlayWindow.placeWindow(self.positions[self.monitorIndex], self.availableMonitors[self.monitorIndex])
    
    ''' Prompts the user for a color and sets the overlay to that color. '''
    
    def setColor(self):
        color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
        palette = QPalette()
        palette.setColor(QPalette.Background, color)
        self.overlayColorWidget.setPalette(palette)
        self.overlayColorWidget.show()
        
        position = self.positions[self.monitorIndex]
        position['r'] = color.red()
        position['g'] = color.green()
        position['b'] = color.blue()
        position['a'] = color.alpha() / 255.0
        
        self.overlayWindow.placeWindow(position, self.availableMonitors[self.monitorIndex])
    
    ''' Undo all changes to the overlay position and color. Values are reset to the ones in the settings file. '''
    
    def reset(self):
        self.positions = self.loadPositions()
        self.monitorIndex = 0
        self.updateFields()
        self.updateOverlay()
    
    ''' Store position data into the settings file. '''
    
    def savePositions(self):
        try:
            with open(self.csvFilename, 'wt', newline='\n') as csvfile:
                writer = csv.writer(csvfile, delimiter=GuiDialog.CSV_DELIMITER, quotechar=GuiDialog.CSV_QUOTE)
                for position, monitor in zip(self.positions, self.availableMonitors):
                    writer.writerow([monitor['resolution'], position['x'], position['y'], position['xOffset'], \
                                      position['yOffset'], position['r'], position['g'], position['b'], position['a']])
        except OSError as e:
            logError("Unable to save to settings file ({}). Error {}: {}.".format(GuiDialog.CSV_FILENAME, e.errno, e.strerror))
    
    ''' Load position data from the settings file. '''
    
    def loadPositions(self):
        positions=[]
        try:
          with open(self.csvFilename, 'rt') as csvfile:
              reader = csv.reader(csvfile, delimiter=GuiDialog.CSV_DELIMITER, quotechar=GuiDialog.CSV_QUOTE)
              for row in reader:
                  try: # try to get position with rgba
                      positions.append({
                          'resolution': row[0],
                          'x': int(row[1]),
                          'y': int(row[2]),
                          'xOffset': int(row[3]),
                          'yOffset': int(row[4]),
                          'r': int(row[5]),
                          'g': int(row[6]),
                          'b': int(row[7]),
                          'a': float(row[8])
                      })
                  except:
                      try: # if we cant, try to get old style position only
                          positions.append({
                              'resolution': row[0],
                              'x': int(row[1]),
                              'y': int(row[2]),
                              'xOffset': int(row[3]),
                              'yOffset': int(row[4]),
                              'r': 0,
                              'g': 0,
                              'b': 0,
                              'a': 1
                          })
                      except:
                          logError("Error while reading line {} in {}.".format(reader.line_num, GuiDialog.CSV_FILENAME))
        except FileNotFoundError:
            logError("Settings file ({}) doesn't exist. Loading with default values...".format(GuiDialog.CSV_FILENAME))
        except OSError as e:
            logError("Unable to read settings file ({}). Error {}: {}.".format(GuiDialog.CSV_FILENAME, e.errno, e.strerror))
        return positions
    
    def quit(self):
        self.overlayWindow = None
        self.app.closeAllWindows()
    
class F2HabitBreaker(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.guiDialog = GuiDialog(app, self)
        self.guiDialog.show()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setCentralWidget(QWidget(self))
    ''' Sets the overlay's position and color on the screen. '''
    
    def placeWindow(self, position, monitor):
        # move/resize the window into place
        self.resize(position['x'],
                    position['y'])
        self.move(position['xOffset'] + monitor['xOffset'],
                    position['yOffset'] + monitor['yOffset'])
        self.setStyleSheet("QMainWindow { background-color: rgba("+str(position['r'])+", "+str(position['g'])+", "+str(position['b'])+", 1); }")
        self.setProperty("windowOpacity", position['a'] if position['a']>0 else 0.01 )

if __name__ == '__main__':
    try:
        sys.stderr = open(ERROR_LOG, 'at')
    except:
        pass
    
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = F2HabitBreaker(app)
    mainWindow.show()
    sys.exit(app.exec_())
