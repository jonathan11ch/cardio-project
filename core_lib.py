import sys
import os 
import socket
#sensor state checker functions 
#each function returns the state of the syensor (0,1,2)
def nao_checker(nao_ip):
	#ping to nao
	hostname = nao_ip
	response = os.system("ping -c 1 " + hostname)
	if response == 0:
		print(hostname + " is up")	
		return 2
	else:
		print("Nao unreachable, please verify that the robot is on and connected to the same network")  	
		return 0

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
		
def check_devices():
	devices = ["/dev/" + x for x in os.popen("ls /dev/ | egrep -i 'ttyUSB|ttyS[01]$'").read().strip().split('\n')]
	print(devices)
	laser_state = 0
	imu_state = 0 
	for dev in devices:
		if dev == "/dev/ttyS1":
			laser_state = 2
		elif dev == "/dev/imu":
			imu_state = 2
	return [laser_state, imu_state]
	#localhost_checker()	
#def laser_checker():
	#check port on dev 
	#check permision 
	#return 
	

