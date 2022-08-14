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

parser = JackTokenizer(filename)

for line in parser.getJackCommands():
    print(f'{line}')
