#!/usr/bin/env python3
""" FIFOCache module
"""

BaseCaching = __import__("base_caching").BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class inherits from BaseCaching and
    implements FIFO caching strategy.
    """

    def __init__(self):
        """ Initializes the cache """
        super().__init__()

    def put(self, key, item):
        """ Adds an item to the cache using FIFO strategy """
        if key is not None and item is not None:
            # Add the new item to the cache
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # If cache is full, discard the first item (FIFO)
                discarded_key = next(iter(self.cache_data))
                self.cache_data.pop(discarded_key)
                print("DISCARD:", discarded_key)

    def get(self, key):
        """ Retrieves an item from the cache """
        return self.cache_data.get(key, None)
