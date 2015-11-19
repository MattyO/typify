Basic Ussage
----
    class Record(representable.Model):                                                                                                                                                                    
        id = representable.IntegerMatcher()                                                                                                                                                               
        name = representable.StringMatcher())  

    record_json = "{\"id\":1,\"name\":\"testname\"}
    
    a_record = Record.from_json(record_json)
    print record.id
    print record.name
    print a_record.to_json()

This is library is to help facilitate creating objects from common text based representation formates(json, yaml, and python dics).  The following response will be used for a common example.  

    {
       "id":1,
       "name":"Gold Start Ablum",
       "postal_code":44024,
       "created_at":"2015-04-24T21:51:50.691473",
       "songs":[
          {
             "id":1,
             "name":"songname"
          }
       ],
       "author":{
          "id":1,
          "name":"test author",
          "info":{
             "id":1,
             "email":"test@example.com"
          }
       },
       "_links":{
          "self":"testselflink",
          "next":"testnextlink",
          "embedded":{
             "embedded_link":"testembeddedlink"
          }
       },
       "list_thing":[
          1,
          2,
          3,
          4
      ]
    }
    
    
Supported Formats
---
* from_json
* from_yaml
* from_dict

* to_json
* to_yaml
* to_dicttw

    
    
Renaming Attributes
---
    class Record(representable.Model):
        zip = representable.IntegerMatcher(key='postal_code')
        
Parsing Attributes into complex type
---
    class Record(representable.Model):
        created_at = representable.StringMatcher(parse=lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'))
        
Converting complex type when writing to json
---
    class Record(representable.Model):
        created_at = representable.StringMatcher(convert=lambda x: x.isoformat(), default=lambda: datetime.datetime.now())
        
Wrapped attributes
---
    class Record(representable.Model):
        self = representable.StringMatcher(wrap='_links')
        embedded_link = representable.StringMatcher(wrap=['_links', 'embedded'])
        
Nested Objects
---

    class Author(representable.Model):                                                                                                                                                                    
        id = representable.IntegerMatcher()                                                                                                                                                               
        name = representable.StringMatcher()
        
    class Record(representable.Model): 
        author = representable.ObjectMatcher(Author)
        
Objects can be nested forever and ever
---
     class AuthorInfo(representable.Model):                                                                                                                                                                
        id = representable.IntegerMatcher()                                                                                                                                                               
        email = representable.StringMatcher()  
   
    class Author(representable.Model):                                                                                                                                                                    
        id = representable.IntegerMatcher()                                                                                                                                                               
        name = representable.StringMatcher()
        info  = representable.ObjectMatcher(AuthorInfo)
        
    class Record(representable.Model): 
        author = representable.ObjectMatcher(Author)
        
Collections of objects
---
    class Song(representable.Model):                                                                                                                                                                      
        id = representable.IntegerMatcher()                                                                                                                                                               
        name = representable.StringMatcher() 
    
    class Record(representable.Model): 
        songs = representable.CollectionMatcher(Song)
        
List of basic types
---
    class Record(representable.Model): 
        list_thing = representable.ListMatcher()