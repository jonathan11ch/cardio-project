import src.cardio_wigets as cw
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
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

    def get_sensor_status(self):
    	return self.sensor_status
        		

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_window()

    def init_window(self):
        self.central_window = CentralWindow()
        self.setCentralWidget(self.central_window)
        self.show()

#thread function for sensor state monitoring 
def check_sensor(sensor_wg):
	
	#check sensor avialability (state 0)
	sensor_wg.set_sensor_state("imu", 2)

	#provide permisions (state 1)
	sensor_wg.set_sensor_state("laser", 1)
	sensor_wg.set_sensor_state("ecg", 1)

	#sensor permisions granted (state 2)
	sensor_wg.set_sensor_state("nao", 0)



def main():
	app = QApplication(sys.argv)

	main = MainWindow()
 	sensorStatus = main.central_window.get_sensor_status()
	processThread = threading.Thread(target=check_sensor, args=(sensorStatus,))
	processThread.start()
	#launch all threads 
	check_sensor(sensorStatus)
	

	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
    