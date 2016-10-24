from django import template

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
