import datetime
import lib as typify
import pprint


class Song(typify.Model):
    id = typify.IntegerMatcher()
    name = typify.StringMatcher()

class AuthorInfo(typify.Model):
    id = typify.IntegerMatcher()
    email = typify.StringMatcher()

class Author(typify.Model):
    id = typify.IntegerMatcher()
    name = typify.StringMatcher()
    info  = typify.ObjectMatcher(AuthorInfo)

class Record(typify.Model):
    id = typify.IntegerMatcher()
    name = typify.StringMatcher()
    merged_stuff = typify.StringMatcher(merge=lambda doc: str(doc['id']) + ':' + doc['name'] )
    zip = typify.IntegerMatcher(key='postal_code')
    created_at = typify.StringMatcher(parse=lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'), convert=lambda x: x.isoformat(), default=lambda: datetime.datetime.now())
    songs = typify.CollectionMatcher(Song)
    author = typify.ObjectMatcher(Author)
    self = typify.StringMatcher(wrap='_links')
    next = typify.StringMatcher(wrap='_links')
    embedded_link = typify.StringMatcher(wrap=['_links', 'embedded'])
    list_thing = typify.ListMatcher()


record=Record.from_json("{\"id\":1,\"name\":\"testname\",\"postal_code\":44024,\"created_at\":\"2015-04-24T21:51:50.691473\",\"songs\":[{\"id\":1,\"name\":\"songname\"}],\"author\":{ \"id\": 1, \"name\": \"test author\", \"info\":{\"id\":1, \"email\":\"test@example.com\"}}, \"_links\":{\"self\":\"testselflink\",\"next\":\"testnextlink\",\"embedded\":{\"embedded_link\":\"testembeddedlink\"}}, \"list_thing\":[1,2,3,4]}")

printer = pprint.PrettyPrinter()

#print 'start of the real test'
#print Record().to_json()
#record = Record()
#record = Record.from_json("{\"id\":1}")
print record.to_json()

#printer.pprint(record.to_dict())
#print record.to_json()
