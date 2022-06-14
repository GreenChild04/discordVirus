##########################
# Run
##########################

class Parser:
    def __init__(self, text):
        self.text = text

    def run(self):
        tokens, error = Lexer(self.text).run()
        if error:
            print(error.asString())
        inter = Interpreter(tokens).run()

        return inter[0][0], inter[1]


##########################
# Interpreter
##########################
class Interpreter:
    def __init__(self, tokenList):
        self.tokenList = tokenList

    def getTokenType(self, token):
        return token.asType()

    def getTokenValue(self, token):
        return token.asValue()

    def checkToken(self, token, tokenList):
        for i in tokenList:
            if self.getTokenType(i) == token:
                return True

        return False

    def run(self):
        colonSides = []
        finalCmdDir = []
        syntax = []

        if self.checkToken(TT_COL, self.tokenList):
            colonSides = self.colonParser()
            finalCmdDir = self.dotParser(colonSides[0])

            if self.checkToken(TT_DASH, colonSides[1]):
                syntax = self.findSeparateInput(colonSides)

            else:
                print(InvalidSyntaxError('Expected \'-\' after \':\'').asString())

        else:
            finalCmdDir = self.dotParser(self.tokenList)
            syntax = None

        return finalCmdDir, syntax

    def colonParser(self):
        activeTokens = self.tokenSplit(TT_COL, self.tokenList)
        return activeTokens

    def findSeparateInput(self, colonSides):
        typeMemory = None
        output = []

        for i in colonSides[1]:

            if self.getTokenType(i) in [TT_FUN, TT_FLOAT, TT_INT, TT_STR] and typeMemory == TT_DASH:
                output.append(self.getTokenValue(i))

            typeMemory = self.getTokenType(i)

        return output

    def dotParser(self, tokenList):
        activeTokens = self.tokenSplit(TT_DOT, tokenList)
        output = []

        for i in activeTokens:
            for a in i:
                output.append(self.getTokenValue(a))

        return output

    def tokenSplit(self, token, tokenList):
        result = []
        current_set = []
        for item in tokenList:
            if self.getTokenType(item) is token:
                result.append(current_set)
                current_set = []
            else:
                current_set.append(item)
        result.append(current_set)
        return result


##########################
# Lexer
##########################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.currentChar = None
        self.pos = -1

    def run(self):
        self.advance()
        tokenList, error = self.makeTokens()
        return tokenList, error

    def advance(self):
        self.pos += 1
        self.currentChar = self.text[self.pos] if self.pos < len(self.text) else None

    def makeTokens(self):
        tokens = []

        while self.currentChar is not None:
            if self.currentChar in ' <>\t':
                self.advance()
            elif self.currentChar in DIGITS:
                tokens.append(self.makeNumbers())
            elif self.currentChar in CHARACTERS:
                tokens.append(self.makeCharacters())
            elif self.currentChar == '"':
                tokens.append(self.makeText())
            elif self.currentChar == ':':
                tokens.append(Token(TT_COL))
                self.advance()
            elif self.currentChar == '-':
                tokens.append(Token(TT_DASH))
                self.advance()
            elif self.currentChar == '.':
                tokens.append(Token(TT_DOT))
                self.advance()
            else:
                char = self.currentChar
                self.advance()
                return [], IllegalCharError(f"'{char}'")

        return tokens, None

    def makeNumbers(self):
        numStr = ''
        dot_count = 0

        while self.currentChar is not None and self.currentChar in DIGITS + '.':
            if self.currentChar == '.':
                if dot_count == 1: break
                dot_count += 1
                numStr += '.'
            else:
                numStr += self.currentChar
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(numStr))
        else:
            return Token(TT_FLOAT, float(numStr))

    def makeCharacters(self):
        charStr = ''

        while self.currentChar is not None and self.currentChar in CHARACTERS:
            charStr += self.currentChar
            self.advance()
        return Token(TT_FUN, charStr)

    def makeText(self):
        charText = ''

        self.advance()

        while self.currentChar is not None and self.currentChar != '"':
            charText += self.currentChar
            self.advance()
        self.advance()
        return Token(TT_STR, charText)


##########################
# Tokens
##########################

TT_COL = 'COL'
TT_DASH = 'DASH'
TT_DOT = 'DOT'
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_FUN = 'FUN'
TT_STR = "STR"


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def asString(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

    def asValue(self):
        return self.value

    def asType(self):
        return self.type


##########################
# CONSTANTS
##########################

DIGITS = '0123456789'

CHARACTERS = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDGHJKLZXCVBNM_,/\\;'


##########################
# ERRORS
##########################

class Error:
    def __init__(self, errorName, details):
        self.errorName = errorName
        self.details = details
        self.asString()

    def asString(self):
        return f'(Error) {self.errorName}: {self.details}'


class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Unexpected Character', details)


class InvalidSyntaxError(Error):
    def __init__(self, details):
        super().__init__('Invalid Syntax', details)
