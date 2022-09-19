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

		self.code = ""  # all commands in one string, inc. newlines
		self.i = 0  # current index in above monolithic code string
		self.currentTokenType = None  # set in advance()

		# these 5 are used by their respective accessors, e.g. symbol(),
		# keyWord(), intVal(), stringVal(), identifier(). these are called
		# only if the current tokenType matches. invalid otherwise.
		self.currentSymbolValue = None
		self.currentIdentifierValue = None
		self.currentStrConstValue = None
		self.currentIntConstValue = None
		self.currentKeyWordValue = None

		self.symbols = "{}[]().,;+-*/|<>=~"
		self.digits = "0123456789"  # for integer constants
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
			self.code += line + '\n'
		print(self.code)

	# probably not needed
	def testLine(self, line: str):
		# test function with single line input
		self.i = 0
		return

	# unnecessary; not part of the API
	def getJackCommands(self):
		return self.code

	def hasMoreTokens(self):
		# let's say the command string is length 5. we've processed indices
		# 0,1,2,3,4. when we're done with the last token, advance should
		# increment the index to 5. thus, hasMoreTokens should return false
		# if the commandIndex is greater than or equal to its length.
		return self.i < len(self.code)

	def advance(self):
		# 🏭 skip whitespace(s) and single newlines after tokens
		# lines cannot start with spaces, which the constructor handles w/trim()
		while self.code[self.i] == ' ':
			# print(f'→ skipping index for ⎵: {self.code[self.i]}.\n')
			self.i += 1
			if not self.hasMoreTokens():
				return

		if self.code[self.i] == '\n':  # constructor ensures no double \n
			# print(f'→ skipping index for newline: {self.code[self.i]}.\n')
			self.i += 1
			if not self.hasMoreTokens():
				return

		# every lexical category needs to:
		# 	set currentTokenType, currentSymbolValue
		#	increment code index, i, appropriately

		# 🏭 detect symbols
		if self.__isSymbol(self.code[self.i]):
			self.currentTokenType = TokenType.SYMBOL
			self.currentSymbolValue = self.code[self.i]

			# print(f'{self.currentTokenType} detected: →{self.currentSymbolValue}←')
			self.i += 1
			return

		# 🏭 detect string constants
		# 	search rest of string → isn't limited to one line which might be bad
		if self.code[self.i] == '\"':
			nextDoubleQuoteIndex = self.code[self.i+1:].index('\"') + self.i
			# print(f'next double quote index: {nextDoubleQuoteIndex}')

			self.currentTokenType = TokenType.STRING_CONST
			self.currentStrConstValue = self.code[self.i+1:nextDoubleQuoteIndex+1]
			self.i += len(self.currentStrConstValue) + 2
			return

		# 🏭 detect integer constants: decimal numbers in range [0, 32767]
		intBuilder: str = ''
		if self.code[self.i] in self.digits:
			while not self.__isDelimiter(self.code[self.i]) and self.code[self.i] in self.digits:
				intBuilder += self.code[self.i]
				self.i += 1

			# assert value does not overflow, according to spec
			assert 0 <= int(intBuilder) <= 32767

			self.currentTokenType = TokenType.INT_CONST
			self.currentIntConstValue = intBuilder
			# print(f'{self.currentTokenType} detected: {intBuilder}')
			return

		# 🏭 now it's either a keyword or identifier. let's build a string!
		stringBuilder: str = ''
		while not self.__isDelimiter(self.code[self.i]):
			stringBuilder += self.code[self.i]
			self.i += 1

		# 🏭 detect keyword
		# print(f'stringBuffer result: →{stringBuilder}←')
		if self.__isKeyword(stringBuilder):
			self.currentTokenType = TokenType.KEYWORD
			self.currentKeyWordValue = stringBuilder
			# print(f'{self.currentTokenType} detected: {stringBuilder}')
		else:
			# 🏭 detect identifier
			self.currentTokenType = TokenType.IDENTIFIER
			self.currentIdentifierValue = stringBuilder
			# print(f'{self.currentTokenType} detected: {stringBuilder}')

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
		assert self.currentTokenType == TokenType.KEYWORD
		return self.currentKeyWordValue

	def symbol(self):
		assert self.currentTokenType == TokenType.SYMBOL
		return self.currentSymbolValue

	def identifier(self):
		assert self.currentTokenType == TokenType.IDENTIFIER
		return self.currentIdentifierValue

	def intVal(self):
		assert self.currentTokenType == TokenType.INT_CONST
		return self.currentIntConstValue

	def stringVal(self):
		assert self.currentTokenType == TokenType.STRING_CONST
		return self.currentStrConstValue

