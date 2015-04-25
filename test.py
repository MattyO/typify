import datetime
import representable


class Song(representable.Model):
    id = representable.IntegerMatcher()
    name = representable.StringMatcher()

class Author(representable.Model):
    id = representable.IntegerMatcher()
    name = representable.StringMatcher()

class Record(representable.Model):
    id = representable.IntegerMatcher()
    name = representable.StringMatcher()
    zip = representable.IntegerMatcher(key='postal_code')
    created_at = representable.StringMatcher(parse=lambda x: datetime.stringftime(x, ''), convert=lambda x: x.isoformat())
    songs = representable.CollectionMatcher(Song)
    author = representable.ObjectMatcher(Author)
    self = representable.StringMatcher(wrap='_links')
    next = representable.StringMatcher(wrap='_links')
    embedded_link= representable.StringMatcher(wrap=['_links', 'embeded'])

    def __init__(self):
        print 'initing record class'
        print self.id


record=Record.from_json("{\"id'\":1,\"name'\":\"testname\",\"postal_code\":44024,\"created_at\":\"2015-04-24T21:51:50.691473\",\"songs\":[{\"id\":1,\"name\":\"songname\"}],\"_links\":{\"self\":\"testselflink\",\"next\":\"testnextlink\",\"embedded\":{\"embedded_link\":\"testembeddedlink\"}}}")
