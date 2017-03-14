import layout
import css
import html
import style
import png

class DisplayCommand:
    pass

class SolidColor(DisplayCommand):
    def __init__(self, color, rect):
        self.color = color
        self.rect = rect

displayList = []

#First draw box's background, then we draw its borders and content on top of the background

def build_display_list(layout_root):
    list = []
    render_layout_box(list, layout_root)
    return list

def render_layout_box(displaylist, layout_box):
    render_background(displaylist, layout_box)
    render_borders(displaylist, layout_box)

    for child in layout_box.children:
        render_layout_box(displaylist, child)

def render_background(displaylist, layout_box):
    color = get_color(layout_box, 'background')
    displaylist.append(SolidColor(color, layout_box.dimensions.border_box()))

def get_color(layout_box, name):
    if isinstance(layout_box, layout.BlockNode) or isinstance(layout_box, layout.InlineNode):
        color = layout_box.style_node.value(name)
        if isinstance(color, css.ColorValue):
            return color.color
        else:
            return None

    return None

def render_borders(dispaylist, layout_box):
    color = get_color(layout_box, 'border-color')
    if color == None:
        return

    d = layout_box.dimensions
    border_box = d.border_box()
    #Left border
    dispaylist.append(SolidColor(color, layout.Rect(border_box.x, border_box.y, d.border.left, border_box.height)))

    #Right border
    dispaylist.append(SolidColor(color, layout.Rect(border_box.x + border_box.width - d.border.right,
                                                    border_box.y, d.border.right, border_box.height)))

    #Top border
    dispaylist.append(SolidColor(color, layout.Rect(border_box.x, border_box.y, border_box.width, d.border.top)))

    #Bottom border
    dispaylist.append(SolidColor(color, layout.Rect(border_box.x, border_box.y + border_box.height - d.border.bottom,
                                                    border_box.width, d.border.bottom)))

#build display list, turn it into pixels
class Canvas:
    def __init__(self, width, height):
        white = css.color(255, 255, 255, 255)
        self.pixels = [white] * (width * height)
        self.width = width
        self.height = height
    def paint_item(self, item):
        if isinstance(item, SolidColor):
            x0 = clamp(item.rect.x, 0.0, self.width)
            y0 = clamp(item.rect.y, 0.0, self.height)
            x1 = clamp(item.rect.x + item.rect.width, 0.0, self.width)
            y1 = clamp(item.rect.y + item.rect.height, 0.0, self.height)

            for y in (y0, y1):
                for x in (x0, x1):
                    self.pixels[y * self.width + x] = item.color


def clamp(a, lower, upper):
    if a > lower:
        b = a
    else:
        b = lower

    if b > upper:
        return upper
    else:
        return b


def paint(layout_root, bounds):
    display_list = build_display_list(layout_root)
    canvas = Canvas(bounds.width, bounds.height)

    for item in display_list:
        canvas.paint_item(item)

    return canvas

if __name__ == '__main__':
    html_test = '''
        <div class="a">
            <div class="b">
                <div class="c">
                    <div class="d">
                        <div class="e">
                            <div class="f">
                                <div class="g">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    css_test = '''
         * { display: block; padding: 12px; }
        .a { background: #ff0000; }
        .b { background: #ffa500; }
        .c { background: #ffff00; }
        .d { background: #008000; }
        .e { background: #0000ff; }
        .f { background: #4b0082; }
        .g { background: #800080; }
    '''
    root = html.Parser(0, html_test).parse()
    stylesheet = css.Parser(0, css_test).parse()
    stylednode = style.style_tree(root, stylesheet)

    viewport = layout.Dimensions()
    viewport.content.width = 800.0
    viewport.content.height = 600.0

    layoutroot = layout.layout_tree(stylednode, viewport)
    canvas = paint(layoutroot, viewport.content)

    png.from_array(canvas.pixels, 'L').save("small_smiley.png")










