from django import template

register = template.Library()


@register.filter
def model_type(instance):
    return type(instance).__name__


@register.simple_tag(takes_context=True)
def display_you(context, user):
    if user == context['user']:
        return 'vous'
    return user.username