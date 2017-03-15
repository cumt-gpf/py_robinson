PART 2: HTML
======
在这篇文章中讲如何匹配[HTML 源码](http://www.whatwg.org/specs/web-apps/current-work/multipage/introduction.html#a-quick-introduction-to-html)来生成一棵DOM结点组成的树。
匹配是一个很有意思的话题，读者可以看看有关编译器的课程和书籍（龙书第二版），或者参考一些你熟悉的编程语言的[parser generator](https://en.wikipedia.org/wiki/Comparison_of_parser_generators)的实现。

HTML有自己的parser算法，这个算法不同于其他编程语言，HTML的Parser不拒绝无效的输入。它有特定的错误处理机制，所以web浏览器可以展示所有的web页面，
即使那些页面没有按照HTML的语法来。

一段简单的HTML源码
------
本文不实现标准的HTML parser，只是实现一个小的HTML语法的子集。实现的parser能够匹配如下的源码：
```html
<html>
    <body>
        <h1>Title</h1>
        <div id="main" class="test">
            <p>Hello <em>world</em>!</p>
        </div>
    </body>
</html>
```

支持如下语法：
- 平衡的tags: `<p>....</p>`
- 带有双引号标识的属性：`id="main"`
- Text结点：`<em>world</em>`

不支持如下语法：
- 注释
- 自闭合的tag`<br/>`
- 错误处理
- 字符编码检测
- ...

感兴趣的读者可以自行实现上述语法。

示例代码
------
这个parser包含输入的字符串，一个表明下一个要处理的字符的位置的变量。
```python
class Parser:
    def __init__(self, pos, input):
        self.pos = pos
        self.input = input
```
我们可以实现一些简单的方法来得到下一个要处理的字符。
```python
    #返回当前要处理的字符，但是不消耗它
    def next_char(self):
        return self.input[self.pos]
        

    #给定的字符串是接下来的字符串的开始吗
    def starts_with(self, s):
        return self.input[self.pos:].startswith(s)
        

    #返回是否结束
    def eof(self):
        return self.pos >= len(self.input)
   
    #消耗当前字符串，位置+1，并返回
    def consume_char(self):
        s = self.next_char()
        self.pos += 1
        return s
```
有时候我们想消耗一连串字符，比如匹配出一个tag名称，方法`consume_while`将一个判断方法作为参数，这个判断方法需要一个char类型的参数，返回一个bool值。
```python
    def consume_while(self, test):
        result = ''
        while not self.eof() and test(self.next_char()):
            result += self.consume_char()
        return result
```
可以使用`consume_whitespace`方法来消耗掉空白字符。
```python
    def consume_whilespace(self):
        def test(c):
            return c.isspace()
        self.consume_while(test)
```
这里除了上面那种写法，也可以使用`lambda`表达式的写法，显得高级一点。lambda表达式作为一种匿名函数，还是有很多应用场景的，具体可参考《Python学习手册（第四版）》。
```python
   def consume_whilespace(self):
        test = lambda c: c.isspace()
        self.consume_while(test)
```
当需要匹配一个字母和数字组成的字符串时，比如tag名称，属性名称时，可以这么写：
```python
    def parse_tag_name(self):
        test = lambda c: c.isalnum()
        return self.consume_while(test)
```
现在我们可以开始写HTML的parser了，首先看第一个字符，如果是以`<`打头的则是一个element，否则是一个text。
```python
    def parse_node(self):
        if self.next_char() == '<':
            return self.parse_element()
        else:
            return self.parse_text()

    def parse_text(self):
        test = lambda c: c != '<'
        data = self.consume_while(test)
        return dom.Text([], data)
```
接下来要parse一个element，稍稍复杂，包括开始和闭合的tag，一些属性，中间也有一些子节点。
```python
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
```
匹配属性的时候稍微简单一些，毕竟我们只实现了一些简单的语法，只需要重复的寻找tag name，=，以及用双引号包裹的值，直到遇到`>`结束。
```python
    def parse_attr(self):
        name = self.parse_tag_name()
        assert self.consume_char() == '='
        value = self.parse_attr_value()
        return (name, value)
        

    def parse_attr_value(self):
        open_quote = self.consume_char()
        assert open_quote == '"' or open_quote == '&#39;'
        test = lambda c: c != open_quote
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
```
匹配子节点的时候只需要重复调用`parse_node`方法即可，直到遇到了闭合tag`</`
```python
    def parse_nodes(self):
        nodes = []
        while True:
            self.consume_whilespace()
            if self.eof() or self.starts_with('</'):
                break
            nodes.append(self.parse_node())

        return nodes
```
最后我们把上面的代码组合起来，匹配HTML源码到一个DOM树。本方法返回一个根节点。
```python
    def parse(self):
        nodes = self.parse_nodes()

        #如果有返回该结点，否则新建一个结点
        if len(nodes) == 1:
            return nodes.pop(0)
        else:
            return dom.Element('html', {}, nodes)
```
这一节主要写了如何写一个简单的HTML parser。下一节会讲CSS的数据结构以及匹配。
