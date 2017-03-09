import style
class Dimensions(object):
    def __init__(self):
        self.content = Rect()
        self.padding = EdgeSizes()
        self.border = EdgeSizes()
        self.margin = EdgeSizes()

class Rect(object):
    def __init__(self, x = 0, y = 0, width = 0, height = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class EdgeSizes(object):
    def __init__(self, left=0, right=0, top=0, bottom=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

class LayoutBox(object):
    def __init__(self, box_type):
        self.dimensions = Dimensions()
        self.box_type = box_type
        self.children = []

    def get_inline_container(self):
        if isinstance(self.box_type, InlineNode) or isinstance(self.box_type, AnonymousBlock):
            return self
        else:
            if isinstance(self.children[-1], AnonymousBlock):
                return self.children[-1]
            else:
                self.children.append(LayoutBox(AnonymousBlock))
                return self.children[-1]


class BoxType:
    def __init__(self, style_node):
        self.style_node = style_node

class BlockNode(BoxType):
    def __init__(self, style_node):
        super(BlockNode, self).__init__(style_node)

class InlineNode(BoxType):
    def __init__(self, style_node):
        super(InlineNode, self).__init__(style_node)

class AnonymousBlock(BoxType):
    pass

def build_layout_tree(style_node):
    # create root box
    assert style_node.display() != 'none'
    if style_node.display() == 'block':
        box_type = BlockNode(style_node)
    elif style_node.display() == 'inline':
        box_type = InlineNode(style_node)
    root = LayoutBox(box_type)

    for child in style_node.children:
        if child.display() == 'block':
            root.children.append(build_layout_tree(child))
        elif child.display() == 'inline':
            root.get_inline_container().children.append(build_layout_tree(child))
        else:
            pass

    return root


