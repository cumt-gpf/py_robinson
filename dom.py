
class Node(object):
    def __init__(self, children):
        self.children = children
    def print_test(self):
        print(self)
        if len(self.children) == 0:
            return
        else:
            for node in self.children:
                node.print_test()


class Text(Node):
    def __init__(self, children, data):
        Node.__init__(self, children)
        self.data = data

class Element(Node):
    def __init__(self, name, attrs, children):
        Node.__init__(self, children)
        self.elementdata = ElementData(name, attrs)

class ElementData(object):
    def __init__(self, tag_name, attributes):
        self.tag_name = tag_name
        self.attributes = attributes

    def id(self):
        if self.attributes.has_key('id'):
            return self.attributes['id']
        else:
            return None

    def clazzes(self):
        if self.attributes.has_key('class'):
            return self.attributes['class'].split(' ')
        else:
            return []


