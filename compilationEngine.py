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

# 2022.10.07 ⊼² current puzzles
# 	how to detect if an expression exists for expressionList
# 		don't we have to advance? set flag to skip next adv I guess
# 		but then we have to check if the next token is an expression
# 			seems like a complicated test
# 	detecting names: class, subRoutine, var
# 		it's an identifier
# 			index 0 capital → className
# 			subroutineName preceded by '.', but now do we detect that?
# 				set previous token?
# 	compileIdentifier: why do we have this?
#
# every rule has an associated compile method (15 total methods) except 6:
#   type, className, subRoutineName, variableName, statement, subroutineCall
#   the logic of these 6 rules is handled by the rules who invoke them
#   e.g. there is no compileStatement because statement has subtypes, and it's
#   split into compileIf, compileWhile, etc.

from tokenizer import JackTokenizer, TokenType


class CompilationEngine:
	"""
	The compilationEngine generates the compiler's output
	"""

	# creates a new compilation engine with the given input and output
	# the next routine called must be compileClass
	def __init__(self, inputJackUri, outputXmlUri):
		# create a Tokenizer object from the inputURI
		self.tk = JackTokenizer(inputJackUri)

		# open file for writing with URI=outputXML
		self.out = open(outputXmlUri, 'w')

		# sometimes compileTerm will need to do an additional advance for LL2.
		# this flag tells us to skip the next advance() if that's the case.
		# foo, foo[expr], foo.bar(exprList), bar(exprList)
		# unsure about difference between Foo.bar(exprList) vs foo.bar(exprList)

		# if true, the next eat() doesn't advance
		self.skipNextAdvance = False
		pass

	# compiles a complete class. called after the constructor
	def compileClass(self):
		o = self.out
		o.write('<class>\n')
		while self.tk.hasMoreTokens():
			self.compileLet()
		o.write('</class>\n')

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

	# eats token = identifier, checks type
	def compileIdentifier(self):
		o = self.out  # makes code more readable

		# we actually don't eat because we're not sure what identifier it is
		# instead, we advance and assert tokenType
		self.tk.advance()
		# print(f'{self.tk.getTokenType()}')
		assert self.tk.getTokenType() == TokenType.IDENTIFIER

		# then write <identifier> value </identifier>
		o.write(f'<identifier> {self.tk.identifier()} </identifier>\n')

	# letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
	def compileLet(self):
		o = self.out

		# 'let'
		self.eat('let')
		o.write('<letStatement>\n')
		o.write('<keyword> let </keyword>\n')

		# className, varName, subRName all identifiers ← 'program structure'
		self.compileIdentifier()

		# check next token for two options: '[' or '='
		self.tk.advance()

		# assert it's a symbol
		assert self.tk.getTokenType() == TokenType.SYMBOL
		assert self.tk.symbol() == '[' or self.tk.symbol() == '='

		# if next token is '[', eat('['), compileExpr, eat(']')
		if self.tk.symbol() == '[':
			self.eat('[', advanceFlag=False)
			o.write('<symbol> [ </symbol>')

			self.compileExpression()

			self.eat(']')
			o.write('<symbol> ] </symbol>')

			self.tk.advance()  # reach the '='

		# we are guaranteed the next symbol is '='
		# eat it, compileExpr, eat(';')
		assert self.tk.symbol() == '='

		self.eat('=', advanceFlag=False)
		o.write('<symbol> = </symbol>\n')

		# TODO # for expressionLess, use term: id, strC, intC
		# TODO can also be true, false, null, this ← keywords!
		# actually these are both taken care of in compileExpr,Term
		self.compileExpression()
		self.eat(';')
		o.write('<symbol> ; </symbol>\n')

		o.write('</letStatement>\n')

	# compiles an if statement, possibly with a trailing else clause
	# if '(' expression ')' '{' statements '}' (else '{' statements '}')?
	def compileIf(self):
		"""
		<ifStatement>
          <keyword> if </keyword>
          <symbol> ( </symbol>
          <expression>
            <term>
              <identifier> b </identifier>
            </term>
          </expression>
          <symbol> ) </symbol>
          <symbol> { </symbol>
          <statements>
          </statements>
          <symbol> } </symbol>
          <keyword> else </keyword>
          <symbol> { </symbol>
          <statements>
          </statements>
          <symbol> } </symbol>
        </ifStatement>
		:return:
		"""
		o = self.out
		# if '(' expression ')'
		self.eat('if')
		o.write('<ifStatement>')

		self.eat('(')
		o.write('<symbol> ( </symbol>')
		self.compileExpression()
		self.eat(')')
		o.write('<symbol> ) </symbol>')

		# '{' statements '}'
		self.__compileStatementsWithinBrackets()

		# (else '{' statements '}')?
		self.tk.advance()  # check for else token
		if self.tk.getTokenType() == TokenType.KEYWORD:
			if self.tk.keyWord() == 'else':
				self.__compileStatementsWithinBrackets()
			else:  # we've already advanced once to check the else keyword
				self.skipNextAdvance = True

		o.write('</ifStatement>\n')

	def __compileStatementsWithinBrackets(self):
		self.eat('{')
		o.write('<symbol> { </symbol>')
		self.compileStatements()
		self.eat('}')
		o.write('<symbol> } </symbol>')

	# 'while' '(' expression ')' '{' statements '}'
	def compileWhile(self):
		o = self.out

		# 'while'
		self.eat('while')
		o.write('<whileStatement>\n')
		o.write('<keyword> while </keyword>\n')

		# '(' expression ')'
		self.eat('(')
		o.write('<symbol> ( </symbol>\n')
		self.compileExpression()
		self.eat(')')
		o.write('<symbol> ) </symbol>\n')

		# '{' statements '}'
		self.eat('{')
		o.write('<symbol> { </symbol>\n')
		self.compileStatements()
		self.eat('}')
		o.write('<symbol> } </symbol>\n')

		o.write('</whileStatement>\n')

	def compileDo(self):
		pass

	def compileReturn(self):
		pass

	# compiles a term. if the current token is an identifier, the routine must
	# distinguish between a variable, an array entry, or a subroutine call. a
	# single look-ahead token, which may be one of [, (, or ., suffices to
	# distinguish between the possibilities. any other token is not part of this
	# term and should not be advanced over.
	#
	# the output should be wrapped with <term></term> with the value inside:
	#   <integerConstant> 1 </integerConstant>
	#   <identifier> i </identifier>
	#   <keyword> false </keyword>
	#   <keyword> null </keyword>
	#   <keyword> this </keyword>
	def compileTerm(self):
		o = self.out
		# TODO varName | constant, but the full grammar rule is:
		# integerConstant stringConstant keywordConstant varName
		# varName '[' expression ']' subroutineCall '(' expression ')'
		# unaryOp term

		# TODO 1st pass: term should just be int,str,keyword,identifier with no
		# TODO varName[expr] or subCall(expr)
		# TODO but probably unaryOp term is fine. unaryOps are - and ~

		# 🏭 integerConst stringConst keywordConst identifier unaryOp→term
		# remember that keywordConstants are false, true, null, this
		self.tk.advance()
		match self.tk.getTokenType():
			case TokenType.IDENTIFIER:
				value = self.tk.identifier()

				# we need to advance one more time to check 4 LL2 cases
				# we already advanced, so don't advance the next time we need to
				# self.eat. if this flag is true when eat is called, don't
				# advance. reset the flag instead.
				# TODO somewhere else this happens. we can just set the flag
				self.tk.advance()
				self.skipNextAdvance = True

				tokenType = self.tk.getTokenType()
				match tokenType:
					case TokenType.SYMBOL:
						advTokenValue = self.tk.symbol()
						if advTokenValue == '.':
							# TODO process subroutineCall
							pass
						if advTokenValue == '(':
							# TODO process subroutineCall
							pass
						if advTokenValue == '[':
							# TODO process varName[expression]
							pass
					case _:
						raise TypeError(f'')

				o.write(f'<identifier> {value} </identifier>\n')
			case TokenType.KEYWORD:
				value = self.tk.keyWord()
				assert value in ['true', 'false', 'null', 'this'], value
				o.write(f'<keyword> {value} </keyword>\n')
			case TokenType.INT_CONST:
				value = self.tk.intVal()
				o.write(f'<integerConstant> {value} </integerConstant>\n')
			case TokenType.STRING_CONST:
				value = self.tk.stringVal()
				o.write(f'<stringConstant> {value} </stringConstant>\n')
			case TokenType.SYMBOL:
				value = self.tk.symbol()
				# this will be unaryOp term: write op, recursively compileTerm
				# but it can't be another unaryOp term?
				pass
			case _:
				raise TypeError(f'invalid TokenType: {self.tk.getTokenType()}')

	# not used in the first pass
	def compileExpression(self):
		# temporarily call compileTerm for expressionLessSquare testing
		# when we're ready to test expressions, then we can test Square
 		self.compileTerm()

	# compiles a (possibly empty) comma-separated list of expressions
	# (expression (, expression)*)?
	def compileExpressionList(self):
		# how do we check if an expression exists?
		# we could check if the first part is a term...

		# then advance to check for symbol ','
		# if symbol is ',': compileExpression(), repeat

		pass

	# we must have two versions of eat: one with advance and one without
	# this is for cases with ()? or ()* and we must advance first before
	# checking the token, e.g.
	# → varDec: 'var' type varName (',' varName)*';'
	# → let: 'let' varName ('[' expression ']')? '=' expression ';'
	def eat(self, expectedToken: str, advanceFlag=True):
		# expected token ← what the compile_ method that calls eat expects
		# actual tokenizer token ← tokenizer.advance
		# note that sometimes we don't advance because the compile method
		# calling this has already done so

		# four cases between doNotAdvWhileEating and advance parameters:
		# skipNextAdvance advanceFlag action
		#               T T           → don't advance()
		#               T F           → don't advance()
		#               F T           → advance(), reset sna
		#               F F           → don't advance(), reset sna
		# ∴ only advance if skipNextAdvance=False, advanceFlag=True

		if not self.skipNextAdvance and advanceFlag:
			# skip advance if flag is on from LL2 read-ahead situation
			# → see term: foo, foo[expr], foo.bar(exprList), bar(exprList)
			# turn off the "skip next eat()'s advance()" toggle if it's on
			self.tk.advance()

		# reset the flag now that we've 'consumed' an eat command
		if self.skipNextAdvance:
			self.skipNextAdvance = False

		tokenType = self.tk.getTokenType()  # current token

		match tokenType:  # determine value of token
			case TokenType.KEYWORD:
				value = self.tk.keyWord()
			case TokenType.SYMBOL:
				value = self.tk.symbol()
			case TokenType.IDENTIFIER:
				value = self.tk.identifier()
			case TokenType.INT_CONST:
				value = self.tk.intVal()
			case TokenType.STRING_CONST:
				value = self.tk.stringVal()
			case _:
				raise TypeError(f'token type invalid: not keyword, symbol, '
								  f'identifier, int constant, or string constant: {tokenType}')
		# assert expectedToken matches actual token
		# print(f'[eating → {value}]')
		assert expectedToken == value, f'expected: {expectedToken}, actual:{value}'


