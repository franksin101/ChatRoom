from socket import *
from threading import *
from _thread import *
from time import sleep
from random import randint 
from queue import *
import struct
import uuid
import sys

from ChatRoomPacket import *

Account = {
		"mary" : "mary",
		"bob" : "bob"
		"apple" : "apple"
		"123" : "123"
	}
		
class ChatRoomServer :
	def __init__(self, ip = "192.168.56.1", port = 5000) :
		self.ip = ip # do automatic detect
		self.port = port
		self.user = dict()
		self.Q = Queue(1000)
		self.cond = Condition()
		self.mainSocket = socket(AF_INET, SOCK_STREAM)
		self.mainSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		
	def monitor(self, maxConnection = 1000) :
		self.mainSocket.bind((self.ip, self.port))
		self.mainSocket.listen(maxConnection)
		while True :
			newSocket, connAddr = self.mainSocket.accept()
			Thread(target = self.active, args = (newSocket,)).start()
			
	def active(self, sock) :
		AuthStatus = bool(0)
		username = ""
		
		# authentic
		for i in range(3) :
			try :
				if AuthStatus :
					break
				
				msg = "type=authReq&account=?&password=?"
				sock.sendall(str2b(msg))
				data = sock.recv(4096)
				
				userInfo = b2D(data)
					
				if userInfo["type"] == "authRes" and userInfo["account"] in list(Account.keys()) and Account[userInfo["account"]] == userInfo["password"] :
					if userInfo["account"] in list(self.user.keys()) :
						break
					print(userInfo["account"], " authentic success !")
					AuthStatus = bool(1)
					username = userInfo["account"]
					print("password ", userInfo["password"])
					self.user[username] = [username, sock]
					self.Q.put((username, "type=authOK"))
					
					try :
						fd = open(username, "r+")
						text = fd.read()
						text = text.split('\n')
						fd.seek(0)
						fd.truncate()
						fd.close()
						
						for t in text :
							self.Q.put((username, t))
					except FileNotFoundError :
						pass
					
					
			except ConnectionResetError :
				sock.close()
				exit()
		
		# authentic check		
		if not AuthStatus  :
			print('authentic error')
			sock.sendall(str2b("type=logout"))
			sock.close()
			exit()
		
		while True :
			try :
				data = sock.recv(4096)
				if len(data) > 0 :
					D = b2D(data)
				
					if D["type"] == "talk" :
						if D["to"]   in  list(self.user.keys()) :
							# on-line
							self.Q.put((D["to"], "type=talk&from=%s&to=%s&message=%s" % (username, D["to"], D["message"])))
						elif D["to"] in list(Account.keys()) :
							# off-line
							fd = open(D["to"], "a")
							fd.write("\ntype=talk&from=%s&to=%s&message=%s\n" % (username, D["to"], D["message"]))
							fd.close()
							
					elif D["type"] == "send" :
						if D["to"]   in  list(self.user.keys()) :
							# on-line
							self.Q.put((D["to"], "type=send&from=%s&to=%s&message=%s" % (username, D["to"], D["message"])))
						elif D["to"] in list(Account.keys()) :
							# off-line
							fd = open(D["to"], "a")
							fd.write("\ntype=send&from=%s&to=%s&message=%s\n" % (username, D["to"], D["message"]))
							fd.close()
							
					elif D["type"] == "list" :
						userstr = ""
						users = []
						i = 0
						for u in list(self.user.keys()) :
							users.append("user%d=%s" % (i, u))
							i = i + 1
						userstr = '&'.join(users)
						userstr = "type=list&" + userstr
						self.Q.put((username, userstr))
						
					elif D["type"] == "broadcast" :
						for u in list(self.user.keys()) :
							self.Q.put((u, "type=broadcast&message=%s" % D["message"]))
							
					elif D["type"] == "logout" :
						sock.sendall(str2b("type=logout"))
						sock.close()
						del self.user[username]
						break
				
					# self.Q.put( (username, data) )
				
			except ConnectionResetError :
				sock.close()
				if not username == '' :
					del self.user[username]
				break
		exit()
		
	def check(self) :
		while True :
			if not self.Q.empty() :
				data = self.Q.get()
				try :
					self.user[data[0]][1].sendall(str2b(data[1]))
				except OSError :
					if data[0] in list(Account.keys()) :
						# off-line
						fd = open(data[0], "a")
						fd.write("\n" + data[1] + "\n")
						fd.close()
					pass
				except KeyError :
					if data[0] in list(Account.keys()) :
						# off-line
						fd = open(data[0], "a")
						fd.write("\n" + data[1] + "\n")
						fd.close()
					pass
		
	def join(self) :
		while True :
			for t in enumerate() :
				if not t.is_alive() :
					try :
						threadName = t.getName()
						t.join(10)
						print('cancel {} thread', threadName)
					except RuntimeError :
						pass
					break

	def run(self) :
		mThread = Thread(target = self.monitor)
		cThread = Thread(target = self.check)
		jThread = Thread(target = self.join)
		
		mThread.start()
		cThread.start()
		jThread.start()
		
		print("Server Start OK")
		
		mThread.join()
		cThread.join()
		jThread.join()
		
			
		
if __name__ == "__main__" :
	server = ChatRoomServer()
	server.run()