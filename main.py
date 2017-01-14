import src.cardio_wigets as cw
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import src.core_lib as cl
import threading

class CentralWindow(QWidget):
    def __init__(self):
        super(CentralWindow, self).__init__()
        self.init_grid()


    #grid layout
    def init_grid(self):
        self.grid = QGridLayout()

        self.parameter_monitor = cw.ParameterMonitor()
        self.sensor_status = cw.SensorStatusWidget()
        self.control_panel = cw.ControlPanelWidget()
        self.network_monitor = cw.NetworkMonitor()

        self.grid.addWidget(self.sensor_status,1,1)
        self.grid.addWidget(self.network_monitor,2,1)
        self.grid.addWidget(self.parameter_monitor,1,2,2,1)
        self.grid.addWidget(self.control_panel,3,1,1,2)

        self.setLayout(self.grid)

    def get_sensor_wg(self):
    	return self.sensor_status

    def get_network_wg(self):
    	return self.network_monitor

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_window()

    def init_window(self):
        self.central_window = CentralWindow()
        self.setCentralWidget(self.central_window)
        self.show()

class CardioApp:

	def __init__(self):
		#Launch the main window interface
		self.MainWindow = MainWindow()
		#run set up proccess



#test function
def check_sensor(main):

	dev_status = cl.check_devices()
	#
	sensor_wg = main.central_window.get_sensor_wg()
	network_wg = main.central_window.get_network_wg()
	#
	def nao():
		#network_wg = main.central_window.get_network_wg()
		nao_ip =  network_wg.get_robot_ip()
		nao_state = cl.nao_checker(str(nao_ip))
		print("state from callback: " + str(nao_state))
	network_wg.setCallback(nao)

	localhost_ip = cl.localhost_checker()
	#nao_ip =  network_wg.get_robot_ip()
	nao_state = 0
	#print ("esta es " + str(nao_ip))
	#nao_state = cl.nao_checker(str(nao_ip))
	#


	if nao_state == 0:
		network_wg.nao_network.ip.setText("Not connected")
	elif nao_state == 2:
		network_wg.nao_network.ip.setText(nao_ip)
	#
	if localhost_ip == -1:
		network_wg.localhost.ip.setText("Not connected")
	else:
		network_wg.localhost.ip.setText(localhost_ip)

	#check sensor avialability (state 0)
	sensor_wg.set_sensor_state("imu", dev_status[1])

	#provide permisions (state 1)
	sensor_wg.set_sensor_state("laser", dev_status[0])
	sensor_wg.set_sensor_state("ecg", 1)

	#sensor permisions granted (state 2)
	sensor_wg.set_sensor_state("nao", nao_state)

'''def nao():
	network_wg = main.central_window.get_network_wg()
	nao_ip =  network_wg.get_robot_ip()
	nao_state = cl.nao_checker(str(nao_ip))
'''
def main():
	#app to run the pyqt widgets
	app = QApplication(sys.argv)
	#creates the main window of the interface
	main = MainWindow()
	#start up process
	check_sensor(main)
	main.central_window.parameter_monitor.set_parameter_list(["1","2","-","2","3","-"])
	#a = cw.IpInputDialog()

	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
