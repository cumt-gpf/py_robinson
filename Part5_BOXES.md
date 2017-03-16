Part 5: Boxes
====
本模块的输入是上节的style tree，输出是layout tree。layout tree中是一系列的二维矩形。

Box模型
------
Layout中的内容全部是关于Box的，一个Box是一个矩形区域，含有宽高，位置信息，浏览器在这块区域上展示图片，视频等。

一个Box可能也含有padding，border，margins等信息，这些信息决定了一个Box的周围状况。这里建了三个类。
```python
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

```

Block和Inline layout
----
在CSS中，`display`属性决定了element生成哪种类型的box，CSS有很多box类型，这里只讨论两种，block和inline。
对于一段HTML代码，举例如下：
```html
<container>
  <a></a>
  <b></b>
  <c></c>
  <d></d>
</container>
```
如果都是block类型，每个box将从上到下垂直排列在容器中。即CSS代码`a, b, c, d { display: block; }`将会展示如下：
![](./block.png)

如果都是inline类型，每个box从左到右水平排列在容器中，如果到达了容器的右边界，将另起一行。CSS代码`a, b, c, d { display: inline; }`
![](./inline.png)

每一个box必须要么只包含block类型的子节点，要么只是inline类型的子节点。如果一个element包含了混合类型的子节点，将插入一个anonymous box来把这两个类型分开。
例如CSS代码:
```html
a    { display: block; }
b, c { display: inline; }
d    { display: block; }
```
产生如下效果：
![](./anonymous.png)


