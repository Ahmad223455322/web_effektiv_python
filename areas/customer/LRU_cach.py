from collections import OrderedDict

class LRUCache:

	def __init__(self, capacity: int):
		self.cache = OrderedDict()
		self.capacity = capacity



	def get_cash(self, key: int) -> int:
		if key not in self.cache:
			return -1
		else:
			self.cache.move_to_end(key)
			return self.cache[key]

	
	def put(self, key: int, value: int) -> None:
		self.cache[key] = value
		self.cache.move_to_end(key)
		
		if len(self.cache) > self.capacity:
			self.cache.popitem(last = False)

