class Dimensions(object):
    def __init__(self, content_Rect, padding_EdgeSizes, border_EdgeSizes, margin_EdgeSizes):
        self.content = content_Rect
        self.padding = padding_EdgeSizes
        self.border = border_EdgeSizes
        self.margin = margin_EdgeSizes

class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class EdgeSizes(object):
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
