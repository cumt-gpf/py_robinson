Part 4: Style
====
本模块以DOM结点和CSS规则作为输入，将它们匹配起来，对每一个DOM结点指定正确的CSS value。

格式树
----
style模块的输出可以称为格式树，树上的每一个结点包含一个DOM结点，和CSS value。
```python
class StyleNode(object):
    def __init__(self, node, specified_values, children):
        self.node = node
        self.specified_values = specified_values
        self.children = children
```
浏览器经常以一棵树作为输入，输出另一棵相关的树。例如，Gecko的layout代码以DOM tree作为输入，产生一个frame tree，可以用来构建view tree。
我们的流程大概如下图![](./pipeline.png)
