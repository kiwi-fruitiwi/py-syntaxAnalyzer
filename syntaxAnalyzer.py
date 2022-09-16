"""
@author kiwi
@date 2022.08.14

project contract
  implement syntaxAnalyzer in python
    parses .jack files → xml from nand2tetris/projects/10
    compare with TextComparer in nand2tetris/tools
  see chapter.10 of book

  1. build JackTokenizer ← unit 4.8
  2. build CompilationEngine, basic expressionless → complete with expressions
    xml file needs to be wrapped in <tokens> tag
    string constants have no double quotes
    remember html special characters [< > " &] → [&lt; &gt; &quot; &amp]

  currentToken varName has 5 branches:
    foo
    foo[expression]
    foo.bar(expList)
    Foo.bar(expList) ← what's the difference? static method vs member?
    bar(expList)

  this is the only case where the jack grammar is LL(2)
    save current token
    look ahead to next one


  ⊼² finish tokenizer, 📹→L4.8, 12:57 is compilation engine
    test using *T.xml files after reading *.jack
    ExpressionLessSquare after basic compilationEngine done
    Square when expressions done

→ a bunch of characters with no space in the middle does not necessarily mean that you have only one token, e.g. getx() has three: getx and two symbols
    look up getx in keywords list. not there, so must be identifier
    next is straightforward symbol table lookup

  consider implementations in library string functions and regex
    check lexical elements diagram in this order. nc = next character
        check if nc is in the symbols list
        integerConstant → is nc [0-9]? take rest of [0-9]
        surrounded by "" → stringConstant. next "[all char ex. " \n]"
        else nc is alphabetical:
            check keywords list for next token. should be all alphabetic
            identifier → [0-9a-zA-Z_]+

"""

# take care of multiple files in a directory vs one target file

from parser import CompilationEngine

from tokenizer import JackTokenizer
from tokenizer import TokenType
from tokenizer import Keyword

from pathlib import Path
import os

root: str = 'C:/Dropbox/code/nand2tetris/kiwi/nand2tetris/projects/'
filename: str = root + '10/ArrayTest/Main.jack'

tk = JackTokenizer(filename)
tk.advance()

# main loop
while tk.hasMoreTokens():
    tokenClassification = tk.getTokenType()
    print(f'<{tokenClassification}>')

    # determine the value of the token
    #   keyWord, symbol, identifier, intVal, stringVal
    value = 'placeholder'

    print(f'{value}')
    print(f'</{tokenClassification}\n>')
    tk.advance()


for line in tk.getJackCommands():
    print(f'{line}')
