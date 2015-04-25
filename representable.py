import inspect
import json
#class MatcherMeta(type):
#    def __new__(cls, name, parents, dtc):
#        pass
#        #attach new from_json method to clsss, di cls, and parents into it
class Matcher: 
    def __init__(self, *args, **kwargs):
        pass
class IntegerMatcher(Matcher):
    pass
class StringMatcher(Matcher):
    pass
class CollectionMatcher(Matcher):
    pass
class ObjectMatcher(Matcher):
    pass

class Model(object):
    @classmethod
    def from_json(cls, payload):
        attributes = {}
        json_object = json.loads(payload)
        matchers = filter(lambda key_value: isinstance(key_value[1], Matcher), inspect.getmembers(cls))
        inst = type(cls.__name__, (cls,), {'id': 2})

        for key, macther in matchers:
            pass
        inst.__init__();


