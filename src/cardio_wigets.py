import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import res.resources_rc


# widget classes for sensor status
class LedWidget(QLabel):

    def __init__(self):
        super(LedWidget, self).__init__()
        self.initUI()
        self.value = 0

    def initUI(self):
        print("loading image")
        self.pixmap = QPixmap()
        self.set_pixmap(0)

        self.show()
    
    def get_status(self):
        return self.value        

    def set_pixmap(self, value):

        if value == 0:
            self.value = value
            self.pixmap.load(':img/red_bulb.png')
        elif value == 1:
            self.value = value
            self.pixmap.load(':img/orange_bulb.png')
        elif value == 2:
            self.value = value 
            self.pixmap.load(':img/green_bulb.png')

        self.pixmap = self.pixmap.scaled(20,20, Qt.KeepAspectRatio)
        
        if self.pixmap.isNull():
            print("Null image...")
        else:
            print("Image loaded... ")

        self.setPixmap(self.pixmap)
        self.resize(self.pixmap.size())

class SensorWidget(QWidget):

    def __init__(self, t):
    	super(SensorWidget, self).__init__()
    	self.t = t
        self.hbox = QHBoxLayout()
    	self.initWidget(self.t)


    def initWidget(self , t):

        self.label = QLabel()
        self.label.setText(t)
        self.label.show()

        self.led = LedWidget()
    	#self.hbox.addStretch(0)
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.led)
        
        self.setLayout(self.hbox) 

class SensorStatusWidget(QWidget):
    def __init__(self):
        super(SensorStatusWidget, self).__init__()
        self.title = QLabel()
        #--------setup---------
        self.title.setText("SENSOR STATUS")
        self.title.setAlignment(Qt.AlignCenter)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Foreground,Qt.red)
        self.title.setPalette(self.palette)
        self.Lfont = QFont()
        self.Lfont.setBold(True)
        self.title.setFont(self.Lfont)


        self.laser = SensorWidget("Laser: ")
        self.imu = SensorWidget("IMU: ")
        self.nao = SensorWidget("Nao: ")
        self.ecg = SensorWidget("Ecg: ")

        #self.laser.setAlignment(Qt.AlignCenter)

        self.vbox = QVBoxLayout()
        
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.laser)
        self.vbox.addWidget(self.imu)
        self.vbox.addWidget(self.ecg)
        self.vbox.addWidget(self.nao)
        #self.vbox.addStretch(0)

        self.setGeometry(0, 0, 200, 200)
        self.setLayout(self.vbox)

    def get_sensor_status(self, s):
        
        if s == "laser":
            return self.laser.led.get_status()

        elif s == "imu":
            return self.imu.led.get_status()

        elif s == "nao":
            return self.nao.led.get_status()

        elif s == "ecg":
            return self.ecg.led.get_status()

        else:
            return -1 

    def set_sensor_state(self, sensor, state):

        if sensor == "laser":
            return self.laser.led.set_pixmap(state)

        elif sensor == "imu":
            return self.imu.led.set_pixmap(state)

        elif sensor == "nao":
            return self.nao.led.set_pixmap(state)

        elif sensor == "ecg":
            return self.ecg.led.set_pixmap(state)

        else:
            return -1    
         
# widget classes for therapy parameters 
class ParameterWidget(QWidget):

    def __init__(self, t,u):
        super(ParameterWidget, self).__init__()
        #name label
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setFixedWidth(100)
        #style setup
        self.palette = QPalette()
        self.palette.setColor(QPalette.Foreground,Qt.blue)
        self.label.setPalette(self.palette)
        self.Lfont = QFont()
        self.Lfont.setBold(True)
        self.label.setFont(self.Lfont)
        self.label.setText(t)
        self.label.show()
        #value label
        self.value = "#"
        self.value_label = QLabel()
        self.value_label.setText(self.value)
        self.value_label.setFixedWidth(50)
        self.value_label.show()
        #unit label 
        self.unit = QLabel()
        self.unit.setText(u)
        self.unit.setFont(self.Lfont)
        self.unit.setFixedWidth(50)
        self.unit.show()

        #set layout
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.label)
        #self.hbox.addStretch(0)
        self.hbox.addWidget(self.value_label)
        #self.hbox.addStretch(0)
        self.hbox.addWidget(self.unit)

        self.setLayout(self.hbox) 
        self.show()

    def set_value(self, l):
        self.value = l
        self.value_label.setText(str(self.value))

