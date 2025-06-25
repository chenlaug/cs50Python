import sys
class Jar:
    def __init__(self, capacity = 12, size = 0):
        self.capacity = capacity
        self.size = size

    def __str__(self):
      return f"{'🍪' * self.size}"

    def deposit(self, n):
      self.size += n

    def withdraw(self, n):
      if n > self.size:
          raise ValueError("Pas assez de cookies pour retirer")
      self.size -= n

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, newCapacity):
      if newCapacity < 0:
            raise ValueError("Capacity must be non-negative")
      self._capacity = newCapacity

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, newSize):
        if newSize > self.capacity:
            raise ValueError(f"Size: {newSize} cannot be greater than Capacity: {self.capacity}")
        if newSize < 0:
            raise ValueError("Size cannot be negative")
        self._size = newSize

def main():
    j1 = Jar(capacity = 10, size=1)
    print(j1)

if __name__ == "__main__":
    main()
