import dom
import css
import html

class StyleNode(object):
    def __init__(self, node, specified_values, children):
        self.node = node
        self.specified_values = specified_values
        self.children = children

def matches(elementdata, selector):
    if isinstance(selector, css.SimpleSelector):
        return matches_simple_selector(elementdata, selector)

def matches_simple_selector(elementdata, selector):
    if selector.tag_name != elementdata.tag_name:
        return False

    if selector.id != elementdata.id():
        return False

    elem_clazzes = elementdata.clazzes()
    if len(set(elem_clazzes) & set(selector.clazz)) == 0:
        return False

    return True

def match_rule(elementdata, rule):
    for selector in rule.selectors:
        if(matches(elementdata, selector)):
            return (selector.specifity(), rule)
    return None

def matching_rules(elementdata, stylesheet):
    matchrules = []
    for rule in stylesheet.rules:
        result = match_rule(elementdata, rule)
        if result != None:
            matchrules.append(result)

    return matchrules

def specified_values(elementdata, stylesheet):
    values = {}
    rules = matching_rules(elementdata, stylesheet)

    def MyFn(s):
        return s[0]
    sorted(rules, key=MyFn)
    for (specifity, rule) in rules:
        for declaration in rule.declarations:
            values[declaration.name] = declaration.value

    return values

def style_tree(root, stylesheet):
    spvalues = ''
    children = []
    if isinstance(root, dom.Element):
        spvalues = specified_values(root.elementdata, stylesheet)
    elif isinstance(root, dom.Text):
        spvalues = {}

    for child in root.children :
        children.append(style_tree(child, stylesheet))

    return StyleNode(root, spvalues, children)

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
    stylednode = style_tree(root, stylesheet)
    print('hello')












