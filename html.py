import dom

class Parser:
    def __init__(self, pos, input):
        self.pos = pos
        self.input = input

    @staticmethod
    def isspace(c):
        return c.isspace()

    @staticmethod
    def istag_name(c):
        return c.isalnum()

    #Read the current char without consuming it
    def next_char(self):
        return self.input[self.pos]

    #Do the next char start with the given string?
    def starts_with(self, s):
        return s.startswith(self.next_char())

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
        self.consume_while(Parser.isspace)

    def parse_tag_name(self):
        self.consume_while(Parser.istag_name)

    def parse_node(self):
        if self.next_char() == '<':
            return self.parse_element()
        else:
            return self.parse_text()

    def parse_text(self):
        def test(c):
            return c != '<'
        data = self.consume_while(test)

        return dom.Text([], data)


    def parse_element(self):
        # Open tag
        assert self.consume_char() == '<'
        tag_name = self.parse_tag_name()
        attrs = self.parse_attributes()
        assert self.consume_char() == '>'

        # Contents
        children = self.parse_nodes()

        # Closing tag
        assert self.consume_char() == '<'
        assert self.consume_char() == '/'
        assert self.parse_tag_name() == tag_name
        assert self.consume_char() == '>'

        return dom.Element(tag_name, attrs, children)

    def parse_attr(self):
        name = self.parse_tag_name()
        assert self.consume_char() == '='
        value = self.parse_attr_value()
        return (name, value)

    def parse_attr_value(self):
        open_quote = self.consume_char()
        assert open_quote == '"' or open_quote == '&#39;'
        def test(c):
            return c != open_quote
        value = self.consume_while(test)
        assert self.consume_char() == open_quote
        return value

    def parse_attributes(self):
        attributes = {}
        while True:
            self.consume_whilespace()
            if self.next_char() == '>':
                break
            (name, value) = self.parse_attr()
            attributes[name] = value

        return attributes

    def parse_nodes(self):
        nodes = []
        while True:
            self.consume_whilespace()
            if self.eof() or self.starts_with('</'):
                break
            nodes.append(self.parse_node())

        return nodes

    def parse(self):
        nodes = self.parse_nodes()

        if len(nodes) == 1:
            return nodes.pop(0)
        else:
            return dom.Element('html', {}, nodes)



if __name__ == '__main__':
    str = '''
        <html>
    <body>
        <h1>Title</h1>
        <div id="main" class="test">
            <p>Hello <em>world</em>!</p>
        </div>
    </body>
    </html>
    '''
    parse = Parser(0, str)
    print(parse.parse())






