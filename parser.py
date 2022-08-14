# no one knows why it's called CompilationEngine
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