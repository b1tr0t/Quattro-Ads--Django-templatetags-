from django import template
from quattro.quattro import Quattro

register = template.Library()

class QuattroAdTag(template.Node):
    """
    Write out a Quattro ad for this request.
    """
    def __init__(self, publisher_id, site_id):
        self.publisher_id = template.Variable(publisher_id)
        self.site_id = template.Variable(site_id)
    
    def render(self, context):
        if 'request' not in context:
            return "<!-- Request is required in the context for the QuattroAdTag -->"
        if not self.publisher_id or not self.site_id:
            return "<!-- Publisher id and site_id are required for QuattroAdTag -->"
        context['request'].has_quattro = True
        q = Quattro(context['request'], pid=self.publisher_id.resolve(context), sid=self.site_id.resolve(context), test=0, fail_silently=True)
        return q.renderAd()

@register.tag
def quattro(parser, token):
    try:
        tag_name, publisher_id, site_id = token.split_contents()
    except ValueError:
        publisher_id = ''
        site_id = ''

    return QuattroAdTag(publisher_id, site_id)
