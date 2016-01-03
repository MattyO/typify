Basic Ussage
----
    class Record(typify.Model):                                                                                                                                                                    
        id = typify.IntegerMatcher()                                                                                                                                                               
        name = typify.StringMatcher())  

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
    class Record(typify.Model):
        zip = typify.IntegerMatcher(key='postal_code')
        
Parsing Attributes into complex type
---
    class Record(typify.Model):
        created_at = typify.StringMatcher(parse=lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'))
        
Converting complex type when writing to json
---
    class Record(typify.Model):
        created_at = typify.StringMatcher(convert=lambda x: x.isoformat(), default=lambda: datetime.datetime.now())
        
Wrapped attributes
---
    class Record(typify.Model):
        self = typify.StringMatcher(wrap='_links')
        embedded_link = typify.StringMatcher(wrap=['_links', 'embedded'])
        
Nested Objects
---

    class Author(typify.Model):                                                                                                                                                                    
        id = typify.IntegerMatcher()                                                                                                                                                               
        name = typify.StringMatcher()
        
    class Record(typify.Model): 
        author = typify.ObjectMatcher(Author)
        
Objects can be nested forever and ever
---
     class AuthorInfo(typify.Model):                                                                                                                                                                
        id = typify.IntegerMatcher()                                                                                                                                                               
        email = typify.StringMatcher()  
   
    class Author(typify.Model):                                                                                                                                                                    
        id = typify.IntegerMatcher()                                                                                                                                                               
        name = typify.StringMatcher()
        info  = typify.ObjectMatcher(AuthorInfo)
        
    class Record(typify.Model): 
        author = typify.ObjectMatcher(Author)
        
Collections of objects
---
    class Song(typify.Model):                                                                                                                                                                      
        id = typify.IntegerMatcher()                                                                                                                                                               
        name = typify.StringMatcher() 
    
    class Record(typify.Model): 
        songs = typify.CollectionMatcher(Song)
        
List of basic types
---
    class Record(typify.Model): 
        list_thing = typify.ListMatcher()
