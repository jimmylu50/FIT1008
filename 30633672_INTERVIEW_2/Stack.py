class Node():
    def __init__(self, item=None, link=None):
        self.item = item
        self.next = link

class Stack1:
    def __init__(self):
        """Creates an empty stack"""
        self.head = None
    
    def size(self):
        """Returns the size, i.e. the number
        of elements in the container."""
        ## Alternatively, we could introduce a 'count'
        ## instance variable.
        count = 0
        node = self.head
        while node is not None:
          count += 1
          node = node.next
        return count
    
    def is_empty(self):
        """Returns True if and only if the container is empty."""
        return self.head is None
        
    def is_full(self):
        """Returns True if and only if the container is full."""
        return False
         
    def push(self, item):
        """Places the given item at the top of the stack."""
        new_node = Node(item, self.head)
        self.head = new_node

        
    def pop(self):
        """Removes and returns the top element of the stack,
        or raises an Exception if there is none."""
        if self.is_empty():
          raise IndexError("Attempted to pop empty stack.")
        item = self.head.item
        self.head = self.head.next
        return item
   
    def remove(self, item):
        """Removes first occurrence of item from the list."""
        ## We always re-wire the parent of the removed element.
        ## But we need to handle two cases where there is no parent:
        ## The queue is empty, or the removed element is the head.
        if self.head is None:
          return
        if self.head.item == item:
          self.head = self.head.next
        prev_node = self.head
        current_node = prev_node.next
        while current_node is not None:
          if current_node.item == item:
            prev_node.next = current_node.next
            return
          prev_node = current_node
          current_node = current_node.next
            
    
    def reset(self):
        """Removes all elements from the container."""
        self.head = None
