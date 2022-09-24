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
#   program structure →
#     class: 'class' className '{' classVarDec* subroutineDec* '}'
#     classVarDec: static|field type varName(,varName)*;
# 	  type: int char boolean className
#     subroutineDec: (constructor|function|method)
#     	(void|type) subroutineName(parameterList) subroutineBody
#     parameterList: (type varName) (, type varName)*)?
#     subroutineBody: {varDec* statements}
#     varDec: var type varName (, varName)*;
#     className: identifier
#     subroutineName: identifier
#     varName: identifier
#
#   statements →
#     statements: statement*
#     statement: let if while do return
#     letStatement: let varName([expression])? = expression;
#     ifStatement: if(expression){statements}(else{statements})?
#     whileStatement: while(expression){statements}
#     doStatement: do subroutineCall;
#     returnStatement: return expression?;
#
#   expressions →
#	  expression: term (op term)*
#	  term: integerConstant | stringConstant | keywordConstant | varName |
#	  	varName[expression] | subroutineCall | (expression) | unaryOp term
#	  subroutineCall: subName(expressionList) |
#	  	(className | varName).subroutineName(expressionList)
#	  expressionList: (expression(, expression)*)?
#	  op: + - * / & | < > =
#	  unaryOp: - ~
#	  keywordConstant: true false null this
#
# ⊼².📹 4.5 parser logic recursion
#	statements → a Jack program includes statements, as follows:
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

class CompilationEngine:
	"""
	The compilationEngine generates the compiler's output
	"""

	# creates a new compilation engine with the given input and output
	# the next routine called must be compileClass
	def __init__(self, inputTokenizer, outputXML):

		pass

	# compiles a complete class. called after the constructor
	def compileClass(self):
		pass

	# compiles a static variable or field declaration
	def compileClassVarDec(self):
		pass

	# compiles a complete method, function, or constructor
	def compileSubroutineDec(self):
		pass

	# compiles a (possibly empty) parameter list. does not handle enclosing '()'
	def compileParameterList(self):
		pass

	# compiles a subroutine's body
	def compileSubroutineBody(self):
		pass

	# compiles a var declaration
	def compileVarDec(self):
		pass

	# compiles a sequence of statements. does not handle enclosing '{}'
	def compileStatements(self):
		pass

	def compileLet(self):
		pass

	# compiles an if statement, possibly with a trailing else clause
	def compileIf(self):
		pass

	def compileWhile(self):
		self.eat('while')
		self.eat(')')
		self.compileExpression()
		self.eat(')')

	def compileDo(self):
		pass

	def compileReturn(self):
		pass

	# compiles a term. if the current token is an identifier, the routine must
	# distinguish between a variable, an array entry, or a subroutine call. a
	# single look-ahead token, which may be one of [, (, or ., suffices to
	# distinguish between the possibilities. any other token is not part of this
	# term and should not be advanced over.
	def compileTerm(self):
		pass

	def compileExpression(self):
		pass

	# compiles a (possibly empty) comma-separated list of expressions
	def compileExpressionList(self):
		pass

	def eat(self, expectedToken: str, tokenizerToken: str):
		# expected token ← what the compile_ method that calls eat expects
		# actual tokenizer token ← tokenizer.advance

		# assert expectedToken matches actual token
		assert expectedToken == tokenizerToken
		pass

	# every rule has an associated compile method (15 total methods) except 6:
	# type, className, subRoutineName, variableName, statement, subroutineCall
	# the logic of these 6 rules is handled by the rules who invoke them
	# e.g. there is no compileStatement because statement has subtypes and it's
	# split into compileIf, compileWhile, etc.