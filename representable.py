import inspect
import json

class Matcher(object):

    def __init__(self, *args, **kwargs):
        if 'key' in kwargs:
            self.key = kwargs['key']

        self.wrap = kwargs.get('wrap', None)

        if 'parse' in kwargs:
            self.parse = kwargs['parse']

    def parse(self, value):
        return value

class IntegerMatcher(Matcher):
    def parse(self, value):
        return int(value)

class StringMatcher(Matcher):
    pass

class CollectionMatcher(Matcher):

    def __init__(self, matcher_cls, **kwargs):
        self.matcher_model = matcher_cls
        super(CollectionMatcher, self).__init__(**kwargs)

    def parse(self, value):
        return [ self.matcher_model.from_dict(inner_dict) for inner_dict in value ]

class ObjectMatcher(Matcher):

    def __init__(self, matcher_cls, **kwargs):
        self.matcher_model = matcher_cls
        super(ObjectMatcher, self).__init__(**kwargs)

    def parse(self, value):
        return self.matcher_model.from_dict(value)


def find_in(key, the_object, wrapped_in):
    if not wrapped_in:
        return the_object[key]

    if isinstance(wrapped_in, basestring):
        wrapped_in = [wrapped_in]

    return find_in(key, the_object[wrapped_in.pop(0)], wrapped_in)


class Model(object):
    @classmethod
    def from_dict(cls, a_dict):
        inst = cls.__new__(cls)
        attributes = {}
        matchers = filter(lambda key_value: isinstance(key_value[1], Matcher), inspect.getmembers(cls))

        for key, matcher in matchers:
            key = getattr(matcher, 'key', key)
            value = find_in(key, a_dict, matcher.wrap)
            setattr(inst, key, matcher.parse(value))

        inst.__init__()
        return inst

    @classmethod
    def from_json(cls, payload):
        json_object = json.loads(payload)
        return cls.from_dict(json_object)
