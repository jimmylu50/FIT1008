#!/usr/bin/python3
"""
This file implements list ADT using Python lists as fake objects and arrays.

@author: Jin Luo
@since: 19 Sep 2019
@input          none
@output         none
@errorHandling  none
@knownBugs      none

Invariants:
- length is never greater than len(the_array)
- length points to the first empty position (if any)
- all slots in positions -length to length-1 of the_array contain items.
@referenced to previous python documents provided fit1008 labs
"""
import math
import unittest
from test_common import *

class ListADT:

    def __init__(self, size):
        """
        Creates an empty object of the class, i.e., an empty array list.
        The list will have a size great or equal to 40
        If user input is less than 40, the size is changed to 40, otherwise
        it will be the user input size

        @pre            None
        @param          size of array list
        @return         a list data structure
        @post           an empty list object is created
        @complexity     best and worst case: O(size)
        """
        if size < 40:
            self.the_array = [None] * 40
            self.capacity = 40
        else:
            self.the_array = [None] * size
            self.capacity = size
        self.length = 0

    def __str__(self):
        """
        Returns the strings of each element from the list.

        @pre            None
        @return         the strings of each element from the list
        @post           None
        @complexity     best and worst case: O(n), n being length of list
        """
        self.string = ''
        for i in range(self.length):
            self.string += str(self.the_array[i]) + '\n'
        return self.string

    def __len__(self):
        """
        Returns the length of the list.

        @pre            None
        @return         the length of the list
        @post           None
        @complexity     best and worst case: O(1)
        """
        return self.length
    
    def is_empty(self):
        """
        Determines if the list has any elements.

        @pre            None
        @return         false if list has elements, true if empty
        @post           None
        @complexity     best and worst case: O(1)
        """
        return self.length == 0

    def __getitem__(self, index):
        """
        Returns the item at given index in the list

        @pre            the ListADT must have elements at the given index
        @param          the index of the list
        @post           raises error if the index given is not a real integer
        @post           raises error if the index given is out of range of list
        @post           index works with both positive and negative valid indexes
        @return         the item in the list at the given index
        @post           None
        @complexity     best and worst case: O(1)
        """
        has_space = self.is_empty()
        if int(index) != index: 
            raise IndexError('Not a valid number index')
        if not has_space:
            if -self.length > index or index > self.length-1:
                raise IndexError('Not a valid index in range of array')
        if index >= 0:
            return self.the_array[index]
        else:
            return self.the_array[index+self.length]

    def __setitem__(self, index, item):
        """
        Sets an item to be the new item at a given index in the list
        @pre            index must be in range
        @param          the index of the list
        @param          an item to place at the given index of the list
        @post           raises error if the index given is not a real integer
        @post           raises error if the index given is out of range of list
        @post           index works with both positive and negative valid indexes
        @return         the item in the list at the given index
        @post           None
        @complexity     best and worst case: O(1)
        """
        has_space = self.is_empty()
        if int(index) != index: 
            raise IndexError('Not a valid number index')
        if not has_space:
            if -self.length > index or index > self.length-1:
                raise IndexError('Not a valid index in range of array')
        if index >= 0:
            self.the_array[index] = item
        else:
            self.the_array[index+self.length] = item

    def __eq__(self, other):
        """
        Checks if the self is equal to the given 'other' or not

        @pre            None
        @param          an input from user, can be anything
        @return         return True if they are same type and have same elements
        @return         return False if not same type or not same elements
        @post           None
        @complexity     best case: O(1) - breaks in first if loop, worst case
                        O(n), n being length of list
        """
        if type(self) != type(other):
            return False
        for i in range(self.length):
            if self.the_array[i] != other[i]:
                return False
        return True


    def insert(self, index, item):
        """
        Adds the input item at a given index of the array list.
        If ListADT is full, the list is increased in size by around 1.9 times

        @pre            there must be enough space in list
        @param          new_item to add to this list
        @param          index to place the new_item in
        @return         a new listADT where new_item is placed into the given
                        index and all items after new_item are pushed backwards
        @post           raises error if the index given is not a real integer
        @post           raises error if the index given is out of range of list
        @post           index works with both positive and negative valid indexes
        @post           raises error if there is no space left
        @post           if no error and inserted, the list is 1 size bigger
        
        @post           if list is full, it is increased by 1.9 times
        @post           the resized list will have the same elements but with
                        different capacity
        @complexity     best and worst case: O(m), m = the length to index
        """
        no_space_left = self.is_full()
        has_space = self.is_empty()
        if int(index) != index: 
            raise IndexError('Not a valid number index')
        if not has_space:
            if -self.length > index or index > self.length:
                raise IndexError('Not a valid index in range of array')
        #resizing when not enough space
        if no_space_left:
            new_capacity = round((self.length * 1.9)+0.5)
            new_array = [None]*(new_capacity)
            for i in range(self.length):
                new_array[i] = self.the_array[i]
            self.the_array = new_array
            self.capacity = new_capacity
        if index >= 0:
            for i in range(self.length-1, index-1, -1):
                self.the_array[i+1] = self.the_array[i]
            self.the_array[index] = item
        elif index < 0:
            for i in range(self.length-1, index+self.length-1, -1):
                self.the_array[i+1] = self.the_array[i]
            self.the_array[index+self.length] = item
        self.length += 1
        
        

    def delete(self, index): 
        """
        Deletes the item at the index provided in the list.
        If number of elements in ListADT is smaller than 1/4 of len,
        the size is then halved

        @pre        index must be valid on ListADT
        @param      index of which item to be deleted
        @return     the deleted item from the list
        @post       if the index is valid, list has one fewer elements
        @post       raises error if the index given is not a real integer
        @post       raises error if the index given is out of range of list
        @post       index works with both positive and negative valid indexes
        @post       raises error if the list is empty
        @post       if index wasn't in list range, list is unchanged and error is raised
        
        @post       if the length is smaller than 1/4 of len, the total size
                    is resized to half of its size, containing same elements
        @complexity best and worst case: O(m), m being size between length and index
        """
        has_space = self.is_empty()
        if int(index) != index: 
            raise IndexError('Not a valid number index')
        if not has_space:
            if -self.length > index or index > self.length-1:
                raise IndexError('Not a valid index in range of array')
        if self.length == 0:
            raise Error("Cannot delete since it's an empty list")
        self.ret_item = self.the_array[index]
        if index >= 0:
            while index != self.length:
                self.the_array[index] = self.the_array[index+1]
                index += 1
        else:
            while index != -1:
                self.the_array[index+self.length] = self.the_array[index+1+self.length]
                index += 1
        self.the_array[self.capacity-1] = None
        self.length -= 1
        #resizing if size reached 
        if self.length < self.capacity/4 and self.capacity//2 >= 40:
            new_array = [None] * (self.capacity//2)
            for i in range(self.length):
                new_array[i] = self.the_array[i]
            self.the_array = new_array
            self.capacity = int(self.capacity//2)
        return self.ret_item
        
    def is_full(self):
        """
        Determines whether the list is full.
        Since it is implemented with arrays, it can get full.

        @return     true if the list is full, false otherwise
        @complexity best and worst case: O(1)
        """
        return self.length == len(self.the_array)

    def __contains__(self, item):
        """
        Checks if the item to look for is in the list or not

        @pre        None
        @param      item to search for in list
        @return     true if the list contains the item, false if it does not contain
        @post       None
        @complexity best case is O(1), worst case is O(n), n being length
        """
        for i in range(self.length):
            if item == self.the_array[i]:
                return True
        return False
 
    def append(self, item):
        """
        Adds the input item at the end of the list.

        @pre            List must not be full
        @param          new_item to add to this list
        @post           returns True if list has space, False it is has not
        @post           if True, the list has one more element after the method is called and
                        list[last] equals new_item after the method is called
        @post           If False, list is untouched
        @complexity     best and worst case: O(1)
        """
        has_space_left = not self.is_full()
        if has_space_left:
            self.the_array[self.length] = item
            self.length +=1
        else:
            raise Exception('List is full')
        
    
    def unsafe_set_array(self,array,length):
        """
        UNSAFE: only to be used during testing to facilitate it!! DO NOT USE FOR ANYTHING ELSE
        """
        try:
            assert self.in_test_mode
        except:
            raise Exception('Cannot run unsafe_set_array outside testing mode')
			
        self.the_array = array
        self.length = length

class testcase(unittest.TestCase):
    def test_insert(self):
        x = ListADT(10)
        append(x, [1 for i in range(1000)])
        if not hasattr(x, "the_array"):
            raise AttributeError("could not identify underlying array for the ListADT.")

        y = ListADT(10)
        self.assertEqual(len(y.the_array), 40, "Allocated array below threshold.")

        y = ListADT(44)
        for i in range(45):
            y.insert(i, i)
        self.assertEqual(len(y.the_array), 84, "Incorrect grow.")
        for i in range(25):
            y.delete(len(y)-1)
        self.assertTrue(len(y.the_array) == 42, "Incorrect shrink.")

if __name__ == '__main__':
    unittest.main()
