###PART1: GETTING STARTED 
###我们在做些什么？
浏览器引擎是web浏览器的一部分，它从Internet中抓取页面并且翻译为我们可读，可听，可看的形式。像Blink，Webkit，Trident都是
浏览器引擎。相反，浏览器自己的UI被称为chrome，有些浏览器UI不一样，但是有一样的浏览器引擎。

一个浏览器引擎包含很多模块，有HTTP客户端，HTML paser，CSS paser，JavaScript引擎等。

####为什么要写一个玩具浏览器引擎？
首先，能实际使用的浏览器代码量十分庞大，很复杂。属于大型复杂软件。我们编写的玩具虽然不能使用，但是可以学习它们是怎么组成的，怎么
工作的。所以，如果你想知道你天天打交道的浏览器是怎么工作的话，就实现一个部分功能的浏览器吧。这里我们实现一个简单的HTML和CSS的paser，
并且结合两者，以图片的形式展现结果。

原文是用Rust写的，我为了熟悉Python，这里选择用Python写。

####第一步 DOM
首先会展示[DOM](http://dom.spec.whatwg.org/)的数据结构。DOM是由结点组成的树，一个结点含有0个或者多个子结点。
```python
class Node:
    def __init__(self, children):
        self.children = children
```
结点也是有不同[类型](https://dom.spec.whatwg.org/#dom-node-nodetype)的，但是这里我们只考虑两种，一种是Element，一种是Text的。
这里我们可以继承Node来实现。
```python
class Text(Node):
    def __init__(self, children, data):
        Node.__init__(self, children)
        self.data = data

class Element(Node):
    def __init__(self, name, attrs, children):
        Node.__init__(self, children)
        self.elementdata = ElementData(name, attrs)
```
一个Element中包含一个tag名称和一系列的属性，这些属性可以表示成键值对的形式。这里我们写到一个ElementData类中。
```python
class ElementData(object):
    def __init__(self, tag_name, attributes):
        self.tag_name = tag_name
        self.attributes = attributes
```
一个完整的DOM实现包含了很多数据和方法，但是对于我们的玩具，这些已经够了。下一节会写一个HTML paser来把HTML代码
转化为以树组织的DOM结点。

