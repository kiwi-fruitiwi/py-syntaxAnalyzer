import enum


# enumeration for tokenTypes
class TokenType(enum.Enum):
	KEYWORD = 1
	SYMBOL = 2
	ID = 3
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

lexical elements: the jack language includes five types of terminal tokens
keyword:
	class constructor function method field static var
	int char boolean
	void true false null this let do if else while return
symbol: 
	{}()[].,;+-*/*|<>=~
integerConstant: 
	a decimal number in the range 0... 32767
StringConstant: 
	a sequence of Unicode chars not including double quotes or \n
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
		self.jack_commands = []
		self.commandIndex = -1  # current command index;
		self.currentCommand = None  # initially there is no current command

		for line in lines:
			# ignore whitespace
			if line == '\n':
				continue

			# ignore entire-line comments
			if line[0] == '/' and line[1] == '/':
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

			self.jack_commands.append(line)

	def getJackCommands(self):
		return self.jack_commands.copy()

	def hasMoreTokens(self):
		pass

	def advance(self):
		pass

	def getTokenType(self):
		pass
