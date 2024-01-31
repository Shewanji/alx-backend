#!/usr/bin/env python3
"""module for the class LRUCache"""

BaseCaching = __import__("base_caching").BaseCaching


class LRUCache(BaseCaching):
    """A LRUCache class that inherits from BaseCaching."""

    def __init__(self):
        """Initializes the cache"""
        super().__init__()
        self.order = []  # List to track the order of keys

    def put(self, key, item):
        """Adds an item to the cache using LRU strategy"""
        if key is not None and item is not None:
            # Add the new item to the cache
            self.cache_data[key] = item

            # Update the order to reflect the most recent access
            if key in self.order:
                self.order.remove(key)
            self.order.append(key)

            # Check if cache is full
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # Discard the least recently used item (LRU)
                discarded_key = self.order.pop(0)
                del self.cache_data[discarded_key]
                print("DISCARD:", discarded_key)

    def get(self, key):
        """Retrieves an item from the cache"""
        if key in self.cache_data:
            # Update the order to reflect the most recent access
            self.order.remove(key)
            self.order.append(key)
            return self.cache_data[key]
        return None