class ParameterMonitor(QWidget):
    def __init__(self):
        super(ParameterMonitor, self).__init__()
        #set title
        self.title = QLabel()
        self.title.setText("THERAPY PARAMETERS")
        self.title.setAlignment(Qt.AlignCenter)
        #style setup
        self.palette = QPalette()
        self.palette.setColor(QPalette.Foreground,Qt.red)
        self.title.setPalette(self.palette)
        self.Lfont = QFont()
        self.Lfont.setBold(True)
        self.title.setFont(self.Lfont)
        #parameter widget declaration
        self.cadence = ParameterWidget("Cadence: ", "Steps/s")
        self.step_length = ParameterWidget("Step length: ", "m")
        self.speed = ParameterWidget("Speed: ", "km/h")
        self.inclination = ParameterWidget("Inclination: ", "degrees")
        self.heart_beats = ParameterWidget("Heart Beats: ", "bpm")
        self.borg_scale = ParameterWidget("Borg Scale: ", "range")
        #set values
        #self.cadence.set_value(1)
        #set layout 
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.cadence)
        self.vbox.addWidget(self.step_length)
        self.vbox.addWidget(self.speed)
        self.vbox.addWidget(self.inclination)
        self.vbox.addWidget(self.heart_beats)
        self.vbox.addWidget(self.borg_scale)
        self.vbox.addStretch(0)
        self.vbox.setSpacing(0)
        

        self.hbox = QVBoxLayout()
        self.hbox.addWidget(self.title)
        self.hbox.addLayout(self.vbox)
        self.setLayout(self.hbox)
        self.setGeometry(0, 0, 400, 100)
        self.show()

# widget  classes for Control panel
class ControlPanelWidget(QWidget):
    def __init__(self):
        super(ControlPanelWidget, self).__init__()
        self.title = QLabel()
        #------setup------
        self.title.setText("CONTROL PANEL")
        self.title.setAlignment(Qt.AlignCenter)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Foreground,Qt.red)
        self.title.setPalette(self.palette)
        self.Lfont = QFont()
        self.Lfont.setBold(True)
        self.title.setFont(self.Lfont)
        #------variable declaration------
        self.run_button = QPushButton("Run Therapy")
        self.stop_button = QPushButton("Stop Therapy")
        self.borg_button = QPushButton("Borg Scale")
        self.save_button = QPushButton("Save data")
        
        #horizontal box layout
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.run_button)
        self.hbox.addWidget(self.stop_button)
        self.hbox.addWidget(self.save_button)
        self.hbox.addWidget(self.borg_button)
        #vertical box layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.title)
        self.vbox.addLayout(self.hbox)
        self.vbox.addStretch(0)

        self.setLayout(self.vbox)
        self.show()

#Network status classes
class NetworkLabel(QWidget):
    def __init__(self):
        super(NetworkLabel, self).__init__()
        self.label = QLabel()
        self.ip = QLabel()
        self.hbox = QHBoxLayout()
        self.label.setText("Ip Adrress: ")
        self.ip.setText("127.0.0.1")
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.ip)
        self.setLayout(self.hbox)

class NetworkMonitor(QWidget):
    def __init__(self):
        super(NetworkMonitor, self).__init__()
        #self title
        self.title = QLabel()
        self.title.setText("NETWORK MONITOR")
        self.title.setAlignment(Qt.AlignCenter)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Foreground,Qt.red)
        self.title.setPalette(self.palette)
        self.Lfont = QFont()
        self.Lfont.setBold(True)
        self.title.setFont(self.Lfont)

        self.localhost = NetworkLabel()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.localhost)
        self.vbox.addStretch(0)
        self.setLayout(self.vbox)

#Main window class
class CentralWindow(QWidget):
    def __init__(self):
        super(CentralWindow, self).__init__()
        self.init_grid()
        
    #grid layout
    def init_grid(self):
        self.grid = QGridLayout()
        self.parameter_monitor = ParameterMonitor()
        self.sensor_status = SensorStatusWidget()
        self.control_panel = ControlPanelWidget()
        self.network_monitor = NetworkMonitor()

        self.grid.addWidget(self.sensor_status,1,1)
        self.grid.addWidget(self.network_monitor,2,1)
        self.grid.addWidget(self.parameter_monitor,1,2,2,1)
        self.grid.addWidget(self.control_panel,3,1,1,2)
        self.setLayout(self.grid)
    #box layout 
    def init_box(self):
        self.parameter_monitor = ParameterMonitor()
        self.sensor_status = SensorStatusWidget()
        self.control_panel = ControlPanelWidget()

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.sensor_status)
        self.hbox.addWidget(self.parameter_monitor)
        
        
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.control_panel)

        self.setLayout(self.vbox)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_window()

    def init_window(self):

        self.central_window = CentralWindow()
        self.setCentralWidget(self.central_window)
        self.show()

def main():
    app = QApplication(sys.argv)

    main = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
