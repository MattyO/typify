import inspect
import json
import copy

class Matcher(object):

    def __init__(self, *args, **kwargs):
        if 'key' in kwargs:
            self.key = kwargs['key']

        self.wrap = kwargs.get('wrap', None)

        if 'parse' in kwargs:
            self.parse = kwargs['parse']

        if 'convert' in kwargs:
            self.convert = kwargs['convert']

    def parse(self, value):
        return value

    def convert(self, value):
        return value

class IntegerMatcher(Matcher):
    pass

class StringMatcher(Matcher):
    pass

class ListMatcher(Matcher):
    pass

class CollectionMatcher(Matcher):

    def __init__(self, matcher_cls, **kwargs):
        self.matcher_model = matcher_cls
        super(CollectionMatcher, self).__init__(**kwargs)

    def parse(self, value):
        return [ self.matcher_model.from_dict(inner_dict) for inner_dict in value ]

    def convert(self, value):
        return [ a_model.to_dict() for a_model in value ]

class ObjectMatcher(Matcher):

    def __init__(self, matcher_cls, **kwargs):
        self.matcher_model = matcher_cls
        super(ObjectMatcher, self).__init__(**kwargs)

    def parse(self, value):
        return self.matcher_model.from_dict(value)

    def convert(self, value):
        return value.to_dict()


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

class Model(object):

    @classmethod
    def matchers(cls):
        return filter(lambda key_value: isinstance(key_value[1], Matcher), inspect.getmembers(cls))

    @classmethod
    def from_dict(cls, a_dict):
        inst = cls.__new__(cls)
        attributes = {}
        matchers = cls.matchers()

        for attribute, matcher in matchers:
            key = getattr(matcher, 'key', attribute)
            value = find_in(key, a_dict, matcher.wrap)
            setattr(inst, attribute, matcher.parse(value))

        inst.__init__()
        return inst

    @classmethod
    def from_json(cls, payload):
        json_object = json.loads(payload)
        return cls.from_dict(json_object)

    def to_dict(self):
        returned_dict = {}
        for attribute, matcher in self.matchers():
            key = getattr(matcher, 'key', attribute)
            value = matcher.convert(getattr(self, attribute))
            set_or_create(key, value, returned_dict, matcher.wrap)

        return returned_dict

    def to_json(self):
        return json.dumps(self.to_dict())
