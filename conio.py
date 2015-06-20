from __future__ import print_function
import os
import colorama
from colorama import Fore, Back, Style
import msvcrt
import struct

# 請先安裝colorama => pip install -U colorama

__keyBase__ = b''
__chess__x__ = 1
__chess__y__ = 1

# constant value
KEY_ARROW = "KEY_ARROW"
KEY_UP = "KEY_UP"
KEY_DOWN = "KEY_DOWN"
KEY_LEFT = "KEY_LEFT"
KEY_RIGHT = "KEY_RIGHT"

FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

Enter = '\r'
BackSpace = '\x08'
NonASCII = '\xff'

ACTIVE = (Fore.WHITE, Style.NORMAL, Back.YELLOW, Style.BRIGHT) # active 
INACTIVE = (Fore.BLACK, Style.NORMAL, Back.WHITE, Style.NORMAL)

def putch(c) :
	if len(c) <= 5 and ord(c) >= 0 and ord(c) <= 255 :
		msvcrt.putch(struct.pack('!B', ord(c)))
		
def putstr(string) :
	for c in string :
		putch(c)

def getch() :
	return msvcrt.getch()
	
def kbhit() :
	return msvcrt.kbhit()
	

def getKey() : # python windows function call
	global __keyBase__
	kbValue = struct.pack('!B', ord(NonASCII))
	if kbhit() :
		kbValue = getch()
	if kbValue == b'\xe0' :
		__keyBase__ = kbValue
		# print('arrow key base')
		return KEY_ARROW
	else :
		if __keyBase__ == b'\xe0' :
			if kbValue == b'H' : # up
				# print('up')
				__keyBase__ = b''
				return KEY_UP
			elif kbValue == b'P' : # down
				# print('down')
				__keyBase__ = b''
				return KEY_DOWN
			elif kbValue == b'K' : # left
				# print('left')
				__keyBase__ = b''
				return KEY_LEFT
			elif kbValue == b'M' : # right
				# print('right')
				__keyBase__ = b''
				return KEY_RIGHT
			else :
				# print(kbValue)
				__keyBase__ = b''
		elif __keyBase__ == b'\x00' :
			pass
		else :
			# print(kbValue, end = '')
			# print(chr(struct.unpack("!B", kbValue)[0]))
			return chr(struct.unpack("!B", kbValue)[0])

def initscr() :
	colorama.init()
			
def setFGColor(color = Fore.WHITE, style = Style.NORMAL) :
	if color in FORES and style in STYLES:
		print("%s%s" % (color, style), end='')
	else :
		print('Error Foreground color')
		
def setBGColor(color = Back.BLACK, style = Style.NORMAL) :
	if color in BACKS and style in STYLES:
		print("%s%s" % (color, style), end='')
	else :
		print('Error Background color')
		
def defaultColor() :
	setFGColor()
	setBGColor()
		
def gotoxy(x, y) :
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	print('\x1b[%d;%dH' % (y, x), end='')
	
def clsscr() :
	os.system("cls")

def box(x, y, width, height) :
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	gotoxy(x, y)
	print(' '*width*2, end = '')
	for i in range(height) :
		gotoxy(x, y + i)
		print('  ', end = '')
		gotoxy(x + width*2 - 1, y + i)
		print('  ', end = '')
	gotoxy(x, y + height)
	print(' '*(width*2 + 1), end = '')
	
def drawText(x, y, string) :
	gotoxy(x, y)
	print(string, end = '')
	
def active(x = 1, y = 1, string = '') :
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	gotoxy(x, y)
	setFGColor(ACTIVE[0], ACTIVE[1])
	setBGColor(ACTIVE[2], ACTIVE[3])
	print(string, end = '')
	defaultColor()
	
def inactive(x = 1, y = 1, string = '') :
	if x <= 0 :
		x = 1
	if y <= 0 :
		y = 1
	gotoxy(x, y)
	setFGColor(INACTIVE[0], INACTIVE[1])
	setBGColor(INACTIVE[2], INACTIVE[3])
	print(string, end = '')
	defaultColor()
	
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

if __name__ == "__main__" :
	initscr()
	clsscr()
	"""
	setBGColor(Back.YELLOW, Style.NORMAL)
	box(1, 1, 39, 30)
	drawText(5, 3, 'A')
	drawText(7, 3, 'A')
	drawText(9, 3, 'A')
	"""
	
	chess(10, 5)
	chessSet(3, 2)
	
	while True :
		pass
	
	"""
	gotoxy(16, 5)
	input()
	while (True) :
		if kbhit() :
			clsscr()
			setFGColor(Fore.YELLOW, Style.NORMAL)
			gotoxy(16, 5)
			# print(getKey(), end='')
			value = getKey()
			if value == '\r' or value == '\n' :
				print('Enter', end = '')
			elif value == '\x08' :
				print('BackSpace', end = '')
			elif value == KEY_DOWN :
				print('KEY DOWN', end = '')
	"""