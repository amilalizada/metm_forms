from django.template.defaulttags import register

@register.filter
def get_item(err_list, key):
    for error in err_list:
        # print(error)
        if key in error:
            return error.get(key,'')
    return ''

@register.simple_tag
def all_opt(value):
    print('aaaaaaaaaaaaaaa',value)
    options_list = value.split(",")
    print(options_list)
    return options_list