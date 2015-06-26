class Matcher(object):

    def __init__(self, *args, **kwargs):
        if 'key' in kwargs:
            self.key = kwargs['key']

        self.wrap = kwargs.get('wrap', None)

        if 'parse' in kwargs:
            self.parse = kwargs['parse']

        if 'convert' in kwargs:
            self.convert = kwargs['convert']

        self._default = kwargs.get('default', lambda: None)

    def parse(self, value):
        return value

    def convert(self, value):
        return value

    def default(self):
        return self._default()

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

    def default(self):
        return []

class ObjectMatcher(Matcher):

    def __init__(self, matcher_cls, **kwargs):
        self.matcher_model = matcher_cls
        super(ObjectMatcher, self).__init__(**kwargs)

    def parse(self, value):
        return self.matcher_model.from_dict(value)

    def convert(self, value):
        return value.to_dict()

    def default(self):
        #print 'object matcher default'
        m = self.matcher_model()
        #print m
        return m
        #return self.matcher_model()
