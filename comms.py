#OPAL-RT Technologies Inc.
#This script is provided 'as is', without warranty of any kind.

#Purpose: Communication file responsible for UDP communications with the simulator
#The raspberry pi acts as a server, and the simulator is a client.

import socket
import array
#import pickle

class Ethernet:

	BUF_SIZE = 1024
	HOST_IP = '132.206.62.246'
	PORT = 45000
	def __init__(self):
        
		# Set up socket and bind socket to port and local host IP
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s.bind((self.HOST_IP, self.PORT))
		print('Waiting for connection from simulator...')
		data, self.address = self.s.recvfrom(self.BUF_SIZE)
		print ('Connected')
		self.message_header = data[0:6]
		
		self.s.close()
		
	def status(self):
	# Set up socket and bind socket to port and local host IP

		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.s.bind((self.HOST_IP, self.PORT))
		
		data, address = self.s.recvfrom(self.BUF_SIZE)
		# Rearrange data from bytes into an array, d for double
		data_doubles = array.array('d', data)

		self.s.close()
		return data_doubles[1:]
	

	def send(self,commands):
        # Set up socket and bind socket to port and local host IP
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.s.bind((self.HOST_IP, self.PORT))
        
        # Rearrange data from array and include message identification
#		n = len(commands)
#		message_length = bytes(array.array('h', [n*8])) 
#
#		message = self.message_header + message_length+ bytes(array.array('d',commands))
#
#		
#		self.s.sendto(message, self.address)
#		
#        # Close socket to prevent accumulation of data
#		self.s.close()
        
        
        
          message=array.array('d', [self.message_header])
        message=array.array('d',[self.message_header])
#        message_length = array.array('d', [commands]) # h represent unsinged short
#        message=array.array('d',[])
#        for i in range(1):
        message.append(commands[0])
        message.append(commands[1])
        message.append(commands[2])
        message.append(commands[3])
        message.append(commands[4])
        message.append(commands[5])
        message.append(commands[6])
#        message.append(commands[7]) 
        # message.append( message_length)
        
        # Send data
        self.s.sendto(bytes(message), self.address)
        
        # Close socket to prevent accumulation of data
        self.s.close()


