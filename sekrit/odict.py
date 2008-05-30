#! /usr/bin/env python

# http://urchin.earth.li/~twic/odict.py

"""
This is a straightforward ordered dict implementation. It aims to be
comprehensible, clean, correct and concise. It does not aim to be
fast.

As a bonus, i provide icmp, a general function to compare two
iterators.

(c) 2005 Tom Anderson <twic@urchin.earth.li> - all rights reserved

Redistribution and use in source and binary forms, with or without
modification, are permitted.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

class odict(dict):
	"""
	An ordered dict (odict). This is a dict which maintains an
	order to its items; the order is rather like that of a list,
	in that new items are, by default, added to the end, but items
	can be rearranged. Note that updating an item (setting a value
	where the key is already in the dict) is not considered to
	create a new item, and does not affect the position of that
	key in the order. However, if an item is deleted, then a new
	item with the same key is added, this is considered a new
	item.

	This order is visible in two ways. Firstly, whenever an
	implicit order of the items in the dict is exposed, for
	example when it is iterated over, or when it is stringified,
	the proper order is used. Secondly, the member variable
	'order' is a list of all the keys in the dict, in order; this
	is a magic list, which presents a 'live' view of the odict,
	and which can be modified only in certain ways: items can be
	deleted, in which case they are removed from the underlying
	odict, and they can be rearranged using the sort, reverse,
	move and swap methods (the latter two being unique to this
	class), but new items cannot be added in any way.
	"""

	@staticmethod
	def fromkeys(ks, v=None):
		d = odict()
		for k in ks:
			d[k] = v
		return d
	def __init__(self, items=None):
		dict.__init__(self)
		self._order = []
		self.order = _orderproxy(self)
		if (items != None):
			self.update(items)
	def __setitem__(self, k, v):
		if (not k in self):
			self._order.append(k)
		dict.__setitem__(self, k, v)
	def __delitem__(self, k):
		dict.__delitem__(self, k)
		self._order.remove(k)
	def update(self, items):
		if (not isinstance(items, dict)):
			items = dict(items) # thus handles both dicts and sequences of pairs
		for k in items:
			self[k] = items[k]
	def pop(self, k, d=None):
		self._order.remove(k)
		return dict.pop(self, d)
	def popitem(self, i=-1):
		"Pops the item at index i in the order, defaulting to the last."
		if (len(self) == 0):
			raise KeyError, "odict is empty"
		k = self._order.pop(i)
		v = dict.pop(self, k)
		return v
	def clear(self):
		dict.clear(self)
		self._order[:] = []
	def __iter__(self):
		return self.iterkeys()
	def keys(self):
		return list(self._order)
	def iterkeys(self):
		return iter(self._order)
	def values(self):
		return [self[k] for k in self._order]
	def itervalues(self):
		for k in self.iterkeys():
			yield self[k]
	def items(self):
		return [(k, self[k]) for k in self._order]
	def iteritems(self):
		for k in self.iterkeys():
			yield (k, self[k])
	# the minimal set of comparison methods seems to be eq, ne and cmp; not sure why
	def __eq__(self, other):
		if (len(self) != len(other)):
			return False
		return icmp(self.iteritems(), other.iteritems()) == 0
	def __ne__(self, other):
		return not self == other
	def __cmp__(self, other):
		"If other is an odict, compares the two as if comparing their items lists. If not, compares their types."
		if (isinstance(other, odict)):
			return icmp(self.iteritems(), other.iteritems())
		else:
			return cmp(type(self), type(other)) # i think this is the right thing to do ...
	def __repr__(self):
		return "odict.odict(" + str(self) + ")"
	def __str__(self):
		return "{" +", ".join(repr(k) + ": " + repr(self[k]) for k in self._order) + "}"

class _orderproxy(list): # should this be a subclass of list, or object?
	def __init__(self, od):
		self.od = od
	def __getitem__(self, i):
		return self.od._order[i]
	def __getslice__(self, i, j):
		return self.od._order[i:j]
	def __setitem__(self, i, x):
		raise NotImplementedError, "assignment to an order list is not possible"
	def __setslice__(self, i, j, xs):
		raise NotImplementedError, "slice assignment to an order list is not possible"
	def insert(self, i, x):
		raise NotImplementedError, "insertion into an order list is not possible (yes that is a word!)"
	def append(self, x):
		raise NotImplementedError, "appension to an order list is not possible (yes that is a word!)"
	def extend(self, xs):
		raise NotImplementedError, "extension of an order list is not possible"
	def __iadd__(self, other):
		raise NotImplementedError, "in-place addition to an order list is not possible"
	def __imul__(self, other):
		raise NotImplementedError, "in-place multiplication of an order list is not possible"
	def __delitem__(self, i):
		del self.od[self.od._order[i]]
	def __delslice__(self, i, j):
		for x in self.od._order[i:j]: # we rely on slices being copies here
			del self.od[x]
	def pop(self, i=-1):
		k = self.od._order[i]
		del self.od[k] # incurs an unnecessary list.remove
		return k
	def remove(self, v):
		del self.od[v]
	def move(self, i, j):
		"Moves an item from index i to index j; morally equivalent to self.insert(j, self.pop(i))."
		self.od._order.insert(j, self.od._order.pop(i))
	def swap(self, i, j):
		"Swaps the items at indices i and j."
		t = self.od._order[j]
		self.od._order[j] = self.od._order[i]
		self.od._order[i] = t
	def reverse(self):
		self.od._order.reverse()
	def sort(self, **kwargs): #cmp, key, reverse
		self.od._order.sort(**kwargs)
	def __len__(self):
		return len(self.od)
	def __contains__(self, x):
		return x in self.od
	def count(self, x):
		return self.od._order.count(x)
	def index(self, x, start=0, stop=None):
		if (stop == None):
			return self.od._order.index(x, start)
		else:
			return self.od._order.index(x, start, stop)
	def __iter__(self):
		return iter(self.od._order)
	def __reversed__(self):
		return self.od._order.__reversed__()
	# it appears we have to override the individual rich comparison methods
	def __eq__(self, other):
		return self.od._order == other
	def __ne__(self, other):
		return self.od._order != other
	def __gt__(self, other):
		return self.od._order > other
	def __ge__(self, other):
		return self.od._order >= other
	def __lt__(self, other):
		return self.od._order < other
	def __le__(self, other):
		return self.od._order <= other
	# slightly weirdly, it looks like we don't actually need to override __cmp__
	def __cmp__(self, other):
		return cmp(self.od._order, other)
	def __add__(self, other):
		return self.od._order + other
	def __radd__(self, other):
		return list(other) + self.od._order
	def __mul__(self, other):
		return self.od._order * other
	def __rmul__(self, other):
		return other * self.od._order
	def __repr__(self):
		return "[" + ", ".join(repr(x) for x in self.od._order) + "]"

def icmp(a, b):
	"Compares two iterators. This works exactly like comparing two lists. This belongs in itertools."
	for xa in a:
		try:
			xb = b.next()
			d = cmp(xa, xb)
			if (d != 0):
				return d
		except StopIteration:
			return 1
	try:
		b.next()
		return -1
	except StopIteration:
		return 0
