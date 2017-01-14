import sys
import os 
import socket
#sensor state checker functions 
#each function returns the state of the syensor (0,1,2)
'''
This function check the connection beetween the pc and the Nao robot 
The functions performs a ping to test the connection
if a response is recieved then returns 2 (the connection is up)
otherwise returns 0 (connection down)

In parameters: String "NAO Ip" 
Out Parameters: Integer 0 or 2 depending of the state of the connection
'''

def nao_checker(nao_ip):
	#ping to nao
	if not (nao_ip == "----"):
		hostname = nao_ip
		response = os.system("ping -c 1 " + hostname)
		if response == 0:
			print(hostname + " is up")	
			return 2
		else:
			print("Nao unreachable, please verify that the robot is on and connected to the same network")  	
			return 0
	else:
		print("Wrong ip format")
		

'''
This functions checks the pc's internet connection connection and the ip Address
Creates a socket in order to stablish a simple connection with a normal server (google.com) 
After the connection ask for the IP address

In parameters: void
Out Parameters: String "Ip address" if successfull and Integer -1 if no internet conection
'''

def localhost_checker():

	hostname = "google.com"
	response = os.system("ping -c 1 " + hostname)
	if response == 0:
			
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('google.com', 0))
		ip = s.getsockname()[0]
		print("Pc is up and connected with ip address: " + ip)
		print(ip)
		return ip
	else:
		print("Not connected to the network")
		return -1

'''
This function checks on the system (ubuntu) the connected devices
particulary search the hokuyo and imu device

In Parameters: void
Out Parameters: tuple [Laser_state, imu_state]
'''	
def check_devices():
	#check dev folder for serial (usb) connected sensors
	devices = ["/dev/" + x for x in os.popen("ls /dev/ | egrep -i 'hokuyo|imu'").read().strip().split('\n')]
	print(devices)
	laser_state = 0
	imu_state = 0 
	for dev in devices:
		if dev == "/dev/hokuyo":
			laser_state = 2
		elif dev == "/dev/imu":
			imu_state = 2
	return [laser_state, imu_state]
	

