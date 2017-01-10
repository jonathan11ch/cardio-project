import threading
import socket
import pickle
import time

class nao_data_listener():
	def __init__(self, function = None):
		print("creating Nao data listener")
		#socket variables
		self.TCP_PORT = 13000
		self.TCP_IP = "192.168.1.10"
		
		#storage variables
		self.BUFFER_SIZE = 1024 #reception buffer
		self.data  = [] # raw data 
		self.sensor_data = [] # data deserialized
		self.payload = ""
		#callback functions on data recieved
		if function:
			self.f = function  
		else: 
			self.f = self.echo
		#frecuency variables
		self.TIME = 5
		#boolean
		self.THREAD_ON = True
		self.PRINT = False
		self.SERIALIZED = True	
		self.SPIN_ONCE = False
		
	def set_payload(self, p):
		self.payload = p		
			
	def echo(self):
		print(self.data)		
			
	def set_callback(self, f):
		self.f = f
	
	def set_communication(self):
		print("setting communication with data server...")
		while self.THREAD_ON:
			try:
				#start socket connection
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((self.TCP_IP, self.TCP_PORT))
				print("connected..")
				if not(self.payload == ""):
					s.send(self.payload)
				
				print("waiting.....")
				self.data = s.recv(self.BUFFER_SIZE)
				s.close()
				#end of socket 
				print("serialize")
				#deserialization of data 
				if self.SERIALIZED:
					self.sensor_data = pickle.loads(self.data)
				print("running callback")
				self.f()	
				
				if self.PRINT:	
					print("*************************************************************************************************************")
					print("....data recieved....")
					print("------------------------------------------------------------------------")
					print("....RAW DATA....")
					print(self.data)
					print("------------------------------------------------------------------------")
					print("....DESERIALIZED DATA....")
					print(self.sensor_data)
					print("------------------------------------------------------------------------")
				
			except Exception:
				print("Error while connecting to the data server ")
				print (Exception)
				
			if self.SPIN_ONCE:
				break
						
			time.sleep(self.TIME)
					
	def start_thread(self):
		listener_thread = threading.Thread(target = self.set_communication)
		listener_thread.start()		
	
	def get_sensor_data(self):	
		return self.sensor_data
				
	def shut_down(self):
		self.THREAD_ON = False	

class sensor_broadcaster():
	
	def __init__(self, function = None):
		# socket variables
		self.TCP_IP = 'localhost'
		self.TCP_PORT = 8000
		
		# storage variables
		self.BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
		self.data_to_send = []
		
		#callback functions on data recieved
		if function:
			self.f = function  
		else: 
			self.f = self.echo
		
		# boolean
		self.SERVER_THREAD = True
		self.RECEPTION = False
		
	def set_callback(self, f):
		self.f = f			
				
	def server_process(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.TCP_IP, self.TCP_PORT))
		s.listen(1)
		print("sensor boradcaster server running...")
		while self.SERVER_THREAD:
			print("waiting on connection....")
			conn, addr = s.accept()
			print ('Connection address:', addr)
			self.f()
			if self.RECEPTION:
				recieved  = conn.recv(self.BUFFER_SIZE)
				r = pickle.loads(recieved)
			#with open('entry.pickle', 'wb') as f:
			data = pickle.dumps(self.data_to_send, protocol = 2)
			print(data)
			conn.send(data)  
			conn.close()
			
		s.close()	
		
	def echo(self):
		print("incomming request")	
			
	def start_thread(self):
		server_thread = threading.Thread(target = self.server_process)
		server_thread.start()				
	
	def load_data(self, data):
		self.data_to_send = data
				
	def shut_down(self):
		self.SERVER_THREAD = False	
		
 
		
def nao_server_init():

	TCP_IP = 'localhost'
	TCP_PORT = 8000
	BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	print("nao server running...")
	global SERVER_TRHEAD
	while SERVER_TRHEAD:
		print("waiting on connection....")
		conn, addr = s.accept()
		print ('Connection address:', addr)
		#data = conn.recv(BUFFER_SIZE)
		#if not data: break
		global Nao_data
		data = Nao_data
		#print ("sending data")
		#print (data)
		#with open('entry.pickle', 'wb') as f:
		data_to_send = pickle.dumps(data, protocol = 2)
		print(data_to_send)
		conn.send(data_to_send)  
		conn.close()
	s.close()
		
if __name__ == "__main__":
	
	Nao_data = ["data1","data1"]
	#SERVER_TRHEAD = True
	s = sensor_broadcaster()
	s.load_data(Nao_data)
	s.start_thread()
	#listener = nao_data_listener()
	#listener.start_thread()
	con = 0
	#socket_thread = threading.Thread(target = nao_server_init)
	#socket_thread.start()
	try:
		while True:
			con = con +1
			if (con == 10):
				s.load_data(["cgani","imu","laser",3443])
			time.sleep(1)
	except KeyboardInterrupt:
		#SERVER_TRHEAD = False
		s.shut_down()
		
	
