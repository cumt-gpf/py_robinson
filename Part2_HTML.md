###PART 2: HTML
在这篇文章中讲如何匹配[HTML 源码](http://www.whatwg.org/specs/web-apps/current-work/multipage/introduction.html#a-quick-introduction-to-html)来生成一棵DOM结点组成的树。
匹配是一个很有意思的话题，读者可以看看有关编译器的课程和书籍（龙书第二版），或者参考一些你熟悉的编程语言的[parser generator](https://en.wikipedia.org/wiki/Comparison_of_parser_generators)的实现。

HTML有自己的parser算法，这个算法不同于其他编程语言，HTML的Parser不拒绝无效的输入。它有特定的错误处理机制，所以web浏览器可以展示所有的web页面，
即使那些页面没有按照HTML的语法来。

###一段简单的HTML源码
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

###示例代码
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
有时候我们想消耗一串字符，方法`consume_while`通过一个


