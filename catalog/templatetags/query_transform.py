# this custom tag receives a new query parameter that will be added
# to the already existing query parameter. This way, the tag saves existing
# query parameter, adds a new one, and returns the result.

from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):  # query_transform is our tag, **kwargs contain new query params that we want to add to existing
    updated = request.GET.copy()  # copy all existing query params
    for k, v in kwargs.items():  # loop over new params
        if v is not None:
            updated[k] = v  # add new params if they are
        else:
            updated.pop(k, 0)
    return updated.urlencode()  # convert dict into query parameters and return
