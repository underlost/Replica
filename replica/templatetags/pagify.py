from django.template import Library, Node, Variable
from django.core.paginator import Paginator
import settings

register = Library()

class PagifyNode(Node):
    def __init__(self, items, page_size, varname):
    	self.items = Variable(items)
    	self.page_size = int(page_size)
    	self.varname = varname

    def render(self, context):
    	pages = Paginator(self.items.resolve(context), self.page_size)
    	request = context['request']
    	page_num = int(request.GET.get('page', 1))

    	context[self.varname] = pages.page(page_num)
    	return ''

@register.tag
def pagify(parser, token):
    """
    Usage:

    {% pagify items by page_size as varname %}
    """

    bits = token.contents.split()
    if len(bits) != 6:
    	raise TemplateSyntaxError, 'pagify tag takes exactly 5 arguments'
    if bits[2] != 'by':
    	raise TemplateSyntaxError, 'second argument to pagify tag must be "by"'
    if bits[4] != 'as':
    	raise TemplateSyntaxError, 'fourth argument to pagify tag must be "as"'
    return PagifyNode(bits[1], bits[3], bits[5])
    
    
    
    #{% load pagify %}
    
    #{% pagify items by 20 as page %}
    #{% for item in page %}
    #    {{ item }}
    #{% endfor %}