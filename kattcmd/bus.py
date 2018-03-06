import collections
import pydash


class BusError(Exception):
    pass


_storage = {}
def Set(key, value):
    _storage[key] = value

def Get(key):
    return _storage.get(key, None)


class Bus:

    def __init__(self):
        self.ID = 0
        self.providers = {}
        self.listeners = collections.defaultdict(list)
        self.provide('set', Set)
        self.provide('get', Get)


    def provide(self, topic, callback):
        '''Provide an RPC to be used by the bus.'''
        self.providers[topic] = callback


    def call(self, topic, *args, **kwargs):
        '''Call an RPC that exists on the bus and any listeners.'''

        # Check if RPC exists, throw error on fault.
        def non_existant_rpc():
            return topic not in self.providers

        def raise_RPC_error():
            raise BusError('No RPC Provider: {}'.format(topic))


        # Else call listeners and then return with RPC result.
        def call_listeners():
            if topic in self.listeners:
                for _, listener in self.listeners[topic]:
                    listener(*args, **kwargs)

        def call_rpc(unused):
            return self.providers[topic](*args, **kwargs)

        call_listeners_and_rpc = pydash.flow(call_listeners, call_rpc)

        return pydash.cond([
            (non_existant_rpc, raise_RPC_error),
            (pydash.stub_true, call_listeners_and_rpc)
        ])()


    def listen(self, topic, callback):
        '''Listen to a specific topic and receive a callback for when it is called.'''
        ID = self.ID
        self.ID += 1
        self.listeners[topic].append((ID, callback))
        return ID


    def unlisten(self, topic, ID):
        '''Stop recieving updates for a topic.'''

        def has_id():
            return any(i == ID for i, _ in self.listeners[topic])

        def remove_id():
            items = self.listeners[topic]
            keep = lambda i, _: i != ID
            self.listeners[topic] = [(a, b) for a, b in items if keep(a, b)]

        return pydash.cond([
            (has_id, remove_id)
        ])()


    def unprovide(self, topic):
        '''Unregister a topic.'''

        def has_rpc():
            return topic in self.providers

        def raise_RPC_error():
            raise BusError('No RPC Provider: {}'.format(topic))


        def remove_RPC():
            del self.providers[topic]


        return pydash.cond([
            (has_rpc, raise_RPC_error),
            (pydash.stub_true, remove_RPC)
        ])()
