import dom
import css
import html

class StyleNode(object):
    def __init__(self, node, specified_values, children):
        self.node = node
        self.specified_values = specified_values
        self.children = children

    def value(self, name):
        if self.specified_values.has_key(name):
            return self.specified_values[name]
        else:
            return None

    def display(self):
        if self.specified_values.has_key('display'):
            value = self.specified_values('display')
            if value == 'block' or value == 'none':
                return value
            else:
                return 'inline'
        else:
            return 'inline'

    def lookup(self, name, fallback_name, default):
        if self.value(name) != None:
            return self.value(name)
        elif self.value(fallback_name) != None:
            return self.value(fallback_name)
        else:
            return default

def matches(elementdata, selector):
    if isinstance(selector, css.SimpleSelector):
        return matches_simple_selector(elementdata, selector)

def matches_simple_selector(elementdata, selector):
    result = False
    if selector.tag_name != None and selector.tag_name == elementdata.tag_name:
        result = True

    if selector.id != None and selector.id == elementdata.id():
        result = True

    elem_clazzes = elementdata.clazzes()
    for clazz in elem_clazzes:
        if selector.clazz.__contains__(clazz):
            result = True

    return result

def match_rule(elementdata, rule):
    for selector in rule.selectors:
        if(matches(elementdata, selector)):
            return (selector.specificity(), rule)
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
            values[declaration[0]] = declaration[1]

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
    stylednode = style_tree(root, stylesheet)
    print('hello')












