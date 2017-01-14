import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import res.resources_rc
import core_lib as cl


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

''' SensorStatusWidget:
    This class inherits the QWidget class
    the object displayes the widget for the sensor monitoring
    the monitor displayes four SensorWidget object that show the status of each sensor
    in addition this class provides methods to control the and consult the status of each SensorWidget
'''
class SensorStatusWidget(QWidget):

    """
        __init__ method override
    """
    def __init__(self):
        super(SensorStatusWidget, self).__init__()
        self.init()

    ''' init:
        This function initialize all the object
        creates the basic variables
        set the layout and the widget style
    '''
    def init(self):
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

        #sensor widget variables
        self.laser = SensorWidget("Laser: ")
        self.imu = SensorWidget("IMU: ")
        self.nao = SensorWidget("Nao: ")
        self.ecg = SensorWidget("Ecg: ")

        #layout object
        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.laser)
        self.vbox.addWidget(self.imu)
        self.vbox.addWidget(self.ecg)
        self.vbox.addWidget(self.nao)

        self.setGeometry(0, 0, 200, 200)
        self.setLayout(self.vbox)

    ''' get_sensor_status:
        returns the status of an specific sensor s
        In parameters = String s (sensor)
        Out parameters = Intege 0,1,2 (status)
    '''
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

    ''' set_sensor_state:
        set the status of an specific sensor widget
        In parameters = String s (sensor), Integer 0,1,2 (status)
        Out parameters = Integer -1 if there is an exception
    '''
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
        if  not l == "-":
            self.value = l
            self.value_label.setText(str(self.value))
        else:
            print("leaving parameter unchanged")

    def get_value(self):
        return self.value_label.text()

'''ParameterMonitor
    this class inherits the object QWidget
    The widget displayes all the parameters of the therapy
    provides methods to set the values either individualy (set_parameter_value)
    or as a hole list (set_parameter_list)
'''
class ParameterMonitor(QWidget):
    '''
        __init__ method override
    '''
    def __init__(self):
        super(ParameterMonitor, self).__init__()
        self.init()

    ''' init:
        This function initialize all the object
        creates the basic variables
        set the layout and the widget style
    '''
    def init(self):
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

    '''set_parameter_value:
        set the value to an specific parameter
        In parameters: String value, Strin param
        Out parameters: Integer -1 if something wrong
    '''
    def set_parameter_value(self, value, param):
        if param == "cadence":
            self.cadence.set_value(value)
        elif param == "step_length":
            self.step_length.set_value(value)
        elif param  == "speed":
            self.speed.set_value(value)
        elif param == "inclination":
            self.inclination.set_value(value)
        elif param == "heart_beats":
            self.heart_beats.set_value(value)
        elif param == "borg_scale":
            self.borg_scale.set_value(value)
        else:
            return -1

    ''' set_parameter_list:
        set the values to all the parameters of the monitor
        In parameters: List[] l -- All parameter values
        Out parameters: return msg if something wrong with the format
    '''
    def set_parameter_list(self, l):
        print len(l)
        if len(l) == 6:
            self.cadence.set_value(l[0])
            self.step_length.set_value(l[1])
            self.speed.set_value(l[2])
            self.inclination.set_value(l[3])
            self.heart_beats.set_value(l[4])
            self.borg_scale.set_value(l[5])
        else:
            print("wrong data string ")
            return


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
        self.label.setText("Ip Address: ")
        self.ip.setText("127.0.0.1")
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.ip)
        self.setLayout(self.hbox)

    def __init__(self, b):
    	super(NetworkLabel, self).__init__()
    	print(b)
    	self.label = QLabel()
        self.ip = QLabel()
        self.hbox = QHBoxLayout()
        self.label.setText("Ip Address: ")
        self.ip.setText("127.0.0.1")

    	self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.ip)

    	if  b:
    		self.button = QCommandLinkButton()
        	self.hbox.addWidget(self.button)
        	#self.q = NetworkRequestWidget()
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

		self.localhost = NetworkLabel(False)

		self.nao_network = NetworkLabel(True)
		self.nao_network.label.setText("Nao Address: ")
		self.nao_network.ip.setText("----")
		self.nao_network.button.clicked.connect(self.showDialog)

		self.vbox = QVBoxLayout()
		self.vbox.addWidget(self.title)
		self.vbox.addWidget(self.localhost)
		self.vbox.addWidget(self.nao_network)
		self.vbox.addStretch(0)

		self.setLayout(self.vbox)

	def get_robot_ip(self):
		return self.nao_network.ip.text()


	def setCallback(self, func):
		self.func = func

	def Callback(self):
		self.func()


	def showDialog(self):
		ip, ok = QInputDialog.getText(self, 'Input Dialog','Enter the Nao IP:')
		if ok:
			print (ip)
			self.nao_network.ip.setText(ip)
			self.Callback()


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
