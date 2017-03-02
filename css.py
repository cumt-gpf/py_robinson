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
    def __init__(self, tag_name, id, clazz):
        self.tag_name = tag_name
        self.id = id
        self.clazz = clazz

    def specificity(self):
        a = 0 if (self.id == None) else 1
        b = len(self.clazz)
        c = 0 if (self.tag_name == None) else 1
        return (a, b, c)



class Declaration(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class color(object):
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

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
            elif '.' == self.next_char():
                self.consume_char()
                selector.clazz.append(self.parse_identifier())
            elif '*' == self.next_char():
                self.consume_char()
            elif self.next_char().isalnum():
                selector.tag_name = self.parse_identifier()
            else:
                break

        return selector

    def parse_identifier(self):
        def test(c):
            return c.isalnum() or c == '_' or c == '-'
        return self.consume_while(test)

    def parse_rule(self):
        selectors = self.parse_selectors()
        declarations = self.parse_declarations()
        return Rule(selectors, declarations)

    def parse_rules(self):
        rules = []
        while True:
            self.consume_whilespace()
            if self.eof():
                break
            else:
                rules.append(self.parse_rule())

        return rules

    def parse_selectors(self):
        selectors = []
        while True:
            selectors.append(self.parse_simple_selector())
            self.consume_whilespace()
            if self.next_char() == ',':
                self.consume_char()
                self.consume_whilespace()
            elif self.next_char() == '{':
                break
            else:
                print("unexpect % in selector list" % self.next_char())
        sorted(selectors, reverse=True)
        return selectors

    def parse_declarations(self):
        assert self.consume_char() == '{'
        declarations = []
        while True:
            self.consume_whilespace()
            if self.next_char() == '}':
                self.consume_char()
                break
            else:
                declarations.append(self.parse_declaration())
        return declarations



    def parse_declaration(self):
        name = self.parse_identifier()
        self.consume_whilespace()
        assert self.consume_char() == ':'
        self.consume_whilespace()
        value = self.parse_value()
        self.consume_whilespace()
        assert self.consume_char() == ';'

        return (name, value)


    def parse_value(self):
        if self.next_char() == '#':
            return self.parse_color()
        elif self.next_char().isdigit():
            return self.parse_length()
        else:
            return self.parse_identifier()



    def parse_color(self):
        assert self.consume_char() == '#'
        r = self.parse_hex_pair()
        g = self.parse_hex_pair()
        b = self.parse_hex_pair()
        a = 255
        return (r, g, b, a)

    def parse_hex_pair(self):
        s = self.input[self.pos : self.pos + 2]
        self.pos += 2
        return int(s, 16)

    def parse_float(self):
        def test(c):
            return c.isdigit()
        s = self.consume_while(test)
        return s

    def parse_unit(self):
        s = self.parse_identifier()
        if s == 'px':
            return s
        else:
            print ('unrecognized unit')


    def parse_length(self):
        return (self.parse_float(), self.parse_unit())

    def parse(self):
        return Stylesheet(self.parse_rules())


if __name__ == '__main__':
    test = '''
         h1, h2, h3 { margin: auto; color: #cc0000; }
         div.test { margin-bottom: 20px; padding: 10px; }
         #answer { display: none; }
    '''
    paser = Parser(0, test)
    haha = paser.parse_rules()
    print('hello')









