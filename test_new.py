class Something(object):
    def __init__(self):
        print 'initing'

s = Something()
s2= type('foo', (Something,), {})
s2.__init__(s2);
