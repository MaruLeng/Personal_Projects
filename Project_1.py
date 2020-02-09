# Author: Yifeng Leng
# PSU id: ybl5226
# Purpose of this file: A lexer and parser for SQL programming language

INT, FLOAT, ID, COMMA, KEYWORD, OPERATOR, EOI, INVALID = 1,2,3,4,5,6,7,8

# Receive an input and determine which token type it is.
# We will use this function in class Parser.
def typeToString(tp):
    if (tp == INT):
        return "Int"
    elif (tp == FLOAT):
        return "Float"
    elif (tp == "ID"):
        return "ID"
    elif (tp == "COMMA"):
        return "Comma"
    elif (tp == "KEYWORD"):
        return "Keyword"
    elif (tp == "OPERATOR"):
        return "Operator"
    elif (tp == "EOI"):
        return "EOI"
    else:
        return "Invalid"

# This is a class to define tokens
# An object of Token class has two fields: its type and its value
# For example, Token(ID, "x1"); Token(KEYWORD, "SELECT")
class Token:
    "A class for representing Tokens"

    def __init__(self, tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal

    # Get methods
    # These 2 methods will return token's type and value
    # So, you can use them as 2 variables
    def getTokenType(self):
        return self.type
    def getTokenValue(self):
        return self.val

    def __repr__(self):
        if (self.type in [INT, FLOAT, ID, KEYWORD]):
            return self.val
        elif (self.type == COMMA):
            return ","
        elif (self.type == OPERATOR):
            if (self.val == "="):
                return "="
            elif (self.val == "<"):
                return "<"
            elif (self.val == ">"):
                return ">"
        elif (self.type == EOI):
            return ""
        else:
            return "invalid"

#These are CharSets
#In Lexer class, a function called consumeChars will use these sets as inputs
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
PUNCUATION = ",=<>"
DOT = "."

# A class defines what kind of a string should be
class Lexer:
    # The object should be a string
    def __init__(self,s):
        # for example, an input string "statement"
        # The local variables stmt == "statement", index == 0~8, stmt has a method called nextChar
        # to find next character.
        self.stmt = s
        self.index = 0
        self.nextChar()
    
    # ch is the character on the index
    # when we get the char, the index will be added by 1
    def nextChar(self):
        self.ch = self.stmt[self.index] 
        self.index = self.index + 1

    # for example, if we have a string "ab12,"
    # when the consumeChars is called, the input will be LETTERS, DIGITS, or both
    # r = a
    # use self.nextChar() to get b, now ch==b
    # as long as the ch is in LETTERS and DIGITS
    # r = r+self.ch; which is r = a + b
    # r == ab
    # and call self.nextChar() again to get 1
    # After the while loop, r==ab12, and because "," is not in LETTERS and DIGITS, we stop
    # and return r, which is ab12
    def consumeChars (self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r
    
    # We have defined fields. Now we should check which type it should be
    # Use nextToken method
    def nextToken(self):
        # Don't stop until the whole string is scanned. 
        # so we use a while loop

        while True:
            # if we have a string starts with a letter
            if self.ch.isalpha():
                # You must understand what is consumeChar(Charset)
                # id = a the string until the character doesn't belong to LETTERS or DIGITS
                # We have 2 senario, an id or keyword?
                id = self.consumeChars(LETTERS+DIGITS)
                if (id=="SELECT" or id=="FROM" or id=="WHERE" or id=="AND"):
                    return Token(KEYWORD, id)
                else:
                    return Token(ID, id)
            
            # if we have a string starts with a digit
            elif self.ch.isdigit():
                # num = a the string until the character doesn't belong to DIGITS
                num = self.consumeChars(DIGITS)
                
                # Be aware that self.ch is the num's next character
                # For example, the imput == 12345.
                # then num == 12345, self.ch == .
                # Because consumeChars calls nextChar in the last iteration of while loop
                # And if you look nextChar method, you will see self.ch is the next character
                
                # !!!!Notice!!!! If you called consumerChars(Charset) and self.ch; self.ch will be the next character
                # For example, if input is "abcd5", s = self.consumeChars(LETTERS) and followed by x = self.ch
                # Then s == "abcd", self.ch == 5
                
                # If self.ch is not a ".", then the whole string is an integer
                
                # If we have a string starts with an integer but followed by a non-digit(except ".")
                # Then this string is invalid
                followingChar = self.ch
                if ((followingChar.isdigit() == False) and (followingChar != ".") and (followingChar != ' ')):
                    return Token(INVALID, num)

                
                if self.ch != ".":
                    return Token(INT, num)
                # else, there is a "." in num, we make add num with dot
                # for example, input = "123.45"
                # after the code below, num == "123."
                num += self.ch
                # then we call nextChar() again. Notice now the string starts from 4
                self.nextChar()
                # if 4 is a digit
                if self.ch.isdigit(): 
                    # self.consumeChars(DIGITS) will return 45
                    # Then add num and 45
                    # num == "123." + "45" == "123.45"
                    num += self.consumeChars(DIGITS)
                    return Token(FLOAT, num)
                    # if we have some other characters, the input is neither int or float
                else: 
                    return Token(INVALID, num)
            # Skip white spaces
            elif self.ch == ' ':
                self.nextChar()
            # If we find a chunck of punctuations
            elif (self.ch == ',' or self.ch == '=' or self.ch == '<' or self.ch == '>'):
                punc = self.consumeChars(PUNCUATION)
                if punc == ",":
                    return Token(COMMA, punc)
                elif punc == "=":
                    return Token(OPERATOR, punc)
                elif punc == "<":
                    return Token(OPERATOR, punc)
                elif punc == ">":
                    return Token(OPERATOR, punc)
                else:
                    return Token(INVALID, punc)
            # $ is the ending sign, after next condition statement, while loop should quit
            elif self.ch == "$":
                return Token(EOI, "")
            # return invalid if none of the above condtion statements is satisfied
            else:
                self.nextChar()
                return Token(INVALID, self.ch)

import sys
class Parser:
    def __init__(self, s):
        # s is the input string, we add a $ at the end of s, a signal that the string in scanned over.
        # token is the string s$ next token. There is a nextToken function above.
        self.lexer = Lexer(s+"$")
        self.token = self.lexer.nextToken()

    #Use run() to check if a string of command is valid in SQL
    def run(self):
        # Call query() method
        self.query()
    
    #Check if a token matched token types
    def match (self, tp):
        val = self.token.getTokenValue()
        if (self.token.getTokenType() == tp):
            self.token = self.lexer.nextToken()
        else: self.error(tp)
        return val

    #Return error if a token is invalid
    def error(self, tp):
        print "Syntax error: expecting: " + typeToString(tp) \
              + "; saw: " + typeToString(self.token.getTokenType())
        sys.exit(1)

    #<Query> -> SELECT <IDList> FROM <IDList> [WHERE <CondList>]
    #as the sequence above, we call query() keywordStmt() IdList() keywordStmt() and IdList()
    #Then if there is a WHERE, we can check CondList() again
    #because it is [], we can only call [WHERE <CondList>] one time, that's why I have a counter here
    #And we have match(EOI) to stop
    def query(self):
        counter = 1
        print "<Query>"
        self.keywordStmt()
        self.IdList()
        self.keywordStmt()
        self.IdList()
        if self.token.getTokenType() == KEYWORD and counter==1:
            if self.token.getTokenValue() == "WHERE":
                counter += 1
                self.keywordStmt()
                self.condList()
            else:
                print "INVALID Keyword"
        self.match(EOI)
        print "</Query>"
    
    def condList(self):
        print "\t<CondList>"
        self.cond()
        
        while self.token.getTokenType() == KEYWORD:
            if self.token.getTokenValue() == "AND":
                print "\t\t<Keyword>AND</Keyword>"
                self.token = self.lexer.nextToken()
                self.cond()
            else:
                print "INVALID Keyword"

        print "\t</CondList>"
    
    def cond(self):
        print "\t\t<Cond>"
        self.ids()
        self.operator()
        self.Term()
        print "\t\t</Cond>"

    def operator(self):
        op = self.match(OPERATOR)
        print "\t\t\t<Operator>" + op + "</Operator>"
    
    def Term(self):
        print "\t\t\t<Term>"
        if self.token.getTokenType() == ID:
            print "\t\t\t\t<Id>" + self.token.getTokenValue() \
                  + "</Id>"
            print "\t\t\t</Term>"
        elif self.token.getTokenType() == INT:
            print "\t\t\t\t<Int>" + self.token.getTokenValue() + "</Int>"
            print "\t\t\t</Term>"
        elif self.token.getTokenType() == FLOAT:
            print "\t\t\t\t<Float>" + self.token.getTokenValue() + "</Float>"
            print "\t\t\t</Term>"
        else:
            print "Syntax error: expecting an ID, an int, or a float" \
                  + "; saw:" \
                  + typeToString(self.token.getTokenType())
            sys.exit(1)
        self.token = self.lexer.nextToken()
        

    def keywordStmt(self):
        key = self.match(KEYWORD)
        print "\t<Keyword>" + key + "</Keyword>"

    def IdList(self):
        print "\t<IdList>"
        self.ids()
        while self.token.getTokenType() == COMMA:
            print "\t\t<Comma>,</Comma>"
            self.token = self.lexer.nextToken()
            self.ids()
        print "\t</IdList>"

    def ids(self):
        val = self.match(ID)
        print "\t\t<Id>" + val + "</Id>"



            

# print "Testing the lexer: test 1"
# lex = Lexer ("x1 $")
# tk = lex.nextToken()
# while (tk.getTokenType() != EOI):
#     print tk
#     tk = lex.nextToken()
# print

# print "Testing the lexer: test 2"
# lex = Lexer ("x > 1; y = 2.3; z < x $")
# tk = lex.nextToken()
# while (tk.getTokenType() != EOI):
#     print tk
#     tk = lex.nextToken()
# print

# print "Testing the lexer: test 3"
# lex = Lexer ("x = 1; y < 2; z := x $")
# tk = lex.nextToken()
# while (tk.getTokenType() != EOI):
#     print tk
#     tk = lex.nextToken()
# print                




# print "Testing the parser: test 1"
# parser = Parser ("SELECT C1,C2,C3 FROM T1 WHERE C1=45 AND C2<3.5 AND C3=45.4")
# parser.run()

# print "Testing the parser: test 2"
# parser = Parser ("SELECT C1,C2 FROM T1 WHERE C1=5.23")
# parser.run()

# print "Testing the parser: test 3"
# parser = Parser ("SELECT C1C2,C2C1 FROM T11T WHERE C1=>5.23")
# parser.run()

# print "Testing the parser: test 4"
# parser = Parser ("SELECT C1,C2 FROM FROM T1 WHERE C1=5.23")
# parser.run()

