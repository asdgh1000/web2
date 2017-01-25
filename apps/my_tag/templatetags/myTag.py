from django import template
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter

register = template.Library()


class NavTagItem(template.Node):
    def __init__(self, nav_path, nav_displaytext):
        self.path = nav_path.strip('"')
        self.text = nav_displaytext.strip('"')

    def render(self, context):
        cur_path = context['request'].path
        # print cur_path,self.path
        if self.path == '/':
            current = cur_path == '/'
        else:
            current = cur_path.startswith(self.path)
        cur_id = ''
        if current:
            cur_id = ' class="active" '
        return '<li %s><a href="%s">%s</a></li>' % (cur_id, self.path, self.text)


@register.tag
def navtagitem(parser, token):
        try:
            tag_name, nav_path, nav_text = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError(
                "%r tag requires exactly two arguments: path and text" %
                token.split_contents[0])
        return NavTagItem(nav_path, nav_text)


@register.filter("truncate_chars")
def truncate_chars(value, max_length):
        truncd_val = value
        if len(value) > max_length:
                truncd_val = value[:max_length]
                return truncd_val + " ..."
        return truncd_val


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


@register.filter
def markdown(value):
    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    return markdown(value)
