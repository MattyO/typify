import copy

def find_in(key, the_object, wrapped_in):

    if not wrapped_in:
        return the_object[key]

    wrapped_in = copy.copy(wrapped_in)

    if isinstance(wrapped_in, basestring):
        wrapped_in = [wrapped_in]

    return find_in(key, the_object[wrapped_in.pop(0)], wrapped_in)

def set_or_create(key, value, the_object, wrapped_in):

    if not wrapped_in:
        the_object[key] = value
        return

    wrapped_in = copy.copy(wrapped_in)

    if isinstance(wrapped_in, basestring):
        wrapped_in = [wrapped_in]

    new_key = wrapped_in.pop(0)
    if new_key not in the_object:
        the_object[new_key] = {}

    return set_or_create(key, value, the_object[new_key], wrapped_in)

