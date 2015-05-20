from socket import *
from threading import *
from _thread import *
from time import sleep
from random import randint 
from queue import *
import signal
import struct
import uuid
import sys
import getpass

from ChatRoomPacket import *

class ChatRoomClient :
	def __init__(self, ip = "192.168.56.1", port = 5000) :
		self.ip = ip
		self.port = port
		self.cond = Condition()
		self.mod = bool(0)
		self.exe = bool(1)
		self.peer = ""
		self.hint = "Command is -->"
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.socket.connect((self.ip, self.port))
		self.run()
		
	def cmd(self) :
		while self.exe :
			if self.mod == bool(1) :
				command = input(self.hint)
				command = command.split(" ")
				
				if command[0] == "listuser" :
					self.peer = ""
					self.hint = "Command is -->"
					self.socket.sendall(str2b("type=list"))
					
				elif command[0] == "send" :
					self.peer = ""
					self.hint = "Command is -->"
					if len(command) >= 3 :
						msg = ' '.join(command[2:len(command)])
						self.socket.sendall(str2b("type=send&to=%s&message=%s" % (command[1], msg)))
					else :
						pass
						
				elif command[0] == "talk" :
					self.peer = ""
					self.hint = "Command is -->"
					if len(command) >= 3 :
						self.peer = command[1]
						self.hint = "talk with %s : " % self.peer
						msg = ' '.join(command[2:len(command)])
						self.socket.sendall(str2b("type=talk&to=%s&message=%s" % (command[1], msg)))
					elif len(command) == 2 :
						self.peer = command[1]
						self.hint = "talk with %s : " % self.peer
					else :
						pass
				
				elif command[0] == "__exit" :
					self.peer = ""
					self.hint = "Command is -->"
						
				elif command[0] == "broadcast" :
					self.peer = ""
					self.hint = "Command is -->"
					if len(command) >= 2 :
						msg = ' '.join(command[1:len(command)])
						self.socket.sendall(str2b("type=broadcast&message=%s" % msg))
					else :
						pass
						
				elif command[0] == "logout" :
					self.peer = ""
					self.hint = "Command is -->"
					self.socket.sendall(str2b("type=logout"))
					break
					
				else :
					if self.peer == "" :
						print("unknow ", command[0])
					else :
						msg = ' '.join(command[0:len(command)])
						self.socket.sendall(str2b("type=talk&to=%s&message=%s" % (self.peer, msg)))
					
	def read(self) :
		while self.exe :
			data = self.socket.recv(4096)
			if len(data) > 0 :	
				D = str2D(b2str(data))
				
				if D["type"] == "authReq" :
					user = input('user :')
					passwd = getpass.getpass()
					msg = 'type=authRes&account=%s&password=%s' % (user, passwd)
					self.socket.sendall(struct.pack(str2F(msg), *str2B(msg)))
					
				elif D["type"] == "authOK" :
				
					print("authOK")
					self.mod = bool(1)
					
				elif D["type"] == "list" :
					for u in list(D.keys()) :
						if not u == "type" :
							print(u, " => ", D[u])
					print(self.hint)
							
				elif D["type"] == "talk" :
					print("from %s say : %s" % (D["from"], D["message"]))
					print(self.hint)
					
				elif D["type"] == "send" :
					print("from %s say : %s" % (D["from"], D["message"]))
					print(self.hint)
				
				elif D["type"] == "broadcast" :
					print("broadcast message : %s" % D["message"])
					print(self.hint)
					
				elif D["type"] == "logout" :
					print('logout')
					self.exe = bool(0)
					break
					
	def run(self) :
		
		rThread = Thread(target = self.read)
		cThread = Thread(target = self.cmd)
		
		rThread.start()
		cThread.start()
		
		print("Client Start OK")
		
		cThread.join()
		rThread.join()
			
				
				


if __name__ == "__main__" :
	c = ChatRoomClient()
