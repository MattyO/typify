import copy

def find_in(key, the_object, wrapped_in, default=None):

    if not wrapped_in:
        return the_object.get(key, default)

    wrapped_in = copy.copy(wrapped_in)

    if isinstance(wrapped_in, basestring): #helps out the recursivness of the function
        wrapped_in = [wrapped_in]

    temp_wrapped_in = wrapped_in.pop(0)
    if not the_object.has_key(temp_wrapped_in):
        return default

    return find_in(key, the_object[temp_wrapped_in], wrapped_in)

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

