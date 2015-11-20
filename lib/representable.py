import inspect
import json

import matchers
import helpers

class MetaModel(type):
    def __new__(meta, name, bases, namespace):
        matchers = MetaModel.find_matchers(namespace)
        for key, matcher in matchers:
            namespace[key] = matcher.default()
        namespace['_meta'] = matchers

        return super(MetaModel, meta).__new__(meta, name, bases, namespace)

    @classmethod
    def find_matchers(cls, n):
        return [(key, value) for key, value in n.items() if isinstance(value, matchers.Matcher)]

class Model(object):

    __metaclass__ = MetaModel

    @classmethod
    def matchers(cls):
        return cls._meta

    @classmethod
    def from_dict(cls, a_dict):
        inst = cls.__new__(cls)
        attributes = {}
        matchers = cls.matchers()

        for attribute, matcher in matchers:
            key = getattr(matcher, 'key', attribute)
            value = helpers.find_in(key, a_dict, matcher.wrap, matcher.default())
            if not isinstance(value, cls):
                if hasattr(matcher, 'merge') and callable(matcher.merge):
                    value = matcher.merge(a_dict)
                else:
                    value = matcher.parse(value)
            setattr(inst, attribute, value)

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
            helpers.set_or_create(key, value, returned_dict, matcher.wrap)

        return returned_dict

    def to_json(self):
        return json.dumps(self.to_dict())
