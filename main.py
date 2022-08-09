# @author kiwi
# @date 2022.08.09
#
# class CompilationEngine {
# 	compileStatements() {}
# 	compileIfStatement() {}
# 	compileWhiteStatement() {}
# 	...
# 	compileTerm() {}
# }
#
# jack grammar
#
# statement: 		ifStatement | whiteStatement | letStatement
# statements:		statement*
# ifStatement:	    if (expression) {statements}
# whiteStatement:	while (expression) {statements}
# letStatement:	    let varName = expression;
# expression:   	term (op term)?
# term:			    varName | constant
# varName:		    a string not beginning with a digit
# constant:		    a decimal number
# op:				+, -, =, >, <


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
