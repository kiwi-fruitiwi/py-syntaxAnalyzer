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
#	classVarDec: static|field type varName(,varName)*;
#	type: int char boolean className
#	subroutineDec: (constructor|function|method)
#		(void|type) subroutineName(parameterList) subroutineBody
#	parameterList: (type varName) (, type varName)*)?
#	subroutineBody: {varDec* statements}
#	varDec: var type varName (, varName)*;
#	className: identifier
#	subroutineName: identifier
#	varName: identifier
#
# statements →
#	statements: statement*
#	statement: letStatement ifStatement whileStatement doStatement returnStatement
#	letStatement: let varName([expression])? = expression;
#	ifStatement: if(expression){statements}(else{statements})?
#	whileStatement: while(expression){statements}
#	doStatement: do subroutineCall;
#	returnStatement: return expression?;
#
# expressions →
#	expression: term (op term)*
#	term: integerConstant | stringConstant | keywordConstant | varName |
#		varName[expression] | subroutineCall | (expression) | unaryOp term
#	subroutineCall: subName(expressionList) |
#		(className | varName).subroutineName(expressionList)
#	expressionList: (expression(, expression)*)?
#	op: + - * / & | < > =
#	unaryOp: - ~
#	keywordConstant: true false null this
#
#
#
#
#
#
# ? statements → a Jack program includes statements, as follows:
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