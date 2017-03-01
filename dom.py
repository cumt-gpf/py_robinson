
class Node(object):
    def __init__(self, children):
        self.children = children


class Text(Node):
    def __init__(self, children, data):
        super(Text, self).__init__(children)
        self.data = data


class Element(Node):
    def __init__(self, name, attrs, children):
        super(Element, self).__init__(children)
        elementdata = ElementData(name, attrs)
        self.elementdata = elementdata

class ElementData(object):
    def __init__(self, tag_name, attributes):
        self.tag_name = tag_name
        self.attributes = attributes



