# no one knows why it's called CompilationEngine. this is a parser that feeds
# from syntaxAnalyzer output:  "a Jack analyzer that makes use of Tokenizer's
# services"
#
# step 1: basic compilationEngine that handles everything but expressions
# step 2: add handling of expressions
#
# the tokenizer handles lexical elements, while the compilationEngine handles
# the following: program structure, statements, and expressions
#
# program structure →
# 	class: 'class' className '{' classVarDec* subroutineDec* '}'
#
#
# statements →
# 	statement: 		ifStatement | whiteStatement | letStatement
# 	statements:		statement*
# 	ifStatement:	if (expression) {statements}
# 	whiteStatement:	while (expression) {statements}
# 	letStatement:	let varName = expression;
# 	expression: 	term (op term)?
# 	term:			varName | constant
# 	varName:		a string not beginning with a digit
# 	constant:		a decimal number
# 	op:				+, -, =, >, <
#
# expressions
#	expression: term (op term)*
#
#
#

class CompilationEngine:
	def compileStatements(self):
		pass

	def compileIfStatement(self):
		pass

	def compileWhileStatement(self):
		self.eat('while')
		self.eat(')')
		self.compileExpression()
		self.eat(')')

	def compileExpression(self):
		pass

	# insert all the rules, minus the 5:
	# type, className, subRoutineName, variableName, statement, subroutineCall

	def compileTerm(self):
		pass

	def eat(self, token: str):
		pass