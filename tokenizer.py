import enum


# enumeration for tokenTypes
class TokenType(enum.Enum):
	KEYWORD = 1
	SYMBOL = 2
	IDENTIFIER = 3
	INT_CONST = 4
	STRING_CONST = 5


class Keyword(enum.Enum):
	CLASS = 1
	METHOD = 2
	FUNCTION = 3
	CONSTRUCTOR = 4
	INT = 5
	BOOLEAN = 6
	CHAR = 7
	VOID = 8
	VAR = 9
	STATIC = 10
	FIELD = 11
	LET = 12
	DO = 13
	IF = 14
	ELSE = 15
	WHILE = 16
	RETURN = 17
	TRUE = 18
	FALSE = 19
	NULL = 20
	THIS = 21


''' jack grammar guide for tokenizer.py

	lexical elements → the jack language includes five categories of terminal 
	elements, also known as tokens:
	
	keyword:
		class constructor function method field static var
		int char boolean
		void true false null this let do if else while return
	symbol: 
		{}()[].,;+-*/*|<>=~
		
	integerConstant: 
		a decimal number in the range 0... 32767
		
	StringConstant: 
		a sequence of Unicode chars not including double quotes or \n surrounded 
		by double quotes
		
	identifier: 
		a sequence of letters, digits, and underscore not starting with a digit
'''


class JackTokenizer:
	def __init__(self, filename):
		"""
		opens a .jack file and saves all .jack commands for later processing.
		strips whitespace, full-line comments, and inline comments

		:return: nothing, but fills self.jack_commands array
		"""

		jack_file = open(filename, 'r')
		lines = jack_file.readlines()
		self.jackCommands = ""  # all commands in one string, inc. newlines
		self.commandIndex = 0  # current index in above string
		self.currentCommand = None  # initially there is no current command
		self.currentTokenType = None  # set in advance()
		self.symbols = "{}[]().,;+-*/|<>=~"
		self.keywords = [
			'class',
			'constructor',
			'function',
			'method',
			'field',
			'static',
			'var',
			'int',
			'char',
			'boolean',
			'void',
			'true',
			'false',
			'null',
			'this',
			'let',
			'do',
			'if',
			'else',
			'while',
			'return'
		]

		for line in lines:
			# ignore whitespace
			if line == '\n':
				continue

			# ignore entire-line comments
			if line[0] == '/' and line[1] == '/':
				continue

			# ignore comments that start with /**
			# TODO add case if this appears mid-line: slice!
			#  but what about multiline?
			if line[0] == '/' and line[1] == '*' and line[2] == '*':
				continue

			# ignore mid-line comments
			try:
				index = line.index('//')
				line = line[0:index]
			except ValueError:
				# '//' wasn't found!
				pass

			# strip whitespace
			line = line.strip()

			# combine lines into a single string separated by newlines
			# later, we can count our current line via newline characters?
			# unless newline chars are present in .jack file strings, too.
			self.jackCommands += line + '\n'
		print(self.jackCommands)

	# probably not needed
	def testLine(self, line: str):
		# test function with single line input
		self.commandIndex = 0
		return

	# unnecessary; not part of the API
	def getJackCommands(self):
		return self.jackCommands

	def hasMoreTokens(self):
		# let's say the command string is length 5. we've processed indices
		# 0,1,2,3,4. when we're done with the last token, advance should
		# increment the index to 5. thus, hasMoreTokens should return false
		# if the commandIndex is greater than or equal to its length.
		return self.commandIndex < len(self.jackCommands)

	def advance(self):
		# keyword → starts with alphabetic character.
		# 	try token.lower().isAlpha()
		#	lower() does not mutate
		# make keywords list. append until next delimiter
		# then check in keywords. if not keyword, probably an identifier

		# skip whitespace and newlines after tokens
		currentChar: str = self.jackCommands[self.commandIndex]
		if (currentChar == ' ') or (currentChar == '\n'):
			self.commandIndex += 1

		print(f'current char: {self.jackCommands[self.commandIndex]}')

		stringBuffer: str = ''
		while not self.__isDelimiter(self.jackCommands[self.commandIndex]):
			stringBuffer += self.jackCommands[self.commandIndex]
			self.commandIndex += 1
		print(f'token: {stringBuffer}')
		print(f'index: {self.commandIndex}')

		# detect keyword
		if self.__isKeyword(stringBuffer):
			self.currentTokenType = TokenType.KEYWORD
			print(f'tokenType {self.currentTokenType} detected')

		# if it's not a keyword, it should be an identifier


		# integerConstant: must be in "0123456789" until a delimiter

		# stringConstant:
		#
		# signified with ", then find index of next "
		# throw error if second " doesn't exist on same line
		# ignore spaces inside



		# set token type
		self.currentTokenType = TokenType.KEYWORD

	# returns true if next char is ⎵, \n, symbol
	def __isDelimiter(self, char: str):
		return self.__isSymbol(char) or (char == ' ') or (char == '\n')

	# returns true if character input is in our symbols list
	def __isSymbol(self, char: str):
		return char in self.symbols

	# returns true if input string is a keyword
	def __isKeyword(self, token: str):
		return token in self.keywords

	def getTokenType(self):
		return self.currentTokenType

	def keyWord(self):
		# assert tokenType
		pass

	def symbol(self):
		pass

	def identifier(self):
		pass

	def intVal(self):
		pass

	def stringVal(self):
		pass

