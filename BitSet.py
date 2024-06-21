class BitSet:
    def __init__(self, size):
        self.size = size
        self.bitset = [0] * ((size // 32) + 1) # Used integer of 32 bits
        
    def set(self, index):
        if index >= self.size:
            raise IndexError("Index out of range")
        self.bitset[index // 32] |= 1 << (index % 32)
        
    def clear(self, index):
        if index >= self.size:
            raise IndexError("Index out of range")
        self.bitset[index // 32] &= ~(1 << (index % 32))
        
    def get(self, index):
        if index >= self.size:
            raise IndexError("Index out of range")
        return (self.bitset[index // 32] & (1 << (index % 32))) != 0

# Example of usage
bitset = BitSet(100) # Create a bitset of size 100
bitset.set(10) # Set the bit at index 10
print(bitset.get(10)) # Verify if the bit at index 10 is set true
bitset.clear(10) # Clear the bit at index 10
print(bitset.get(10)) # Verify if the bit at index 10 is set false