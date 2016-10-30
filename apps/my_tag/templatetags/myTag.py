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


@register.filter("truncate_chars")
def truncate_chars(value, max_length):
        if len(value) > max_length:
                truncd_val = value[:max_length]
                if not len(value) == max_length+1 and value[max_length+1] != " ":
                        truncd_val = truncd_val[:truncd_val.rfind(" ")]
                return truncd_val + "..."
        return value
