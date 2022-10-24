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
		self.skipNextAdvanceOnEat = False
		pass

	# calls compile on whatever needs testing at the moment
	def testCompile(self):
		self.compileClassVarDec()
		pass

	# compiles a complete class. called after the constructor
	def compileClass(self):
		"""
		expected output example:
			<class>
			  <keyword> class </keyword>
			  <identifier> Main </identifier>
			  <symbol> { </symbol>
			  <subroutineDec>
				<keyword> function </keyword>
				<keyword> void </keyword>
				<identifier> main </identifier>
				<symbol> ( </symbol>
				<parameterList>
				</parameterList>
				<symbol> ) </symbol>
				<subroutineBody>
				...

		follows pattern: class className '{' classVarDec* subroutineDec* '}'
		"""
		o = self.out
		o.write('<class>\n')
		self.eat('class')  # this will output <keyword> class </keyword>

		# className is an identifier
		self.compileIdentifier()
		self.eat('{')

		while self.compileClassVarDec():
			continue  # probably unnecessary continue; empty body

		while self.compileSubroutineDec():
			continue

		o.write('</class>\n')

	# compiles a static variable or field declaration
	def compileClassVarDec(self):
		"""
		<classVarDec>
		  <keyword> field </keyword>
		  <keyword> int </keyword>
		  <identifier> size </identifier>
		  <symbol> ; </symbol>
		</classVarDec>

		used by compileClass, following this pattern:
		(static | field) type varName (',' varName)* ';'
		type → int | char | boolean | className
		"""
		o = self.out
		o.write('<classVarDec>\n')

		self.advance()

		# static or field?
		assert self.tk.getTokenType() == TokenType.KEYWORD
		assert self.tk.keyWord() in ['static', 'field']
		o.write(f'<keyword> {self.tk.keyWord()} </keyword>\n')

		self.__compileType()

		# varName(',' varName)*
		self.__compileVarNameList()
		o.write('</classVarDec>\n')

	# helper method for classVarDec, subroutineDec, parameterList, carDec
	def __compileType(self):
		# type → advance, if TokenType is keyword: int char or boolean
		self.advance()
		match self.tk.getTokenType():
			case TokenType.KEYWORD:
				# process int, char, boolean
				assert self.tk.keyWord() in ['int', 'char', 'boolean']
				self.out.write(f'<keyword> {self.tk.keyWord()} </keyword>\n')
			case TokenType.IDENTIFIER:
				# process className
				self.compileIdentifier()
			case _:
				raise ValueError(
					f'did not find identifier or keyword token: {self.tk.getTokenType()}')

	# compiles a complete method, function, or constructor
	def compileSubroutineDec(self):
		pass

	# compiles a (possibly empty) parameter list. does not handle enclosing '()'
	def compileParameterList(self):
		"""
		<parameterList>
		  <keyword> int </keyword>
		  <identifier> Ax </identifier>
		  <symbol> , </symbol>
		  <keyword> int </keyword>
		  <identifier> Ay </identifier>
		  <symbol> , </symbol>
		  <keyword> int </keyword>
		  <identifier> Asize </identifier>
		</parameterList>

		follows pattern:
			((type varName) (, type varName)*)?
			note that the entire pattern could be empty
				the character after parameterList ends is always ')'
		"""
		o = self.out
		o.write('<parameterList>\n')

		self.advance(skipNextAdvOnEat=True)

		# if next symbol is ')', end the parameterList
		if self.tk.getTokenType() == TokenType.SYMBOL:
			o.write('</parameterList>\n')
			return

		# otherwise the next symbol MUST be a type: int char bool className
		# consume: type varName
		self.__compileType()  # type
		self.compileIdentifier()  # varName

		# then while next token is ',', consume type varName
		self.advance(skipNextAdvOnEat=True)

		# pattern: (, type varName)*
		# next token must be either ',' or ';'
		assert self.tk.getTokenType() == TokenType.SYMBOL
		while self.tk.symbol() == ',':
			self.eat(',')
			self.compileIdentifier()
			self.advance(skipNextAdvOnEat=True)  # check next symbol: ',' or ';'

		# if not ',', must be ')' → end parameterList
		assert self.tk.symbol() == ';'
		self.eat(';')
		o.write('</parameterList>\n')

	# compiles a subroutine's body
	def compileSubroutineBody(self):
		pass

	# compiles a var declaration
	def compileVarDec(self):
		"""
	    <varDec>
	    	<keyword> var </keyword>
	    	<identifier> Array </identifier>
	    	<identifier> a </identifier>
	    	<symbol> ; </symbol>
	    </varDec>
	    <varDec>
	    	<keyword> var </keyword>
	    	<keyword> int </keyword>
	    	<identifier> length </identifier>
	    	<symbol> ; </symbol>
	    </varDec>
	    <varDec>
	    	<keyword> var </keyword>
	    	<keyword> int </keyword>
	    	<identifier> i </identifier>
	    	<symbol> , </symbol>
	    	<identifier> sum </identifier>
	    	<symbol> ; </symbol>
	    </varDec>

	    pattern: var type varName (',' varName)*';'
		"""
		o = self.out
		o.write('<varDec>\n')

		# var

		# type

		# varName

		# (',' varName)*';'

		o.write('</varDec>\n')

	# compiles a sequence of statements. does not handle enclosing '{}'
	# a statement is one of 5 options: let, if, while, do, return
	# statements is statement*, meaning it can be nothing
	def compileStatements(self):
		"""
		<statements>
            <letStatement>
              <keyword> let </keyword>
              <identifier> a </identifier>
              <symbol> [ </symbol>
              <expression>
                <term>
                  <identifier> i </identifier>
                </term>
              </expression>
              <symbol> ] </symbol>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> Keyboard </identifier>
                  <symbol> . </symbol>
                  <identifier> readInt </identifier>
                  <symbol> ( </symbol>
                  <expressionList>
                    <expression>
                      <term>
                        <stringConstant> ENTER THE NEXT NUMBER:  </stringConstant>
                      </term>
                    </expression>
                  </expressionList>
                  <symbol> ) </symbol>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> i </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> i </identifier>
                </term>
                <symbol> + </symbol>
                <term>
                  <integerConstant> 1 </integerConstant>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
          </statements>
		:return:

		statements is found in if, while, and subroutineBody
			if (expression) {statements} else {statements}
			while (expression) {statements}
			{varDec* statements}

		note that statements always ends in '}'!
		"""
		o = self.out
		o.write('<statements>\n')

		# we want to try to compile {let, if, while, do, return} statements
		# until we run out of those keywords
		# ✒note! currently statements always ends with }
		while self.__compileStatement():
			# empty because we want to stop when it returns false
			continue  # probably not necessary

		o.write('</statements>\n')

	# helper method for compileStatements, returning false if
	# {let if while do return} are not found
	def __compileStatement(self):
		"""

		:return: true if a statement was found, false if not
		"""
		self.advance()
		self.skipNextAdvanceOnEat = True

		# if compileStatement is being called, tokenType must be one of
		# {let, if, while, do, return}
		if self.tk.getTokenType() != TokenType.KEYWORD:
			return False
		else:
			match self.tk.keyWord():
				case 'let':
					self.compileLet()
					return True
				case 'if':
					self.compileIf()
					return True
				case 'while':
					self.compileWhile()
					return True
				case 'do':
					self.compileDo()
					return True
				case 'return':
					self.compileReturn()
					return True
				case _:
					raise ValueError(f'did not find let, if, while, do, or return → {self.tk.keyWord()}')

	# helper method for compileClassVarDec, compileVarDec
	# classVarDec pattern: (static | field) type varName (, varName)* ';'
	# varDec: var type varName (, varName)* ';'
	#
	# the pattern we are targeting is:
	# 	varName (',' varName)*;
	# the goal is to implement this repeated handling code once here
	def __compileVarNameList(self):
		# varName
		self.compileIdentifier()
		self.advance(skipNextAdvOnEat=True)  # check ahead to see: ',' or ';' ?

		# (',' varName)*
		while self.tk.symbol() == ',':
			self.eat(',')
			self.compileIdentifier()
			self.advance(skipNextAdvOnEat=True)

		# the only token we have left is ';'
		self.eat(';')

	# eats token = identifier, checks type
	def compileIdentifier(self):
		o = self.out  # makes code more readable

		# we actually don't eat because we're not sure what identifier it is
		# instead, we advance and assert tokenType
		self.advance()
		# print(f'{self.tk.getTokenType()}')
		assert self.tk.getTokenType() == TokenType.IDENTIFIER

		# then write <identifier> value </identifier>
		o.write(f'<identifier> {self.tk.identifier()} </identifier>\n')

	def compileLet(self):
		"""
		letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
		:return:
		"""
		o = self.out

		# 'let'
		o.write('<letStatement>\n')
		self.eat('let')

		# className, varName, subRName all identifiers ← 'program structure'
		self.compileIdentifier()

		# check next token for two options: '[' or '='
		self.advance(skipNextAdvOnEat=True)

		# assert it's a symbol
		assert self.tk.getTokenType() == TokenType.SYMBOL
		assert self.tk.symbol() == '[' or self.tk.symbol() == '='

		# if next token is '[', eat('['), compileExpr, eat(']')
		if self.tk.symbol() == '[':
			self.eat('[')
			self.compileExpression()
			self.eat(']')
			self.advance()  # reach the '='

		# we are guaranteed the next symbol is '='
		# eat it, compileExpr, eat(';')
		assert self.tk.symbol() == '='

		self.eat('=')

		# TODO # for expressionLess, use term: id, strC, intC
		# TODO can also be true, false, null, this ← keywords!
		# actually these are both taken care of in compileExpr,Term
		self.compileExpression()
		self.eat(';')

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
		o.write('<ifStatement>')
		self.eat('if')
		self.__compileExprWithinParens()

		# '{' statements '}'
		self.__compileStatementsWithinBrackets()

		# (else '{' statements '}')?
		self.advance()  # check for else token
		if self.tk.getTokenType() == TokenType.KEYWORD:
			if self.tk.keyWord() == 'else':
				self.__compileStatementsWithinBrackets()
			else:  # we've already advanced once to check the else keyword
				self.skipNextAdvanceOnEat = True

		o.write('</ifStatement>\n')

	def __compileExprWithinParens(self):
		self.eat('(')
		self.compileExpression()
		self.eat(')')

	def __compileStatementsWithinBrackets(self):
		self.eat('{')
		self.compileStatements()
		self.eat('}')

	# 'while' '(' expression ')' '{' statements '}'
	def compileWhile(self):
		o = self.out

		# 'while'
		o.write('<whileStatement>\n')
		self.eat('while')

		# '(' expression ')'
		self.__compileExprWithinParens()

		# '{' statements '}'
		self.__compileStatementsWithinBrackets()

		o.write('</whileStatement>\n')

	# 'do' subroutineCall ';'
	def compileDo(self):
		"""
		<doStatement>
          <keyword> do </keyword>
          <identifier> Memory </identifier>
          <symbol> . </symbol>
          <identifier> deAlloc </identifier>
          <symbol> ( </symbol>
          <expressionList>
            <expression>
              <term>
                <keyword> this </keyword>
              </term>
            </expression>
          </expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
		:return:
		"""
		o = self.out

		o.write('<doStatement>\n')
		self.eat('do')

		# subroutineName '(' expressionList ')' |
		# (className | varName) '.' subroutineName '(' expressionList ')'
		#
		# two possibilities:
		# 	identifier (className | varName) → '.' e.g. obj.render(x, y)
		# 	identifier (subroutineName) → '(' e.g. render(x, y)
		self.advance()
		o.write(f'<identifier> {self.tk.identifier()} </identifier')

		self.advance(skipNextAdvOnEat=True)

		# handling the ',render' subroutineName after '.'
		if self.tk.symbol() == '.':
			self.eat('.')
			# advance and grab the subroutineName
			self.advance()
			o.write(f'<identifier> {self.tk.identifier()} </identifier')

		# then eat('(') → compileExpressionList
		self.eat('(')
		self.compileExpressionList()  # TODO currently takes care of ending ')'

		# ';'
		self.eat(';')
		o.write('</doStatement>\n')

	# 'return' expression? ';'
	def compileReturn(self):
		"""
		<returnStatement>
          <keyword> return </keyword>
          <expression>
            <term>
              <identifier> x </identifier>
            </term>
          </expression>
          <symbol> ; </symbol>
        </returnStatement>

		:return:
		"""
		o = self.out

		# 'return'
		o.write('<returnStatement>\n')
		self.eat('return')

		# expression? ';'
		# the next token is either a ';' or an expression
		# expressions are more difficult to check for so, check for symbol ';'
		# if it's a ';' we're done! although unary ops can start terms
		self.advance(skipNextAdvOnEat=True)

		if self.tk.getTokenType() == TokenType.SYMBOL:
			currentSymbol = self.tk.symbol()
			if currentSymbol == ';':
				# we already advanced! set advanceFlag anyway. redundant with
				# self.skipNextAdvance being True though.
				self.eat(';')
			else:
				# unaryOp is part of the definition of a term
				if currentSymbol == '-' or currentSymbol == '~':
					self.compileExpression()
		else:
			self.compileExpression()

		o.write('</returnStatement>\n')

	# the expressionless tests for project 10 use simplified 'term' tokens
	# that can only be single identifiers or the keyword 'this'.
	def compileSimpleTerm(self):
		o = self.out
		# the simple version of this rule is identifier | 'this' ←🦔
		self.advance()

		match self.tk.getTokenType():
			case TokenType.IDENTIFIER:
				o.write(f'<identifier> {self.tk.identifier()} </identifier>\n')
			case TokenType.KEYWORD:
				assert self.tk.keyWord() == 'this'
				o.write(f'<keyword> {self.tk.keyWord()} </keyword>\n')

			# adding extra cases: integer and string constant
			case TokenType.INT_CONST:
				value = self.tk.intVal()
				o.write(f'<integerConstant> {value} </integerConstant>\n')
			case TokenType.STRING_CONST:
				value = self.tk.stringVal()
				o.write(f'<stringConstant> {value} </stringConstant>\n')
			case _:
				raise ValueError(f'simple term was not an identifier or "this"')

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
		self.advance()
		match self.tk.getTokenType():
			case TokenType.IDENTIFIER:
				value = self.tk.identifier()

				# we need to advance one more time to check 4 LL2 cases
				# we already advanced, so don't advance the next time we need to
				# self.eat. if this flag is true when eat is called, don't
				# advance. reset the flag instead.
				# TODO somewhere else this happens. we can just set the flag
				self.advance(skipNextAdvFlag=True)

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
 		self.compileSimpleTerm()

	# compiles a (possibly empty) comma-separated list of expressions
	# (expression (',' expression)*)?
	def compileExpressionList(self):
		"""
		empty expressionList tags are a possibility
			<expressionList>
			</expressionList>

		otherwise, expressions separated by ',' symbols: x, y, z
			<expressionList>
			<expression>
			  <term>
				<identifier> x </identifier>
			  </term>
			</expression>
			<symbol> , </symbol>
			<expression>
			  <term>
				<identifier> y </identifier>
			  </term>
			</expression>
			</expressionList>
		:return:
		"""
		# (expression (',' expression)*)?

		o = self.out
		o.write('<expressionList>')
		# how do we check if an expression exists? if it's ')', exprList empty
		# e.g. out.write('compiler') vs out.write()
		# hitting the last ')' ensures the expressionList is done
		self.advance(skipNextAdvOnEat=True)

		if self.tk.symbol() == ')':
			self.eat(')')
			o.write('</expressionList>')
		else:
			self.compileExpression()

		self.advance(skipNextAdvOnEat=True)

		# after compileExpression, next token has only two options:  ')' vs ','
		# ',' corresponds to (',' expression)*. eat(',') → compileExpression
		while self.tk.symbol() == ',':
			self.eat(',')
			self.compileExpression()
			self.advance(skipNextAdvOnEat=True)

		# ending case: ')' means we're done
		# TODO potential bug double evaluating ')' in subroutineName(exprList)
		# TODO maybe move this code to compileDo
		if self.tk.symbol() == ')':
			o.write('</expressionList>')
			self.eat(')')

	# we must have two versions of eat: one with advance and one without
	# this is for cases with ()? or ()* and we must advance first before
	# checking the token, e.g.
	# → varDec: 'var' type varName (',' varName)*';'
	# → let: 'let' varName ('[' expression ']')? '=' expression ';'
	def eat(self, expectedTokenValue: str):
		o = self.out
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

		# if not self.skipNextAdvanceOnEat and advanceFlag:
		if not self.skipNextAdvanceOnEat:
			# skip advance if flag is on from LL2 read-ahead situation
			# → see term: foo, foo[expr], foo.bar(exprList), bar(exprList)
			# turn off the "skip next eat()'s advance()" toggle if it's on
			self.advance()

		# reset the flag now that we've 'consumed' an eat command
		if self.skipNextAdvanceOnEat:
			self.skipNextAdvanceOnEat = False

		tokenType = self.tk.getTokenType()  # current token

		match tokenType:  # determine value of token
			case TokenType.KEYWORD:
				value = self.tk.keyWord()
				o.write(f'<keyword> {value} </keyword>\n')
			case TokenType.SYMBOL:
				value = self.tk.symbol()
				o.write(f'<symbol> {value} </symbol>\n')
			case TokenType.IDENTIFIER:
				value = self.tk.identifier()
				o.write(f'<identifier> {value} </identifier>\n')
			case TokenType.INT_CONST:
				value = self.tk.intVal()
				o.write(f'<integerConstant> {value} </integerConstant>\n')
			case TokenType.STRING_CONST:
				value = self.tk.stringVal()
				o.write(f'<stringConstant> {value} </stringConstant>\n')
			case _:  # impossible
				raise TypeError(f'token type invalid: not keyword, symbol, '
								  f'identifier, int constant, or string constant: {tokenType}')
		# assert expectedToken matches actual token
		# print(f'[eating → {value}]')
		assert expectedTokenValue == value, f'expected: {expectedTokenValue}, actual:{value}'

	# wrapper for self.tk.advance. sets skipNextAdvance flag for us
	def advance(self, skipNextAdvOnEat=False):
		self.tk.advance()
		self.skipNextAdvanceOnEat = skipNextAdvOnEat