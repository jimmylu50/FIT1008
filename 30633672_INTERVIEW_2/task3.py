"""
This file reads a file and returns a ListADT of containing each line of the file content

@author: Jin Luo
@since: 19 Sep 2019
@input          none
@output         none
@errorHandling  none
@knownBugs      none

"""
from task2 import ListADT
import math
import unittest
from test_common import *

def read_text_file(name):
    """
    Reads a file and returns a ListADT of containing each line of the file content

    @param       name of text file
    @return      a ListADT of elements containing each line from the text file
    @complexity  best and worst case: O(m*n), n being lines in file, m from insert function 
    """
    with open(name, 'r') as f:
        read_line = f.readlines()
        the_array = ListADT(len(read_line))
        for i in range(len(read_line)):
            the_array.insert(i, read_line[i].strip('\n'))
        return the_array

class TestTask3(unittest.TestCase):
  def test_read_file(self):
    test_lines = read_text_file('TestFile.txt')
    self.assertEqual([ l.strip('\n') for l in ToList(test_lines) ], test_content, msg = "File not correctly read.")
    
if __name__ == '__main__':
  unittest.main()
