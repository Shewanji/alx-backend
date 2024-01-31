#!/usr/bin/env python3
"""This module function inherits from BaseCaching and is a caching system"""

BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    # Initialize the cache
    def __init__(self):
        # Call the parent init
        super().__init__()
        # Create a dictionary to store the frequencies of the keys
        self.frequencies = {}
        # Create a dictionary to store the recency of the keys
        self.recency = {}
        # Create a counter to track the order of insertion
        self.counter = 0

    # Add an item to the cache using LFU strategy
    def put(self, key, item):
        # If key or item is None, do nothing
        if key is None or item is None:
            return
        # If the key is already in the cache, update its value and frequency
        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequencies[key] += 1
        # If the cache is full, discard the least frequently used item
        elif len(self.cache_data) >= self.MAX_ITEMS:
            # Find the minimum frequency among the keys
            min_freq = min(self.frequencies.values())
            # Find the keys with the minimum frequency
            candidates = [
                    k for k, v in self.frequencies.items() if v == min_freq
                    ]
            # If there is more than one candidate, use the LRU algorithm
            if len(candidates) > 1:
                # Find the least recently used key among the candidates
                lru_key = min(candidates, key=lambda k: self.recency[k])
                # Remove the LRU key from the cache
                self.cache_data.pop(lru_key)
                self.frequencies.pop(lru_key)
                self.recency.pop(lru_key)
                # Print the discarded key
                print("DISCARD:", lru_key)
            # If there is only one candidate, remove it from the cache
            else:
                # Get the key with the minimum frequency
                lfu_key = candidates[0]
                # Remove the LFU key from the cache
                self.cache_data.pop(lfu_key)
                self.frequencies.pop(lfu_key)
                self.recency.pop(lfu_key)
                # Print the discarded key
                print("DISCARD:", lfu_key)
            # Add the new key and its value to the cache
            self.cache_data[key] = item
            # Set the frequency of the new key to 1
            self.frequencies[key] = 1
        # If the cache is not full, add the new key and its value to the cache
        else:
            self.cache_data[key] = item
            # Set the frequency of the new key to 1
            self.frequencies[key] = 1
        # Increment the counter by 1
        self.counter += 1
        # Set the recency of the key to the counter value
        self.recency[key] = self.counter

    # Retrieve an item from the cache
    def get(self, key):
        # If key is None or not in the cache, return None
        if key is None or key not in self.cache_data:
            return None
        # return the value of the key and update its frequency and recency
        else:
            # Get the value of the key
            value = self.cache_data[key]
            # Increment the frequency of the key by 1
            self.frequencies[key] += 1
            # Increment the counter by 1
            self.counter += 1
            # Set the recency of the key to the counter value
            self.recency[key] = self.counter
            # Return the value of the key
            return value
