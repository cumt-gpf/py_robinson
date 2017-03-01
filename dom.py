
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
        super(Text, self).__init__(children)
        self.data = data

    def __str__(self):
        return self.data


class Element(Node):
    def __init__(self, name, attrs, children):
        super(Element, self).__init__(children)
        elementdata = ElementData(name, attrs)
        self.elementdata = elementdata

    def __str__(self):
        return self.elementdata.tag_name

class ElementData(object):
    def __init__(self, tag_name, attributes):
        self.tag_name = tag_name
        self.attributes = attributes

    def __str__(self):
        return self.tag_name



