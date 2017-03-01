class Stylesheet(object):
    def __init__(self, rules):
        self.rules = rules

class Rule(object):
    def __init__(self, selectors, declarations):
        self.selectors = selectors
        self.declarations = declarations

class Selector(object):
    pass

class SimpleSelector(Selector):
    def __init__(self, tag_name, id, s_class):
        self.tag_name = tag_name
        self.id = id
        self.s_class = s_class

class Declaration(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Parser:
    def __init__(self, pos, input):
        self.pos = pos
        self.input = input

    #Read the current char without consuming it
    def next_char(self):
        return self.input[self.pos]

    #Do the next char start with the given string?
    def starts_with(self, s):
        return self.input[self.pos:].startswith(s)

    #Return true if all input is consumed
    def eof(self):
        return self.pos >= len(self.input)

    #Return the current character, and advance self.pos to the next char
    def consume_char(self):
        s = self.next_char()
        self.pos += 1
        return s

    #Consume characters until test returns false
    def consume_while(self, test):
        result = ''
        while not self.eof() and test(self.next_char()):
            result += self.consume_char()
        return result

    def consume_whilespace(self):
        def test(c):
            return c.isspace()
        self.consume_while(test)

    def parse_simple_selector(self):
        selector = SimpleSelector(None, None, [])
        while not self.eof():
            if '#' == self.next_char():
                self.consume_char()
                selector.id = self.parse_identifier()
            elif '.' == self.next_char() or ' ' == self.next_char():
                self.consume_char()
                selector.s_class.append(self.parse_identifier())
            elif '*' == self.next_char():
                self.consume_char()
            elif self.next_char().isalnum():
                selector.tag_name = self.parse_identifier()
            else:
                break

        return selector

    def parse_identifier(self):
        pass
















