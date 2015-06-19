from __future__ import print_function
import os
import colorama
from colorama import Fore, Back, Style
import msvcrt
import struct

# 請先安裝colorama => pip install -U colorama

__keyBase__ = b''

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

def putch(c) :
	if len(c) <= 5 and ord(c) >= 0 and ord(c) <= 255 :
		msvcrt.putch(struct.pack('!B', ord(c)))

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
			
def setFGColor(color, style) :
	if color in FORES and style in STYLES:
		print("%s%s" % (color, style), end='')
	else :
		print('Error Foreground color')
		
def setBGColor(color, style) :
	if color in BACKS and style in STYLES:
		print("%s%s" % (color, style), end='')
	else :
		print('Error Background color')
		
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

if __name__ == "__main__" :
	initscr()
	clsscr()
	setBGColor(Back.YELLOW, Style.NORMAL)
	box(1, 1, 39, 30)
	drawText(5, 3, 'A')
	drawText(7, 3, 'A')
	drawText(9, 3, 'A')
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