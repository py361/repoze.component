import unittest

class TestRegistry(unittest.TestCase):
    def _getTargetClass(self):
        from repoze.component import Registry
        return Registry
        
    def _makeOne(self, dict=None, **kw):
        return self._getTargetClass()(dict, **kw)

    def test_ctor(self):
        d = {'a':1}
        registry = self._makeOne(d, b=2)
        self.assertEqual(registry['a'], 1)
        self.assertEqual(registry['b'], 2)

    def test_cmp_againstreg(self):
        registry1 = self._makeOne()
        registry2 = self._makeOne()
        self.assertEqual(registry1.__cmp__(registry2), 0)
        self.assertEqual(registry2.__cmp__(registry1), 0)
        registry1['a'] = 1
        self.assertEqual(registry1.__cmp__(registry2), 1)
        self.assertEqual(registry2.__cmp__(registry1), -1)

    def test_len(self):
        d = {'a':1}
        registry = self._makeOne(d, b=2)
        self.assertEqual(len(registry), 2)

    def test_getitem(self):
        d = {'a':1}
        registry = self._makeOne(d)
        self.assertEqual(registry['a'], 1)
        
    def test_setitem(self):
        d = {'a':1}
        registry = self._makeOne(d)
        registry['a'] = 2
        self.assertEqual(registry['a'], 2)
        
    def test_delitem(self):
        d = {'a':1}
        registry = self._makeOne(d)
        del registry['a']
        self.assertEqual(registry.get('a'), None)
        
    def test_delitem_raises(self):
        registry = self._makeOne()
        self.assertRaises(KeyError, registry.__delitem__, 'b')

    def test_clear(self):
        d = {'a':1}
        registry = self._makeOne(d)
        registry.clear()
        self.assertEqual(len(registry), 0)

    def test_copy(self):
        d = {'a':1}
        registry = self._makeOne(d)
        registry2 = registry.copy()
        self.assertEqual(registry, registry2)

    def test_items(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        self.assertEqual(sorted(registry.items()), [('a', 1), ('b', 2)])
        
    def test_keys(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        self.assertEqual(sorted(registry.keys()), ['a', 'b'])
        
    def test_values(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        self.assertEqual(sorted(registry.values()), [1, 2])

    def test_iteritems(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        self.assertEqual(sorted(registry.iteritems()), [('a', 1), ('b', 2)])
        
    def test_iterkeys(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        self.assertEqual(sorted(registry.iterkeys()), ['a', 'b'])
        
    def test_itervalues(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        self.assertEqual(sorted(registry.itervalues()), [1, 2])

    def test_contains(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        self.failUnless('a' in registry)
        
    def test_has_key(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        self.failUnless(registry.has_key('a'))

    def test_get(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        self.assertEqual(registry.get('a'), 1)

    def test_fromkeys(self):
        d = {'a':1, 'b':2}
        klass = self._getTargetClass()
        registry = klass.fromkeys(['a', 'b'], 2)
        self.assertEqual(registry['a'], 2)
        self.assertEqual(registry['b'], 2)

    def test_update(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        registry.update({'a':2, 'c':3})
        self.assertEqual(registry['a'], 2)
        self.assertEqual(registry['c'], 3)

    def test_updatekw(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        registry.update(None, a=2, c=3)
        self.assertEqual(registry['a'], 2)
        self.assertEqual(registry['c'], 3)

    def test_setdefault(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        val = registry.setdefault('c', 1)
        self.assertEqual(val, 1)
        self.assertEqual(registry['c'], 1)
        val = registry.setdefault('a', 2)
        self.assertEqual(val, 1)
        self.assertEqual(registry['a'], 1)
        self.assertEqual(registry['b'], 2)
        self.assertEqual(registry['c'], 1)

    def test_iter(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        iterator = iter(registry)
        self.assertEqual(sorted(list(iterator)), ['a', 'b'])

    def test_pop_toomanyargs(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        self.assertRaises(TypeError, registry.pop, 'a', 1, 2)

    def test_pop_default_missing(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        val = registry.pop('c', 1)
        self.assertEqual(val, 1)
        
    def test_pop_nodefault_missing(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        self.assertRaises(KeyError, registry.pop, 'c')

    def test_pop_succeds(self):
        d = {'a':1, 'b':2}
        registry = self._makeOne(d)
        val = registry.pop('a')
        self.assertEqual(val, 1)
        self.failIf('a' in registry)

    def test_popitem_empty(self):
        registry = self._makeOne()
        self.assertRaises(KeyError, registry.popitem)
        
    def test_popitem_ok(self):
        d = {'a':1}
        registry = self._makeOne(d)
        val = registry.popitem()
        self.assertEqual(val, ('a', 1))
        self.failIf('a' in registry)

class TestRegistryFunctional(unittest.TestCase):
    def _getTargetClass(self):
        from repoze.component import Registry
        return Registry
        
    def _makeOne(self, dict=None):
        return self._getTargetClass()(dict)

    def _makeRegistry(self, dict=None):
        registry = self._makeOne(dict)

        registry.register('bladerunner', 'deckardvalue' , None, 'deckard')
        registry.register('friend', 'luckmanvalue', 'luckman', name='name')
        registry.register('fight', 'barrisluckmanvalue', 'barris', 'luckman')

        return registry

    def test_as_mapping(self):
        d = {'a':1, 'b':2, 'c':3, 'd':4}
        registry = self._makeRegistry(d)
        self.failUnless(registry == d) # __cmp__
        self.assertEqual(len(registry), 4) # __len__
        self.assertEqual(registry['a'], 1)
        self.assertEqual(registry['b'], 2)
        registry['e'] = 4
        self.assertEqual(len(registry), 5) # __len__
        self.assertEqual(registry['e'], 4)
        del registry['e']
        self.assertEqual(len(registry), 4) # __len__
        self.assertRaises(KeyError, registry.__getitem__, 'e')
        copy = registry.copy()
        self.failUnless(copy == registry)
        self.assertEqual(sorted(registry.items()),
                         [('a', 1), ('b', 2), ('c', 3), ('d', 4)])
        self.assertEqual(sorted(registry.keys()), ['a', 'b', 'c', 'd'])
        self.assertEqual(sorted(registry.values()), [1, 2, 3, 4])
        self.assertEqual(sorted(registry.iteritems()),
                         [('a', 1), ('b', 2), ('c', 3), ('d', 4)])
        self.assertEqual(sorted(registry.iterkeys()), ['a', 'b', 'c', 'd'])
        self.assertEqual(sorted(registry.itervalues()), [1, 2, 3, 4])
        self.failUnless('a' in registry)
        self.failIf('z' in registry)
        self.failUnless(registry.has_key('a'))
        self.failIf(registry.has_key('z'))
        self.assertEqual(registry.get('a'), 1)
        self.assertEqual(registry.get('z', 0), 0)
        self.assertEqual(registry.get('z'), None)
        self.assertEqual(registry.fromkeys({'a':1}), {'a':None})
        registry.update({'e':5})
        self.assertEqual(len(registry), 5)
        self.assertEqual(registry['e'], 5)
        f = registry.setdefault('f', {})
        f['1'] = 1
        self.assertEqual(registry['f'], f)
        L = []
        for k in registry:
            L.append(k)
        self.assertEqual(sorted(L), ['a', 'b', 'c', 'd', 'e', 'f'])
        val = registry.pop('a')
        self.assertEqual(val, 1)
        self.assertEqual(len(registry), 5)
        item = registry.popitem()
        self.assertEqual(len(registry), 4)
        registry.clear()
        self.assertEqual(len(registry), 0)

    def test_register_and_lookup(self):
        registry = self._makeRegistry()
        look = registry.lookup
        eq = self.assertEqual

        eq(look('bladerunner', None, 'deckard'), 'deckardvalue')
        eq(look('bladerunner', None, ['inherits', 'deckard']), 'deckardvalue')
        eq(look('friend', 'luckman', name='name'), 'luckmanvalue')
        eq(look('fight', 'barris', 'luckman'), 'barrisluckmanvalue')
        eq(look('fight', ('inherits', 'barris'), 'luckman'),
           'barrisluckmanvalue')
        eq(look('fight', ('deckard', 'barris'), 'luckman'),
           'barrisluckmanvalue')
        eq(look('bladerunner', (None,), ('deckard', 'barris')), 'deckardvalue')
        eq(look('friend', 'luckman'), None)
        eq(look('bladerunner', 'deckard', ('luckman',)), None)
        eq(look('bladerunner', None, None), None)
        eq(look('bladerunner', 'barris', 'deckard'), 'deckardvalue')
        eq(look('bladerunner', 'luckman', 'deckard'), 'deckardvalue')

        registry.register('default', 'a', None, None)
        eq(look('default', None, None), 'a')

    def test_register_and_resolve_classes(self):
        registry = self._makeRegistry()
        look = registry.resolve
        eq = self.assertEqual

        eq(look('bladerunner', None, Deckard), 'deckardvalue')
        eq(look('bladerunner', None, InheritsDeckard), 'deckardvalue')
        eq(look('friend', Luckman, name='name'), 'luckmanvalue')
        eq(look('fight', Barris, Luckman), 'barrisluckmanvalue')
        eq(look('fight', InheritsBarris, Luckman), 'barrisluckmanvalue')
        eq(look('fight', DeckardBarris, Luckman), 'barrisluckmanvalue')
        eq(look('bladerunner', None, DeckardBarris), 'deckardvalue')
        eq(look('friend', Luckman), None)
        eq(look('bladerunner', Deckard, Luckman), None)
        eq(look('bladerunner', Luckman, Deckard), 'deckardvalue')
        eq(look('bladerunner', Barris, Deckard), 'deckardvalue')
        eq(look('bladerunner', None, None), None)
                            
    def test_register_and_resolve_instances(self):
        registry = self._makeRegistry()
        look = registry.resolve
        eq = self.assertEqual

        deckard = Deckard(None)
        inheritsdeckard = InheritsDeckard(None)
        luckman = Luckman(None)
        barris = Barris(None)
        inheritsbarris = InheritsBarris(None)
        deckardbarris = DeckardBarris(None, None)

        eq(look('bladerunner', None, deckard), 'deckardvalue')
        eq(look('bladerunner', None, inheritsdeckard), 'deckardvalue')
        eq(look('friend', luckman, name='name'), 'luckmanvalue')
        eq(look('fight', barris, luckman), 'barrisluckmanvalue')
        eq(look('fight', inheritsbarris, luckman), 'barrisluckmanvalue')
        eq(look('fight', deckardbarris, luckman), 'barrisluckmanvalue')
        eq(look('bladerunner', None, deckardbarris), 'deckardvalue')
        eq(look('friend', luckman), None)
        eq(look('bladerunner', deckard, luckman), None)
        eq(look('bladerunner', luckman, deckard), 'deckardvalue')
        eq(look('bladerunner', barris, deckard), 'deckardvalue')
        eq(look('bladerunner', None, None), None)

    def test_register_and_resolve_instances_withdict(self):
        registry = self._makeRegistry()
        look = registry.resolve
        eq = self.assertEqual

        deckard = Deckard(None)
        deckard.__component_types__ = 'deckard'
        inheritsdeckard = InheritsDeckard(None)
        deckard.__component_types__ = 'inherits'
        luckman = Luckman(None)
        luckman.__component_types__ = 'luckman'
        barris = Barris(None)
        barris.__component_types__ = 'barris'
        inheritsbarris = InheritsBarris(None)
        inheritsbarris.__component_types__ = 'inherits'
        deckardbarris = DeckardBarris(None, None)
        deckardbarris.__component_types__ = ('deckard', 'barris')

        eq(look('bladerunner', None, deckard), 'deckardvalue')
        eq(look('bladerunner', None, inheritsdeckard), 'deckardvalue')
        eq(look('friend', luckman, name='name'), 'luckmanvalue')
        eq(look('fight', barris, luckman), 'barrisluckmanvalue')
        eq(look('fight', inheritsbarris, luckman), 'barrisluckmanvalue')
        eq(look('fight', deckardbarris, luckman), 'barrisluckmanvalue')
        eq(look('bladerunner', None, deckardbarris), 'deckardvalue')
        eq(look('friend', luckman), None)
        eq(look('bladerunner', deckard, luckman), None)
        eq(look('bladerunner', luckman, deckard), 'deckardvalue')
        eq(look('bladerunner', barris, deckard), 'deckardvalue')
        eq(look('bladerunner', None, None), None)

    def test_register_and_resolve_oldstyle_classes(self):
        registry = self._makeRegistry()
        look = registry.resolve
        eq = self.assertEqual
        
        eq(look('bladerunner', None, OSDeckard), 'deckardvalue')
        eq(look('bladerunner', None, InheritsDeckard), 'deckardvalue')
        eq(look('friend', Luckman, name='name'), 'luckmanvalue')
        eq(look('fight', Barris, Luckman), 'barrisluckmanvalue')
        eq(look('fight', InheritsBarris, Luckman), 'barrisluckmanvalue')
        eq(look('fight', DeckardBarris, Luckman), 'barrisluckmanvalue')
        eq(look('bladerunner', None, DeckardBarris), 'deckardvalue')
        eq(look('friend', Luckman), None)
        eq(look('bladerunner', Deckard, Luckman), None)
        eq(look('bladerunner', Luckman, Deckard), 'deckardvalue')
        eq(look('bladerunner', Barris, Deckard), 'deckardvalue')
        eq(look('bladerunner', None, None), None)

    def test_register_and_resolve_oldstyle_instances(self):
        registry = self._makeRegistry()
        look = registry.resolve
        eq = self.assertEqual
        
        deckard = OSDeckard(None)
        inheritsdeckard = OSInheritsDeckard(None)
        luckman = OSLuckman(None)
        barris = OSBarris(None)
        inheritsbarris = OSInheritsBarris(None)
        deckardbarris = OSDeckardBarris(None, None)

        eq(look('bladerunner', None, deckard), 'deckardvalue')
        eq(look('bladerunner', None, inheritsdeckard), 'deckardvalue')
        eq(look('friend', luckman, name='name'), 'luckmanvalue')
        eq(look('fight', barris, luckman), 'barrisluckmanvalue')
        eq(look('fight', inheritsbarris, luckman), 'barrisluckmanvalue')
        eq(look('fight', deckardbarris, luckman), 'barrisluckmanvalue')
        eq(look('bladerunner', None, deckardbarris), 'deckardvalue')
        eq(look('friend', luckman), None)
        eq(look('bladerunner', deckard, luckman), None)
        eq(look('bladerunner', luckman, deckard), 'deckardvalue')
        eq(look('bladerunner', barris, deckard), 'deckardvalue')
        eq(look('bladerunner', None, None), None)

    def test_register_and_resolve_oldstyle_instances_withdict(self):
        registry = self._makeRegistry()
        resolve = registry.resolve
        eq = self.assertEqual
        from repoze.component import provides

        deckard = OSDeckard(None)
        provides(deckard, 'deckard')

        inheritsdeckard = OSInheritsDeckard(None)
        provides(inheritsdeckard, 'inhherits')

        luckman = OSLuckman(None)
        provides(luckman, 'luckman')

        barris = OSBarris(None)
        provides(barris, 'barris')

        inheritsbarris = OSInheritsBarris(None)
        provides(inheritsbarris, 'inherits')

        deckardbarris = OSDeckardBarris(None, None)
        provides(deckardbarris, 'deckard', 'barris')

        eq(resolve('bladerunner', None, deckard), 'deckardvalue')
        eq(resolve('bladerunner', None, inheritsdeckard), 'deckardvalue')
        eq(resolve('friend', luckman, name='name'), 'luckmanvalue')
        eq(resolve('fight', barris, luckman), 'barrisluckmanvalue')
        eq(resolve('fight', inheritsbarris, luckman), 'barrisluckmanvalue')
        eq(resolve('fight', deckardbarris, luckman), 'barrisluckmanvalue')
        eq(resolve('bladerunner', None, deckardbarris), 'deckardvalue')
        eq(resolve('friend', luckman), None)
        eq(resolve('bladerunner', deckard, luckman), None)
        eq(resolve('bladerunner', luckman, deckard), 'deckardvalue')
        eq(resolve('bladerunner', barris, deckard), 'deckardvalue')
        eq(resolve('bladerunner', None, None), None)

    def test_adapt(self):
        registry = self._makeRegistry()
        adapt = registry.adapt

        class Adapter:
            def __init__(self, context):
                self.context = context

        registry.register('something', Adapter, 'barris')

        adapter = registry.adapt('something', Barris)
        self.assertEqual(adapter.context, Barris)

    def test_register_Nones(self):
        class Two(object):
            __component_types__ = 'two'

        class One(Two):
            __component_types__ = 'one'

        class B(object):
            __component_types__ = 'b'

        class A(B):
            __component_types__ = 'a'

        instance1 = One()
        instance1.__component_types__ = 'i'

        instance2 = A()
        instance2.__component_types__ = 'i'

        registry = self._makeOne()
        registry.register('foo', 'somevalue', None, None)

        result = registry.resolve('foo', instance1, instance2)
        self.assertEqual(result, 'somevalue')

class TestProvidedBy(unittest.TestCase):
    def _callFUT(self, obj):
        from repoze.component import providedby
        return providedby(obj)

    def test_None(self):
        result = self._callFUT(None)
        self.assertEqual(list(result), [None])

    def test_newstyle_class(self):
        class Foo(object):
            __component_types__ = ['a', 'b']
        result = self._callFUT(Foo)
        self.assertEqual(list(result), ['a', 'b', type(Foo), None])

    def test_oldstyle_class(self):
        class Foo:
            __component_types__ = ['a', 'b']
        result = self._callFUT(Foo)
        self.assertEqual(list(result), ['a', 'b', type(Foo), None])

    def test_oldstyle_instance(self):
        class Foo:
            __component_types__ = ['a', 'b']
        foo = Foo()
        result = self._callFUT(foo)
        self.assertEqual(list(result), ['a', 'b', Foo, None])

    def test_newstyle_instance(self):
        class Foo(object):
            __component_types__ = ['a', 'b']
        foo = Foo()
        result = self._callFUT(foo)
        self.assertEqual(list(result), ['a', 'b', Foo, None])

    def test_string(self):
        result = self._callFUT('foo')
        self.assertEqual(list(result), [str, None])

    def test_int(self):
        result = self._callFUT(1)
        self.assertEqual(list(result), [int, None])

    def test_bool(self):
        result = self._callFUT(True)
        self.assertEqual(list(result), [bool, None])

    def test_None(self):
        import types
        result = self._callFUT(None)
        self.assertEqual(list(result), [types.NoneType, None])

from repoze.component import provides

class Deckard(object):
    provides('deckard')
    def __init__(self, context):
        self.context = context

class Luckman(object):
    provides('luckman')
    def __init__(self, context):
        self.context = context

class Barris(object):
    provides('barris')
    def __init__(self, context):
        self.context = context

class DeckardBarris(object):
    provides('deckard', 'barris')
    def __init__(self, context1, context2):
        self.context1 = context1 
        self.context2 = context2
   
class InheritsDeckard(Deckard):
    provides('inherits')
    def __init__(self, context):
        self.context = context
    
class InheritsBarris(Barris):
    provides('inherits')
    def __init__(self, context):
        self.context = context
    
class OSDeckard:
    provides('deckard')
    def __init__(self, context):
        self.context = context

class OSLuckman:
    provides('luckman')
    def __init__(self, context):
        self.context = context

class OSBarris:
    provides('barris')
    def __init__(self, context):
        self.context = context

class OSDeckardBarris:
    provides('deckard', 'barris')
    def __init__(self, context1, context2):
        self.context1 = context1 
        self.context2 = context2
    
class OSInheritsDeckard(OSDeckard):
    provides('inherits')
    def __init__(self, context):
        self.context = context
    
class OSInheritsBarris(OSBarris):
    provides('inherits')
    def __init__(self, context):
        self.context = context
    
