import struct

OpCode = "Operation Code"
MessageType = "Message Type"
Option = "Option"
	
# option code
Account = 0
Password = 1
Message = 2
From = 3
To = 4

# MessageType

AuthReq = 0
AuthRes = 1 
Push = 2 # push message one time
Keep = 3 # keep chating with some body

# OpCode

BROADCAST = 0
PRIVATE = 1


Format = {
		OpCode : "!B",
		MessageType : "!B"
	}

# option format (-1 is var len)
OptFormat = {
		Account : (Account, -1, [], 'B'),
		Password : (Password, -1, [], 'B'),
		Message : (Message, -1, [], 'B'),
		From : (From, -1, [], 'B'),
		To : (To, -1, [], 'B') 
	}
	
# offset
offset = {
		OpCode : (0, 1),
		MessageType : (1, 2),
		Option : (2, 8192)
	}

class ChatRoomPacket :
	def __init__(self) :
		self.Data = {
			"Operation Code" : 0, 
			"Message Type" : 0,
			"Option" : []
		}
		
	def pack(self) :
		data = b''
		data += struct.pack('!B', self.Data[OpCode])
		data += struct.pack('!B', self.Data[MessageType])
		data += self.packOpt()
		return data
		
	def packOpt(self) :
		b = b''
		f = ""
		for e in self.Data[Option] :
			S = ""
			f = ""
			
			if e[0] == Account :
				f += ''.join(['B' for i in range(len(e[2][0]))])
				S = [ord(C) for C in list(e[2][0])]
			elif e[0] == Password :
				f += ''.join(['B' for i in range(len(e[2][0]))])
				S = [ord(C) for C in list(e[2][0])]
			elif e[0] == Message :
				f += ''.join(['B' for i in range(len(e[2][0]))])
				S = [ord(C) for C in list(e[2][0])]
			elif e[0] == From :
				f += ''.join(['B' for i in range(len(e[2][0]))])
				S = [ord(C) for C in list(e[2][0])]
			elif e[0] == To :
				f += ''.join(['B' for i in range(len(e[2][0]))])
				S = [ord(C) for C in list(e[2][0])]
				
			f = "!BB" + f
			
			L = e[1]
			if L == -1 :
				L = len(S)
				
			b += struct.pack(f, e[0], L, *S)
		return b
		
	def unpackFixLen(self, binsrc, start, Offset, Type) :
		newStart = start + Offset + 1
		size = struct.unpack("!B", binsrc[newStart])
		size = size[0]
		nop = size + 1
		newStart = newStart + 1
		content = binsrc[newStart:newStart + size]
		row = self.getOptRow(Type)
		row = row[0:3]
		format = '!' + Type[3]
		return (row, size, content, format, nop)
		
	def unpackVarLen(self, binsrc, start, Offset, Type, typeFix = 1, TLen = 1) :
		newStart = start + Offset + 1
		if TLen == 1 :
			size = struct.unpack("!B", binsrc[newStart:newStart+TLen])
			size = size[0]
		elif TLen == 2 :
			size = struct.unpack("!H", binsrc[newStart:newStart+TLen])
			size = size[0]
		elif TLen == 4 :
			size = struct.unpack("!I", binsrc[newStart:newStart+TLen])
			size = size[0]
		elif TLen > 4 :
			raise RuntimeError
		nop = size + 1
		newStart = newStart + TLen
		content = binsrc[newStart:newStart + size]
		row = self.getOptRow(Type)
		row = row[0:3]
		format = Type[3]
		size = int(size/typeFix)
		format = "!BB" + format*size
		return (row, size, content, format, nop)
		
	def unpack(self, binstr) :
		self.Data[Option] = []
		
		# print(Format[OpCode])
		# print(binstr)
		
		data = ''
		
		try :
			start, end = offset[OpCode]
			data = struct.unpack(Format[OpCode], binstr[start:end])
			self.Data[OpCode] = data[0]
			
			start, end = offset[MessageType]
			data = struct.unpack(Format[MessageType], binstr[start:end])
			self.Data[MessageType] = data[0]
			
			start, maxEnd = offset[Option] 
		except struct.error :
			print('Incorrect packet format !')
			return False
			pass
		
		Offset = 0
		nop = 0
		size = 0
		content = []
		row = []
		format = []
		
		try :
		
			for E in binstr[start:len(binstr)] : 
				if nop > 0 :
					Offset = Offset + 1
					nop = nop - 1
					continue
				elif int(E) == Account :
					row,size,content,format,nop = self.unpackVarLen(binstr, start, Offset, OptFormat[Account])
				elif int(E) == Password :
					row,size,content,format,nop = self.unpackVarLen(binstr, start, Offset, OptFormat[Password])
				elif int(E) == Message :
					row,size,content,format,nop = self.unpackVarLen(binstr, start, Offset, OptFormat[Message])
				elif int(E) == From :
					row,size,content,format,nop = self.unpackVarLen(binstr, start, Offset, OptFormat[From])
				elif int(E) == To :
					row,size,content,format,nop = self.unpackVarLen(binstr, start, Offset, OptFormat[To])
				else :
					print('Error format')
					pass
				
				format = '!' + format[3:len(format)] 
				
				row[0] = E
				row[1] = size
				
				if E in [Account, Password, Message, From, To] :
					row[2] = [''.join([chr(C) for C in list(struct.unpack(format, content))])]
					
				Offset = Offset + 1
				self.Data[Option].append(row)
		except struct.error :
			print('Incorrect packet format !')
			return False
			pass	
	def getOptRow(self, OptRow) :
		return [E for E in OptRow]
		
def str2F(str) :
	return '!' + ''.join(['B' for i in range(len(str))])
	
def str2B(str) :
	return [ord(C) for C in str]
	
def B2str(str) :
	return ''.join([chr(B) for B in str])
	
def str2b(str) :
	f = '!' + ''.join(['B' for i in range(len(str))])
	S = [ord(C) for C in str]
	return struct.pack(f, *S)
	
def b2str(bin) :
	f = '!' + ''.join(['B' for i in range(len(bin))])
	S = struct.unpack(f, bin)
	str = [chr(B) for B in S]
	return ''.join(str)
	
def str2D(str) :
	D = dict()
	seg = str.split("&")
	for s in seg :
		s = s.split("=")
		D[s[0]] = s[1]
	return D
	
def b2D(bin) :
	return str2D(b2str(bin))
			
'''if __name__ == "__main__" :
	p = ChatRoomPacket()
	p.Data[OpCode] = 100
	p.Data[MessageType] = 100
	F = p.getOptRow(OptFormat[Password])
	print(F)
	F[2].append("apple")
	p.Data[Option].append(F)
	
	
	print(p.Data)
	
	binstr = p.pack()
	p.unpack(binstr)
	
	print(p.Data) '''
	
	