import html
import css
import style
class Dimensions(object):
    def __init__(self):
        self.content = Rect()
        self.padding = EdgeSizes()
        self.border = EdgeSizes()
        self.margin = EdgeSizes()
    def padding_box(self):
        return self.content.expanded_by(self.padding)
    def border_box(self):
        return self.padding_box().expanded_by(self.border)
    def margin_box(self):
        return self.border_box().expanded_by(self.margin)

class Rect(object):
    def __init__(self, x = 0, y = 0, width = 0, height = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def expanded_by(self, edge):
        return Rect(self.x - edge.left, self.y - edge.top, self.width + edge.left + edge.right,
                    self.height + edge.top + edge.bottom)

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

    def get_style_node(self):
        if isinstance(self.box_type, AnonymousBlock):
            assert 1 > 2
        else:
            return self.box_type.style_node

    def get_inline_container(self):
        if isinstance(self.box_type, InlineNode) or isinstance(self.box_type, AnonymousBlock):
            return self
        else:
            if isinstance(self.children[-1], AnonymousBlock):
                return self.children[-1]
            else:
                self.children.append(LayoutBox(AnonymousBlock))
                return self.children[-1]
    def layout(self, containing_block):
        if isinstance(self.box_type, BlockNode):
            self.layout_block(containing_block)

    def layout_block(self, containing_block):
        pass

    def calculate_block_width(self, containing_block):
        style = self.get_style_node();
        width = style.value('width')
        auto = css.Keyword('auto')
        if width == None:
            width = auto
        zero = css.Length(0.0, 'Px')
        margin_left = style.lookup('margin-left', 'margin', zero)
        margin_right = style.lookup('margin-right', 'margin', zero)

        border_left = style.lookup('border-left-width', 'border-width', zero)
        border_right = style.lookup('border-right-width', 'border-width', zero)

        padding_left = style.lookup('padding-left', 'padding', zero)
        padding_right = style.lookup('padding-right', 'padding', zero)

        total = 0.0
        for a in [width, margin_left, margin_right, border_left, border_right, padding_left, padding_right]:
            total += a.to_px()

        if width != auto and total > containing_block.width:
            if margin_left == auto:
                margin_left = css.Length(0.0, 'Px')
            if margin_right == auto:
                margin_right = css.Length(0.0, 'Px')

        underflow = containing_block.content.width - total

        width_auto = (width == auto)
        margin_left_auto = (margin_left == auto)
        margin_right_auto = (margin_right == auto)

        if not width_auto and not margin_left_auto and not margin_right_auto:
            margin_right = css.Length(margin_right.to_px() + underflow, 'Px')
        elif not width_auto and not margin_left_auto and margin_right_auto:
            margin_right = css.Length(underflow, 'Px')
        elif not width_auto and margin_left_auto and not margin_right_auto:
            margin_left = css.Length(underflow, 'Px')
        if width_auto:
            if margin_left:
                margin_left = css.Length(0.0, 'Px')
            if margin_right:
                margin_right = css.Length(0.0, 'Px')

            if underflow >= 0.0:
                width = css.Length(0.0, 'Px')
            else:
                width = css.Length(0.0, 'Px')
                margin_right = css.Length(margin_right.to_px() + underflow, 'Px')

        if not width_auto and margin_left_auto and margin_right_auto:
            margin_left = css.Length(underflow / 2, 'Px')
            margin_right = css.Length(underflow / 2, 'Px')

    def calculate_block_position(self, containing_block):
        style = self.get_style_node()
        d = self.dimensions

        zero = css.Length(0.0, 'Px')

        d.margin.top = style.lookup('margin-top', 'margin', zero).to_px()
        d.margin.bottom = style.lookup('margin-bottom', 'margin', zero).to_px()

        d.border.top = style.lookup('border-top-width', 'border-width', zero).to_px()
        d.border.bottom = style.lookup('border-bottom-width', 'border-width', zero).to_px()

        d.padding.top = style.lookup('padding-top', 'padding', zero).to_px()
        d.padding.bottom = style.lookup('padding-bottom', 'padding', zero).to_px()

        d.content.x = containing_block.content.x + d.margin.left + d.border.left + d.padding.left

        d.content.y = containing_block.content.height + containing_block.content.y + d.margin.top + d.border.top + d.padding.top

    def layout_block_chilren(self):
        d = self.dimensions
        for child in self.children:
            child.layout(d)
            d.content.height = d.content.height + child.dimensions.margin_box().height

    def calculate_block_height(self):
        if self.get_style_node().value('height') != None:
            self.dimensions.content.height = self.get_style_node().value('height')








class BoxType:
    def __init__(self, style_node):
        self.style_node = style_node

class BlockNode(BoxType):
    def __init__(self, style_node):
        BoxType.__init__(self, style_node)

class InlineNode(BoxType):
    def __init__(self, style_node):
        BoxType.__init__(self, style_node)

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

if __name__ == '__main__':
    html_test = '''
        <html>
            <body>
                <h1>Title</h1>
                <div id="main" class="test">
                    <p>Hello <em>world</em>!</p>
                </div>
            </body>
        </html>
    '''
    css_test = '''
         h1, h2, h3 { margin: auto; color: #cc0000; }
         div.test { margin-bottom: 20px; padding: 10px; }
         #answer { display: none; }
    '''
    root = html.Parser(0, html_test).parse()
    stylesheet = css.Parser(0, css_test).parse()
    stylednode = style.style_tree(root, stylesheet)
    layoutroot = build_layout_tree(stylednode)
    print('hello')


