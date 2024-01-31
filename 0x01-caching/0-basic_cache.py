#!/usr/bin/env python3
""" BasicCache module
"""

BaseCaching = __import__("base_caching").BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache class inherits from BaseCaching
    """

    def __init__(self):
        """Initialize the cache"""
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        return self.cache_data.get(key) if key is not None else None
