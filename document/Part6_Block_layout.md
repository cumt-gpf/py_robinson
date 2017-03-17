PART 6: BLOCK LAYOUT
=====
继续讲上节的layout模块，这次加入让box有布局的能力。

遍历Layout tree
-----
从`layout`方法开始，以一个layout box作为参数，计算它的大小规模，首先实现部分代码：
```python
def layout(self, containing_block):
     if isinstance(self.box_type, BlockNode):
          self.layout_block(containing_block)
```
？？？？一个block的布局取决于它包含的子节点的大小，对于一般的block box这取决于该box的父节点，对于根节点，是浏览器的窗口。

你肯定还记得，一个block的宽度取决于父节点的宽度，高度取决于子节点。那就意味着，要自上而下遍历树，这样子节点就能知道父节点的宽度了，还需要自下而上遍历树，这样父节点的高度也就知道了。
```python
def layout_block(self, containing_block):
        self.calculate_block_width(containing_block)
        self.calculate_block_position(containing_block)
        self.layout_block_chilren()
        self.calculate_block_height()
```
