import datetime
import representable
import pprint


class Song(representable.Model):
    id = representable.IntegerMatcher()
    name = representable.StringMatcher()

class AuthorInfo(representable.Model):
    id = representable.IntegerMatcher()
    email = representable.StringMatcher()

class Author(representable.Model):
    id = representable.IntegerMatcher()
    name = representable.StringMatcher()
    info  = representable.ObjectMatcher(AuthorInfo)

class Record(representable.Model):
    id = representable.IntegerMatcher()
    name = representable.StringMatcher()
    zip = representable.IntegerMatcher(key='postal_code')
    created_at = representable.StringMatcher(parse=lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'), convert=lambda x: x.isoformat())
    songs = representable.CollectionMatcher(Song)
    author = representable.ObjectMatcher(Author)
    self = representable.StringMatcher(wrap='_links')
    next = representable.StringMatcher(wrap='_links')
    embedded_link = representable.StringMatcher(wrap=['_links', 'embedded'])
    list_thing = representable.ListMatcher()


record=Record.from_json("{\"id\":1,\"name\":\"testname\",\"postal_code\":44024,\"created_at\":\"2015-04-24T21:51:50.691473\",\"songs\":[{\"id\":1,\"name\":\"songname\"}],\"author\":{ \"id\": 1, \"name\": \"test author\", \"info\":{\"id\":1, \"email\":\"test@example.com\"}}, \"_links\":{\"self\":\"testselflink\",\"next\":\"testnextlink\",\"embedded\":{\"embedded_link\":\"testembeddedlink\"}}, \"list_thing\":[1,2,3,4]}")

printer = pprint.PrettyPrinter()
print record.list_thing

#print record
#print record.__dict__
#print record.author.__dict__
#print record.author.info.__dict__
#print record.songs[0].__dict__
#printer.pprint(record.to_dict())
print record.to_json()
