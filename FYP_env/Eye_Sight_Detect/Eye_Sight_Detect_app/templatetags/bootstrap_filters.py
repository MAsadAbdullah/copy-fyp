from django import template

register = template.Library()


@register.filter(name='as_bootstrap')
def as_bootstrap(field):
    css_classes = 'form-control'
    if field.errors:
        css_classes += ' is-invalid'
    return field.as_widget(attrs={'class': css_classes})
