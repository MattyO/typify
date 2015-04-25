import inspect
import json

class Matcher:

    def __init__(self, *args, **kwargs):
        if 'key' in kwargs:
            self.key = kwargs['key']

        self.wrap = kwargs.get('wrap', None)

    def parse(self, value):
        return value

class IntegerMatcher(Matcher):
    def parse(self, value):
        return int(value)

class StringMatcher(Matcher):
    pass


class CollectionMatcher(Matcher):
    pass

    #def __init__(self, matcher_cls, **kwargs):
    #    self.matcher_model = matcher_cls
    #    super(CollectionMatcher, self).__init__(**kwargs)

class ObjectMatcher(Matcher):
    pass

#    def __init__(self, matcher_cls, **kwargs):
#        self.matcher_model = matcher_cls
#        super(ObjectMatcher, self).__init__(**kwargs)
#

def find_in(key, the_object, wrapped_in):
    if not wrapped_in:
        return the_object[key]

    if isinstance(wrapped_in, basestring):
        wrapped_in = [wrapped_in]

    return find_in(key, the_object[wrapped_in.pop(0)], wrapped_in)


class Model(object):
    @classmethod
    def from_json(cls, payload):
        attributes = {}
        json_object = json.loads(payload)
        matchers = filter(lambda key_value: isinstance(key_value[1], Matcher), inspect.getmembers(cls))

        for key, matcher in matchers:
            key = getattr(matcher, 'key', key)
            value = find_in(key, json_object, matcher.wrap)
            attributes[key] = matcher.parse(value)

        print attributes

        inst = type(cls.__name__, (cls,), attributes)
        super(cls, inst).__init__(inst)

        return inst
