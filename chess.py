from conio import *
import random
from colorama import Fore, Back, Style

__chess__x__ = 1
__chess__y__ = 1

CHESSMAN = { # id symbol level
	0  : (u'  ', 0, None),
	1  : (u'將', 7, True),
	2  : (u'士', 6, True),
	3  : (u'士', 6, True),
	4  : (u'象', 5, True),
	5  : (u'象', 5, True),
	6  : (u'車', 4, True),
	7  : (u'車', 4, True),
	8  : (u'馬', 3, True),
	9  : (u'馬', 3, True),
	10 : (u'包', 2, True),
	11 : (u'包', 2, True),
	12 : (u'卒', 1, True),
	13 : (u'卒', 1, True),
	14 : (u'卒', 1, True),
	15 : (u'卒', 1, True),
	16 : (u'卒', 1, True),
	17 : (u'帥', 7, False),
	18 : (u'仕', 6, False),
	19 : (u'仕', 6, False),
	20 : (u'相', 5, False),
	21 : (u'相', 5, False),
	22 : (u'轟', 4, False),
	23 : (u'轟', 4, False),
	24 : (u'傌', 3, False),
	25 : (u'傌', 3, False),
	26 : (u'炮', 2, False),
	27 : (u'炮', 2, False),
	28 : (u'兵', 1, False),
	29 : (u'兵', 1, False),
	30 : (u'兵', 1, False),
	31 : (u'兵', 1, False),
	32 : (u'兵', 1, False),
}

# chess status  : chess pos | id | open or not

def chess(x = 1, y = 1) :
	global __chess__x__
	global __chess__y__
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	__chess__x__ = x
	__chess__y__ = y
	y_wall = (0, 2, 4, 6, 8)
	x_wall = (0, 3, 6, 9, 12, 15, 18, 21, 24)
	blank = (1, 4, 7, 10, 13, 16, 19, 22)
	for j in range(9) :
		if j in y_wall :
			inactive(__chess__x__, j + __chess__y__, ' '*25)
			continue
		for i in range(25) :
			if i in blank :
				active(i + __chess__x__ , j + __chess__y__, u'將')
			elif i in x_wall :
				inactive(i + __chess__x__, j + __chess__y__, ' ')
				
def chessSet(x = 1, y = 1, chessman = u'士') :
	global __chess__x__
	global __chess__y__
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	y_pos = (1, 3, 5, 7)
	x_pos = (1, 4, 7, 10, 13, 16, 19, 22)
	active(x_pos[x - 1] + __chess__x__ , y_pos[y - 1] + __chess__y__, chessman)
	
def chessPos(pos) :
	if str(type(pos)) == "<class 'tuple'>" :
		return (pos[1] -  1)*8 + pos[0]
	elif str(type(pos)) == "<class 'int'>" :
		__x__ = pos % 8
		__y__ = int(pos / 8) + 1
		if __x__ == 0 :
			__x__ = 8
			__y__ = __y__ - 1
		return (__x__, __y__)
	elif str(type(pos)) == "<type 'int'>" :
		__x__ = pos % 8
		__y__ = int(pos / 8) + 1
		if __x__ == 0 :
			__x__ = 8
			__y__ = __y__ - 1			
		return (__x__, __y__)
		
def chessTable() :
	__chess__table__ = dict()
	for i in range(1, 33) :
		__chess__table__[i] = [i, False]
	return __chess__table__
	
def initChess() :
	rArray = [i for i in range(1, 33)]
	random.shuffle(rArray)
	initStr = '|'.join([str(e) for e in rArray])
	return initStr
	
