from django import template

register = template.Library()
stop_words = [
    'плохое_слово1',
    'плохое_слово2',
    'плохое_слово3',
]

@register.filter(name='censor')

def censor(value):

    for sw in stop_words:
        value = value.lower().replace(sw.lower(), '...')
    return value

@register.filter(name='preview')

def preview(value):
    if len(value) > 50:
        return value[:51] + '...'
    else:
        return value

if __name__ == '__main__':
    print(censor("""Слово1 слово2 плохое_слово1 Плохое_слово2
плохое_слово3 плохое_слово4 слово3"""))