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

        @pre            size input must be number
        @param          size of array list
        @return         a list data structure
        @post           an empty list object is created        
        @complexity     best and worst case: O(size)
        """
        self.the_array = [None] * size
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

        @pre            other must be a ListADT too
        @param          an input from user, can be anything
        @return         return True if they are same type and have same elements
        @return         return False if not same type or not same elements
        @post           None
        @complexity     best case: O(1) - breaks in first if loop, worst case
                        O(n), n being length of list
        """
        if type(self) != type(other):
            return False
        if self.__len__() != other.__len__():
            return False
        for i in range(self.length):
            if self.the_array[i] != other[i]:
                return False
        return True


    def insert(self, index, item):
        """
        Adds the input item at a given index of the array list.

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
        @complexity     best and worst case: O(m), m = the length to index
        """
        no_space_left = self.is_full()
        has_space = self.is_empty()
        if int(index) != index: 
            raise IndexError('Not a valid number index')
        if not has_space:
            if -self.length > index or index > self.length:
                raise IndexError('Not a valid index in range of array')
        if no_space_left:
            raise Exception("No space left, cannot insert anymore")
        #insert by shifting the elements to right and place item into index
        if index >= 0:
            for i in range(self.length, index, -1):
                self.the_array[i+1] = self.the_array[i]
            self.the_array[index] = item
        elif index < 0:
            for i in range(self.length, index+self.length, -1):
                self.the_array[i+1] = self.the_array[i]
            self.the_array[index+self.length] = item
        self.length += 1
        

    def delete(self, index):
        """
        Deletes the item at the index provided in the list.

        @pre        index must be valid on ListADT
        @param      index of which item to be deleted
        @return     the deleted item from the list
        @post       if the index is valid, list has one fewer elements
        @post       raises error if the index given is not a real integer
        @post       raises error if the index given is out of range of list
        @post       index works with both positive and negative valid indexes
        @post       raises error if the list is empty
        @post       if index wasn't in list range, list is unchanged  and error is raised
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
        #delete by relocating the next index item into the left one
        if index >= 0:
            while index != self.length:
                self.the_array[index] = self.the_array[index+1]
                index += 1
        else:
            while index != -1:
                self.the_array[index+self.length] = self.the_array[index+1+self.length]
                index += 1
        self.length -= 1
        return self.ret_item
        
    def is_full(self):
        """
        Determines whether the list is full.
        Since it is implemented with arrays, it can get full.

        @pre        None
        @return     true if the list is full, false otherwise
        @post       None
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
    def test_init(self):
        y = ListADT(10)

    def test_str(self):
        x = ListADT(10)
        append(x, [1, 2, 3])
        self.assertEqual(str(x).strip('\n'), '1\n2\n3')

    def test_len(self):
        x = ListADT(20)
        self.assertEqual(len(x), 0, msg="Length of empty list should be 0")
        x.insert(0, 2)
        self.assertEqual(len(x), 1, msg="Length should be 1")

    def test_get(self):
        x = ListADT(10)
        append(x, [0, 1, 2, 3, 4])
        for index, value in [ (1, 1), (-2, 3)]:
            self.assertEqual(x[index], value, msg="Incorrect _getitem_.")

    def test_set(self):
        x1 = ListADT(10)
        append(x1, [1, 2, 3])
        x1[0] = 8
        self.assertTrue(equal(x1, [8, 2, 3]), msg = "Incorrect assignment at index 0")

    def test_eq(self):
        x1 = ListADT(10)
        x2 = ListADT(20)
        self.assertTrue(x1 == x2, msg =  "Lists with different capacity should still be equal.")
        append(x1, [1, 2, 3])
        self.assertFalse(x1 == [1, 2, 3], "Equality test doesn't check type.")

    def test_insert(self):
        x = ListADT(10)
        x.insert(0, 1)
        self.assertTrue(equal(x, [1]), msg =  "Insertion in empty list failed")
        x.insert(1, 2)
        self.assertTrue(equal(x, [1, 2]), msg =  "Insertion at end failed")

    def test_delete(self):
        x = ListADT(10)
        append(x, [0, 1, 2, 3, 4, 5])
        x.delete(2)
        self.assertTrue(equal(x, [0,1,3,4,5]), msg =  "Delete from middle failed")
        x.delete(-4)
        self.assertTrue(equal(x, [0,3,4,5]), msg =  "Negative deletion failed")

if __name__ == '__main__':
    unittest.main()
