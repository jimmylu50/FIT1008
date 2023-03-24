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
from Stack import *
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
        self.stack = Stack1()

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
                    print("?") #if empty, do we print ?
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
            elif user_input <= "insert -1" and user_input <= "insert -" + str(self.length+1):
                line_num = user_input[-2] + user_input[-1]
                new_array = ListADT(40) 
                lines = ''
                while lines != '.\n':
                    lines = input() + '\n'
                    new_array.insert(new_array.__len__(), lines.strip('\n'))
                new_array.delete(new_array.__len__()-1)
                print(self.insert_num_strings(line_num, new_array))
            elif user_input == "undo":
                self.undo()
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
        #if line_num is empty, remove every element by using loop
        #else just delete the line number
        self.counter2 = 0
        #counter2 is used for undoing
        if line_num == "" or line_num == " ":
            #in loop, item and index will be pushed into stack
            for i in range(self.length):
                self.stack.push(str(self.text_lines.__getitem__(0))) #item
                self.stack.push(0) #index
                self.text_lines.delete(0)
                self.length -= 1
                self.counter2 += 1
            #push 'delete' to back
            self.stack.push(self.counter2)
            self.stack.push('delete')
        else:
            self.stack.push(self.text_lines.__getitem__(int(line_num)-1)) #item
            self.stack.push(int(line_num)-1) #index
            self.text_lines.delete(int(line_num)-1)
            self.length -= 1
            self.counter2 += 1
            self.stack.push(self.counter2)
            self.stack.push('delete')
            
            #index and item will also be pushed back as well as 'delete'
        

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
        self.counter = 0
        #counter is used for undo
        if int(line_num) >= 1:
            #for whatever length of lines is, loop that many times
            for i in range(lines.__len__()):
                self.text_lines.insert(int(line_num)-1+i, lines[i])
                #insert at the line_num index
                self.stack.push(int(line_num)-1) #index for undo
                self.length += 1
                self.counter += 1 #counter for undo
            self.stack.push(self.counter)
            self.stack.push('insert')
            return(self.text_lines)
        elif int(line_num) <= -1:
            for i in range(lines.__len__()):
                self.text_lines.insert(int(line_num)+self.length+1, lines[i])
                self.stack.push(int(line_num)-1) #index for undo
                self.length += 1
                self.counter += 1
            self.stack.push(self.counter)
            self.stack.push('insert')
            return(self.text_lines)
        #else return '?'
        else:
            return("?")

    def search_string(self, query):
        """
        Searches for strings in the text_lines

        @pre                 None
        @param: query        a string provided for user wanting to search
                             in text_lines
        @return              line numbers of text_lines which contain the string
        @post                None
        @complexity          best case: O(n*l) worst case = O(n*m*l)
                            n = self.length
                            m = len(new_string)
                            l = len(query)
        """
        #loop through every element of text_lines
        new_list = ListADT(40)
        i = 0
        while i != self.length:
            new_string = str(self.text_lines.__getitem__(i))
            b = True
            j = 0
            #loop through every letter of string
            while j != len(new_string) and b == True:
                if new_string[j] == str(query)[0]:
                    c = True
                    k = 0
                    #loop through every letter of query
                    while k != len(query) and c == True:
                        if j+k < len(new_string):
                            if new_string[j+k] == query[k] and k == len(query)-1:
                                new_list.insert(new_list.__len__(), i+1)
                                b, c = False, False
                            elif new_string[j+k] == query[k]:
                                k += 1
                            else:
                                j += 1
                                c = False
                        else:
                            i += 1
                            b, c = False, False
                else:
                    j += 1
            i += 1
        return_array = [None] * new_list.__len__()
        for i in range(new_list.__len__()):
            return_array[i] = new_list.__getitem__(i)
        return (return_array)

    def undo(self):
        """
        Undo the last insert or delete that occurred
        Done by storing deleted and insert variables into a Stack

        @post    text_lines will be returned to how it was in previous step
        @complexity        O(m), m being either size of counter or counter2
        """
        new_item = self.stack.pop()
        if new_item == 'insert':
            for i in range(self.stack.pop()):
                self.text_lines.delete(self.stack.pop())
            self.length -= 1
        elif new_item == 'delete':
            for i in range(self.stack.pop()):
                index = self.stack.pop()
                item = self.stack.pop()
                if int(index) >= 0:
                    self.text_lines.insert(index, item)
                elif int(index) < 0:
                    self.text_lines.insert(index, item)
                self.length += 1

class testcase(unittest.TestCase):
    def test_undo(self):
        ed = Editor()
    
        extra_lines = [ "These are some extra lines.", "They are will be added to the string." ]

        ed.read_filename('TestFile.txt')
        ed.delete_num("")
        ed.insert_num_strings("1", ToListADT(ListADT, extra_lines))
        ed.undo()
        self.assertTrue(equal_lines(ed, []))
        ed.undo()
        self.assertTrue(equal_lines(ed, test_content))
        with self.assertRaises(Exception, msg = "Undoing past the beginning of history should have failed."):
            ed.undo()

if __name__ == '__main__':
  unittest.main()
