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

from converter import *
from conio import *
from chess import *

class ChatRoomClient :
	def __init__(self, ip = "127.0.0.1", port = 7000) :
		self.ip = ip
		self.port = port
		# self.cond = Condition()
		self.mod = False
		self.exe = True
		# self.peer = ""
		# self.hint = "Command is -->"
		self.chess = []
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.socket.connect((self.ip, self.port))
		self.run()
		
	def cmd(self) :
		command = []
		value = NonASCII
		
		while self.exe :
			if self.mod :
				# command = input(self.hint)
				# command = command.split(" ")
				if kbhit() :
					value = getKey()
					
				if value == Enter : # 輸入enter時產生指令
					value = NonASCII
					putch('\n') # 換行
					
					command  = ''.join(command)
					command = command.split(" ")
					
					if command[0] == "find" :
						self.peer = ""
						self.hint = "Command is -->"
						self.socket.sendall(str2b("type=find"))
						command = []
					
					elif command[0] == "next" :
						self.peer = ""
						self.hint = "Command is -->"
						self.socket.sendall(str2b("type=nextStep"))
						command = []
						
					elif command[0] == "quit" :
						self.peer = ""
						self.hint = ""
						self.socket.sendall(str2b("type=gameOver"))
						command = []
					
					elif command[0] == "logout" :
						self.peer = ""
						self.hint = "Command is -->"
						self.socket.sendall(str2b("type=logout"))
						command = []
						break
					
					else :
						if self.peer == "" :
							print("unknow ", command[0])
							command = []
						else :
							msg = ' '.join(command[0:len(command)])
							self.socket.sendall(str2b("type=talk&to=%s&message=%s" % (self.peer, msg)))
							command = []
				elif value == KEY_ARROW : # 為中繼無效字元 忽略
					value = NonASCII
				elif value == KEY_UP : 
					print('KEY_UP')
					value = NonASCII
				elif value == KEY_DOWN :
					print('KEY_DOWN')
					value = NonASCII
				elif value == KEY_RIGHT :
					print('KEY_RIGHT')
					value = NonASCII
				elif value == KEY_LEFT :
					print('KEY_LEFT')
					value = NonASCII
				elif value == BackSpace : # 按倒退鍵可刪除文字
					if len(command) > 0 :
						command.pop(len(command) - 1)
						putch('\b')
						putch(' ')
						putch('\b')
					value = NonASCII
				elif not value == NonASCII :# 如果非特殊字元，或無效字元則進行輸入
					command.append(value)
					putch(value)
					value = NonASCII
					
	def read(self) :
		while self.exe :
			data = self.socket.recv(4096)
			if len(data) > 0 :	
				D = str2D(b2str(data))
				
				print(D)
				
				if D["type"] == "nickname" : # 登錄驗證
					user = input('user :')
					msg = 'type=nickname&name=%s' % (user,)
					self.socket.sendall(str2b(msg))
				# -------------------------------------------------------------------- #
				elif D["type"] == "loginOK" : # 登錄成功
					print("get nickname, start game mode")
					self.mod = True
				# -------------------------------------------------------------------- #
				elif D["type"] == "peer" : # 確認對手
					self.socket.sendall(str2b("type=peer&user=" + D["user"]))
					print("Your peer is " + D["user"])
				# -------------------------------------------------------------------- #
				elif D['type'] == "noPeer" : # 警告沒有對手
					print('no peer QQ')
					pass
				# -------------------------------------------------------------------- #
				elif D['type'] == "initStep" : # 擁有初始棋盤
					print('initial Chess')
					self.chess = Chess()
					self.chess.drawChess(1, 5)
					self.chess.drawChessInfo(D["chessInfo"])
					if D["first"] == "1" :
						self.socket.sendall(str2b("type=first"))
				# -------------------------------------------------------------------- #
				elif D['type'] == "nextStep" : # 下一步
					# do some next step !
					self.socket.sendall(str2b("type=waitNext"))
					pass
				# -------------------------------------------------------------------- #
				elif D['type'] == "waitNextOK" : # 得到下一步許可
					print("next step ?")
				# -------------------------------------------------------------------- #
				elif D['type'] == "turnError" : # 回合錯誤警告
					print("it's not your turn")
				# -------------------------------------------------------------------- #
				elif D['type'] == "gameOver" : # 結束遊戲
					self.socket.sendall(str2b("type=gameOver"))
				# -------------------------------------------------------------------- #
				elif D["type"] == "logout" : # 中止遊戲
					print('logout')
					self.exe = False
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
	initscr()
	clsscr()
	c = ChatRoomClient()