class Chess :
	__chess__x__ = 1
	__chess__y__ = 1
	SELECT = 1
	SELECTED = 2
	UNSELECT = 3
	def __init__(self) :
		self.table = dict()
		self.pos = [1, 1]
		self.sel = [-1, -1]
	def chessColor(self, flag) :
		if flag == self.SELECT :
			setBGColor(Back.RED, Style.BRIGHT)
			setFGColor(Fore.WHITE, Style.DIM)
		elif flag == self.SELECTED :
			setBGColor(Back.GREEN, Style.BRIGHT)
			setFGColor(Fore.WHITE, Style.DIM)
		elif flag == self.UNSELECT :
			setBGColor(Back.YELLOW, Style.BRIGHT)
			setFGColor(Fore.WHITE, Style.BRIGHT)
	def chess(self, x = 1, y = 1) :
		if x <= 0 :
			x = 1
		if y <= 0 :
			y = 1
		self.__chess__x__ = x
		self.__chess__y__ = y
		y_wall = (0, 2, 4, 6, 8)
		x_wall = (0, 3, 6, 9, 12, 15, 18, 21, 24)
		blank = (1, 4, 7, 10, 13, 16, 19, 22)
		for j in range(9) :
			if j in y_wall :
				inactive(self.__chess__x__, j + self.__chess__y__, ' '*25)
				continue
			for i in range(25) :
				if i in blank :
					#active(i + self.__chess__x__ , j + self.__chess__y__, u'  ')
					self.chessColor(self.UNSELECT)
					drawText(i + self.__chess__x__, j + self.__chess__y__, u'  ')
					defaultColor()
				elif i in x_wall :
					inactive(i + self.__chess__x__, j + self.__chess__y__, ' ')
	def chessman(self, x = 1, y = 1, symbol = u' ', style = UNSELECT) :
		if x <= 0 :
			x = 1
		if y <= 0 :
			y = 1
		y_pos = (1, 3, 5, 7)
		x_pos = (1, 4, 7, 10, 13, 16, 19, 22)
		#active(x_pos[x - 1] + self.__chess__x__ , y_pos[y - 1] + self.__chess__y__, symbol)
		self.chessColor(style)
		drawText(x_pos[x - 1] + self.__chess__x__, y_pos[y - 1] + self.__chess__y__, symbol)
		defaultColor()
	def chessPos(self, pos) :
		if str(type(pos)) == "<class 'tuple'>" :
			return (pos[1] -  1)*8 + pos[0]
		elif str(type(pos)) == "<type 'tuple'>" :
			return (pos[1] -  1)*8 + pos[0]
		elif str(type(pos)) == "<class 'list'>" :
			return (pos[1] -  1)*8 + pos[0]
		elif str(type(pos)) == "<type 'list'>" :
			return (pos[1] -  1)*8 + pos[0]
		elif str(type(pos)) == "<class 'int'>" :
			__x__ = pos % 8
			__y__ = int(pos / 8) + 1
			if __x__ == 0 :
				__x__ = 8
				__y__ = __y__ - 1
			return (__x__, __y__)
		elif str(type(pos)) == "<type 'int'>" :
			__x__ = pos % 8
			__y__ = int(pos / 8) + 1
			if __x__ == 0 :
				__x__ = 8
				__y__ = __y__ - 1			
			return (__x__, __y__)
	def initChess(self) :
		self.table = dict()
		for i in range(1, 33) :
			self.table[i] = [i, True]
		rArray = [i for i in range(1, 33)]
		cnt = 1
		random.shuffle(rArray)
		for e in rArray :
			self.table[cnt][0] = e
			cnt = cnt + 1
		initStr = '|'.join([str(e) for e in rArray])
		return initStr
	def drawChess(self, x = 1, y = 1) : # 畫棋盤上所有棋子
		self.chess(x, y)
		for k in list(self.table.keys()) :
			pos = self.chessPos(k)
			if self.table[k][1] :
				self.chessman(pos[0], pos[1], CHESSMAN[self.table[k][0]][0])
			else :
				self.chessman(pos[0], pos[1], u'？')
	def drawChessman(self, x = 1, y = 1) :
		pass
	def act(sx = -1, sy = -1, tx = -1, ty = -1) :
		pass
		# > 0, > 0, -1, -1 掀子
	def move(self, Op) :
		sel = False
		newX = self.pos[0]
		newY = self.pos[1]
		# print(self.chessPos(self.pos))
		# self.chessman(self.pos[0], self.pos[1], CHESSMAN[self.table[self.chessPos(self.pos)][0]][0])
		
		if Op == KEY_UP :
			newY = self.pos[1] - 1
		elif Op == KEY_DOWN :
			newY = self.pos[1] + 1
		elif Op == KEY_LEFT :
			newX = self.pos[0] - 1
		elif Op == KEY_RIGHT :
			newX = self.pos[0] + 1
		elif Op == Enter :
			sel = True
		
		if newX >= 1 and newX <= 8 :
			if not self.pos[0] == newX :
				self.chessman(self.pos[0], self.pos[1], CHESSMAN[self.table[self.chessPos(self.pos)][0]][0])
				self.pos[0] = newX
			
		if newY >= 1 and newY <= 4 :
			if not self.pos[1] == newY :
				self.chessman(self.pos[0], self.pos[1], CHESSMAN[self.table[self.chessPos(self.pos)][0]][0])
				self.pos[1] = newY
				
		if sel :
			if not (self.sel[0]  == -1 and self.sel[1] == -1) : 
				# 做吃子或移棋
				if self.table[self.chessPos(self.pos)][0] == 0 : # 移子
					pass
				else : # 吃子
					pass
				self.chessman(self.sel[0], self.sel[1], CHESSMAN[self.table[self.chessPos(self.sel)][0]][0], self.UNSELECT)
				self.sel = [-1, -1]
			else :
				self.sel[0] = self.pos[0]
				self.sel[1] = self.pos[1]
				if self.table[self.chessPos(self.sel)][0] == 0 : # 沒有棋子
					self.sel = [-1, -1]
				elif self.table[self.chessPos(self.sel)][1] : # 蓋起來的狀態
					pass
				
		if not (self.pos[0]	== self.sel[0] and self.pos[1] == self.sel[1]) :
			self.chessman(self.pos[0], self.pos[1], CHESSMAN[self.table[self.chessPos(self.pos)][0]][0], self.SELECT)
		if not (self.sel[0]  == -1 and self.sel[1] == -1) :
			if self.table[self.chessPos(self.sel)][0] == 0 : # 沒有棋子
				self.chessman(self.sel[0], self.sel[1], CHESSMAN[self.table[self.chessPos(self.sel)][0]][0], self.UNSELECT)
				self.sel = [-1, -1]
			else :
				self.chessman(self.sel[0], self.sel[1], CHESSMAN[self.table[self.chessPos(self.sel)][0]][0], self.SELECTED) # 顯示選擇的棋子
	
if __name__ == "__main__" :
	initscr()
	clsscr()
	
	#chess(10, 5)
	#chessSet(3, 3)
	
	#print(chessPos((1, 1)))
	#print(chessPos(2))
	#print(chessPos(31))
	#print(chessPos(11))
	#print(chessPos(21))
	
	#print(initChess().split('|'))
	#print(chessTable())
	
	# initA = initChess().split('|')
	
	# chess()
	# xy  = 0
	
	# i = 0
	# for e in initA :
	#	xy = chessPos(int(i))
	#	chessSet(xy[0], xy[1], CHESSMAN[int(e)][0])
	#	i = i + 1
	
	ch = Chess()
	ch.initChess()
	ch.drawChess()
	
	while True :
		value = getKey()
		ch.move(value)
		pass
	