"""
This file implements an interface for user to edit ListADT

@author: Jin Luo
@since: 19 Sep 2019
@input          none
@output         none
@errorHandling  none
@knownBugs      none


"""
from task2 import ListADT
from task3 import read_text_file
import math
import unittest
from test_common import *

class Editor:
    def __init__(self):
        """
        Creates an empty ListADT, size can be varied be still empty

        @pre      None
        @return   a ListADT structure
        @return   length of ListADT
        @post     None
        @complexity     O(1)
        """
        self.text_lines = ListADT(40)
        self.length = 0

    def instruct(self):
        """
        Interface for user to type and place commands

        @pre             None
        @post            something will happen to List structure or print
        @complexity      unsure as it depends on user input
        """
        mark = 1
        read = False
        #this is the user interface
        #input by user is restricted by if statements
        #user can only input something available
        while not read:
            user_input = input("Please type in your command: ")
            if user_input >= "print " + str(mark) and user_input <= "print " + str(self.length):
                print(self.print_num(user_input[-1]))
            elif user_input == "read filename":
                self.read_filename("TestFile.txt")
            elif user_input == "print " or user_input == "print":
                if self.length == 0:
                    print("?") 
                else:
                    for i in range(1, self.length+1):
                        print(self.print_num(i))
            elif user_input >= "delete " + str(mark) and user_input <= "delete " + str(self.length):
                self.delete_num(user_input[-1]) #do we need neg indices for delete
            elif user_input == "delete" or user_input == "delete ":
                self.delete_num("")
            elif user_input >= "insert " + str(mark) and user_input <= "insert " + str(self.length+1):
                line_num = user_input[-1]
                new_array = ListADT(40)
                lines = ''
                while lines != '.\n':
                    lines = input() + '\n'
                    new_array.insert(new_array.__len__(), lines.strip('\n'))
                new_array.delete(new_array.__len__()-1)
                self.insert_num_strings(line_num, new_array)
            elif user_input == "insert 1" and self.length == 0:
                line_num = user_input[-1]
                new_array = ListADT(40)
                lines = ''
                while lines != '.\n':
                    lines = input() + '\n'
                    new_array.insert(new_array.__len__(), lines.strip('\n'))
                new_array.delete(new_array.__len__()-1)
                self.insert_num_strings(line_num, new_array)
                #if len == 4, do we allow user to insert i line 5
            elif user_input >= "insert -1" and user_input <= "insert -" + str(self.length+1):
                line_num = user_input[-2] + user_input[-1]
                new_array = ListADT(40) 
                lines = ''
                while lines != '.\n':
                    lines = input() + '\n'
                    new_array.insert(new_array.__len__(), lines.strip('\n'))
                new_array.delete(new_array.__len__()-1)
                print(self.insert_num_strings(line_num, new_array))
            elif user_input == "quit":
                read = True
            else:
                print("?")

    def read_filename(self, file_name):
        """
        Reads a text file, name of file given by user

        @pre          file_name must be a string and name to a text file
        @param        string name of the file
        @post         class variable text_lines contains the file texts
        @post         length = length of text_lines
        @complexity   O(m), m being the size of text file
        """
        #read file of text file
        if file_name != str(file_name):
            print("?")
        the_array = (read_text_file(file_name))
        self.text_lines = the_array
        self.length = self.text_lines.__len__()
        
    def print_num(self, line_num):
        """
        Prints lines from ListADT text_lines

        @pre           line_num must be a string
        @param         line number provided by user to know which line to print
        @return        the line of text at line number
        @post          None
        @complexity    O(1)
        """
        #print line number in text_lines
        if line_num == "" or line_num == " ":
            return(self.text_lines)
        else:
            return(self.text_lines.__getitem__(int(line_num)-1))

    def delete_num(self, line_num):
        """
        Removes lines in ListADT text_lines

        @pre        line_num must be a string
        @param      line number to indicate which line to delete
        @post       some lines of texts in text_lines will be removed
        @complexity      O(m), m depending on the result of line_num
        can be 1, or m = self.length
        """
        #if line_num is empty, remove every element
        #else just delete the line number
        if line_num == "" or line_num == " ":
            for i in range(self.length):
                self.text_lines.delete(0)
                self.length -= 1
        #the line_num is restricted by the self.instruct, which is the interface
        #user is only allowed to type within index of 1 to self.length
        elif line_num == str(line_num):
            self.text_lines.delete(int(line_num)-1)
            self.length -= 1

    def insert_num_strings(self, line_num, lines):
        """
        Inserts a List of strings provided by user into the line number of
        text_lines provided by user

        @pre                 line_num must be a string and lines must be ListADT
        @param: line_num     line number of text_lines to insert the strings in
        @param: lines        ListADT structure containing strings
        @post:               text_lines will be updated
        @post:               self.length will also be updated
        @return              the updated text_lines
        @complexity          O(m), m being the size of lines
        
        """
        #if line_num is positive, it will insert from the line
        #if line_num is negative, it will slightly vary but still insert from the line
        if int(line_num) >= 1 and int(line_num) <= self.length +1:
            for i in range(lines.__len__()):
                self.text_lines.insert(int(line_num)-1+i, lines.__getitem__(i))
                self.length += 1
            return(self.text_lines)
        elif int(line_num) <= -1 and int(line_num) >= -self.length-1:
            for i in range(lines.__len__()):
                #insert with negative index + self.length
                self.text_lines.insert(int(line_num)+self.length+1, lines.__getitem__(i))
                self.length += 1
            return(self.text_lines)
        #else return ?
        else:
            return("?")

    def search_string(self, query):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

class testcases(unittest.TestCase):
    def test_read(self):
        ed = Editor()
        ed.read_filename('TestFile.txt')
        self.assertTrue(equal_lines(ed, test_content), msg =  "File not correctly read.")

    def test_delete(self):
        ed = Editor()
        ed.read_filename('TestFile.txt')
        ed.delete_num("1")
        self.assertTrue(equal_lines(ed, test_content[1:]), msg =  "Failed to delete first line.")
   
        for index in ["-5"]:
            with self.assertRaises(IndexError, msg = "Deleting out-of-bounds lines should fail."):
                ed.read_filename('TestFile.txt')
                ed.delete_num(index)

    def test_insert(self):
        ed = Editor()
        ed.insert_num_strings("1", ToListADT(ListADT, [test_content[0]]))
        self.assertTrue(equal_lines(ed, [test_content[0]]), msg =  "Failed to insert single line.")

        ed = Editor()
        ed.insert_num_strings("-1", ToListADT(ListADT, [test_content[2], test_content[3]]))
        self.assertTrue(equal_lines(ed, [test_content[2], test_content[3]]), msg =  "Incorrect handling of negative insertion")

if __name__ == "__main__":
    unittest.main()


