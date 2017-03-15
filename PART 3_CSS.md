PART 3: CSS
=====

CSS代码示例
----
下面是一段CSS代码：
```html
h1, h2, h3 { margin: auto; color: #cc0000; }
div.note { margin-bottom: 20px; padding: 10px; }
#answer { display: none; }
```
上面是一个CSS样式表，包含一系列规则，每一行是一个规则。先建一个样式表类。
```python
class Stylesheet:
    def __init__(self, rules):
        self.rules = rules
```
一条规则包含一个或者多个选择器，选择器之间用逗号隔开了，接着是一些放在大括号里的声明。
```python
class Rule(object):
    def __init__(self, selectors, declarations):
        self.selectors = selectors
        self.declarations = declarations
```
选择器分为[简单选择器](http://www.w3.org/TR/CSS2/selector.html#selector-syntax)和用一些连接符连接的复杂选择器，这里只支持简单选择器。
在本项目中，一个简单选择器可以包含一个tag名称，一个以#打头的id，以及任意多个以.打头的class名称。如果有以*打头的，则是一个全局选择器，可匹配任意tag。
为了方便添加更多的选择器，这里选择了继承的形式。
```python
class Selector:
    pass

class SimpleSelector(Selector):
    def __init__(self, tag_name, id, clazz):
        self.tag_name = tag_name
        self.id = id
        self.clazz = clazz
```
一个声明就是一个键值对，中间以`:`隔开，以一个分号结束，比如`margin: auto;`
```python
class Declaration(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
```
这个玩具引擎只支持少数的CSS value类型，value可能是一个Keyword，可能是一个Length，可能是一个Color。这里使用继承来实现，方便以后的添加。
```python
class Value:
    pass
class Keyword(Value):
    def __init__(self, keyword):
        self.keyword = keyword

class Length(Value):
    def __init__(self, length, unit):
        self.length = length
        self.unit = unit
class ColorValue(Value):
    def __init__(self, color):
        self.color = color

class color:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
```
匹配
-----
CSS有一个非常规律的语法，所以相比HTML比较好匹配。当遇到一个匹配错误的时候，直接跳过，执行下面的代码。这是很有好处的，因为这样样式表可以添加新的语法
并且在老旧的浏览器中一样可以翻译能识别的代码。

本文使用了一个非常简单的parser，和HTML parser实现的方式一样，这里简单的贴一些代码。
```python
#匹配一个SimpleSelector，如#id.class1.class2.class3
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
```
上面代码缺少错误检测，一个实用的parser将会跳过不合法的selector。

特征
-----
当有多个样式作用于一个selector的时候，引擎使用[特征](http://www.w3.org/TR/selectors/#specificity)来决定使用哪一个样式。如果一个演示表包含两条规则同时匹配了一个element，较高的特征可以覆盖较低的特征。

一个选择器的特征取决于它的组成部分，ID selector > class selector > tag selector

```python
def specificity(self):
        a = 0 if (self.id == None) else 1
        b = len(self.clazz)
        c = 0 if (self.tag_name == None) else 1
        return (a, b, c)
```
每一条规则的selectors被放在了一个list中，并且特征值最大的放在前面，这在以后的matching中非常重要，下一节会讲。
```python
def parse_rule(self):
        selectors = self.parse_selectors()
        declarations = self.parse_declarations()
        return Rule(selectors, declarations)

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
                raise SyntaxError("unexpect % in selector list" % self.next_char())
        sorted(selectors, reverse=True)
        return selectors
```
剩下的内容就非常简单了，可以之间在我的[代码库](https://github.com/cumt-gpf/py_robinson/tree/2b8352e616166acb5b2684b5de89d3566f354ed0)中看。

接下来会讲style模块，该模块将DOM node和CSS rule结合起来。
