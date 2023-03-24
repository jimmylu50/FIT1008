    .data
size_prompt:	.asciiz "Enter list size: "
element_prompt:	.asciiz "Enter element "
min_str:	.asciiz "The minimum element in this list is "
colon_str:	.asciiz ": "
newline_str:	.asciiz "\n"
correct:	.asciiz "Minimum is correct"
incorrect:	.asciiz "Minimum is incorrect"
test_list1: .word 4,1,2,-5,5
    .text
test:

    # the_list = test_list1 = [1,2,-5,5] 
    # go to compute the minimum of the_list = test_list1 and come back
    # Call get_minimum(the_list)
    addi $sp, $sp, -4 # make space for 1 argument
    la $t0, test_list1# $t0 = test_list1
    sw $t0, 0($sp)    # arg 1
    jal get_minimum   # call
    addi $sp, $sp, 4  # remove the argument

    # determine if correct (==-5)
    addi $t0, $0, -5  # $t0 = expected get_minimum value (-5)
    jal determine_if_correct 

    # the_list = [2,4,-1] 
    # Allocate the required bytes on the heap via syscall and put the address in the_list
    addi $a0, $t0, 16  # 3 elements plus size = 16 bytes
    addi $v0, $0, 9    # allocate the bytes
    syscall
    sw $v0, -4($fp)   # put start address in the_list
    # set global variable size to 3
    addi $t0, $0, 3    # $t0 = 3
    sw $t0, ($v0)      # start of the_list has correct size (3)
    # write the value of the elements 2, 4, -1
    addi $t0, $0, 2    # $t0 = 2
    sw $t0, 4($v0)     # the_list[0] = 2
    addi $t0, $0, 4    # $t0 = 4
    sw $t0, 8($v0)     # the_list[1] = 4
    addi $t0, $0, -1   # $t0 = -1
    sw $t0, 12($v0)    # the_list[2] = -1

    # go to compute the minimum of the_list = [2,4,-1] and come back
    # Call get_minimum(the_list)
    addi $sp, $sp, -4 # make space for 1 argument
    lw $t0, -4($fp)   # $t0 = the_list
    sw $t0, 0($sp)    # arg 1
    jal get_minimum   # call
    addi $sp, $sp, 4  # remove the argument

    # determine if correct (== -1)
    addi $t0, $0, -1  # $t0 = expected get_minimum value (-1)
    jal determine_if_correct
   
    # the_list = [] 
    # Allocate the required bytes on the heap via syscall and put the address in the_list
    addi $a0, $t0, 4   # 0 elements plus size = 4 bytes 
    addi $v0, $0, 9    # allocate the bytes
    syscall
    sw $v0, -4($fp)   # put start address in the_list
    # set global variable size to 0
    sw $0, ($v0)       # start of the_list has correct size (0)
    
    # go to compute the minimum of the_list = [] and come back
    # Call get_minimum(the_list)
    addi $sp, $sp, -4 # make space for 1 argument
    lw $t0, -4($fp)   # $t0 = the_list
    sw $t0, 0($sp)    # arg 1
    jal get_minimum   # call
    addi $sp, $sp, 4  # remove the argument

    # determine if correct (== 0)
    addi $t0, $0, 0   # $t0 = expected get_minimum value (0)
    jal determine_if_correct

    # call students main (which will exit)
    jal main

    # Exit the program (in case something goes wrong and exit does not finish
    addi $v0, $0, 10  # $v0 = 10 for exiting the program
    syscall           

# private leaf function, no need for 
determine_if_correct:   
    bne $t0, $v0, else   # if the expected result (in $t0) is not equal to get_minimum, go to else
        la $a0, correct  # $a0 = string that indicates get_minimum is correct
        j endif
    else:
        la $a0, incorrect # else, $a0 = string that indicates get_minimum is incorrect
    endif:
    addi $v0, $0, 4       # $v0 = 4 to print the string already loaded in $a0
    syscall 
    # print "\n"
    la $a0, newline_str   # $a0 = newline to print a new line (could have added it to the strin, but I might have wanted to print get_minimum)
    syscall
    jr $ra                # go back to caller

    

main:		#main 	
		jal read_list #jump and link to read_list
		
		addi $sp, $sp, -4 #push sp up by 1 spot in stack
		addi $fp, $sp, 0 #set fp to be sp
		sw $v0, 0($fp) #save the_list from read_list into 0($sp)
		
		jal get_minimum #jump and link to get_minimum
		
		addi $sp, $sp, -4 #push sp up by 1 spot in stack
		addi $fp, $sp, 0 #set fp to be sp
		sw $v0, 0($fp) #store return value of get_minimum into first stack pointer
		
		la $a0, min_str #load string from .data
		addi $v0, $0, 4 #print string
		syscall #syscall
		
		lw $a0, ($fp) #load value from first stack pointer
		addi $v0, $0, 1 #print integer
		syscall #syscall
		
		addi $sp, $sp, 8 #remove locals
		j exit #exit
		
read_list:	#read size of list and allocate size, also allow for user input
		addi $sp, $sp, -8 #push sp up by 2 spots in stack
		sw $ra, 4($sp) #save ra from jump link
		sw $fp, 0($sp) #save fp from previous address
		
		addi $fp, $sp, 0 #set new fp to be the same as sp
		
		addi $sp, $sp, -12 #allocating local variables
		
		sw $0, -12($fp) #i
		sw $0, -8($fp) #n
		sw $0, -4($fp) #the_list
		
		la $a0, size_prompt #load string from .data
    		addi $v0, $0, 4 #print string 
    		syscall #syscall
    
    		addi $v0, $0, 5 #ask for user integer input
    		syscall #syscall
    		sw $v0, -8($fp) #store the integer as new 'size' value in .data 
		
    		addi $v0, $0, 9 #allocate space 
    		lw $t0, -8($fp) #get the size of list
    		addi $t1, $0, 4 #make a register with value of 4
   		mult $t0, $t1 #multiply them
    		mflo $t1 #move to t1 register
    		addi $a0, $t1, 4 #add a 4 on top of that, so the entire space required
    		syscall #space required is 4*size+4
    		sw $v0, -4($fp) #store the list at this address
    		sw $t0, ($v0) #store the size in the first element of address
		
enter_elements:	#allow users to enter elements
		lw $t0, -12($fp) #i
		lw $t1, -8($fp) #n
		slt $t0, $t0, $t1 #check if i is smaller than size
		beq $t0, $0, return_1 #if not then go to next label
	
		la $a0, element_prompt #load string from .data
		addi $v0, $0, 4 #print string
		syscall #syscall
	
		lw $a0, -12($fp) #i
		addi $v0, $0, 1 #print integer value of i
		syscall #syscall
	
    		la $a0, colon_str #load string from .data
   		addi $v0, $0, 4 #print string
   		syscall #syscall
   		
   		lw $t0, -12($fp) #i
   		lw $t1, -4($fp) #the_list
   		addi $t2, $0, 4 #set t2 as 4
		mult $t0, $t2 #4*i
		mflo $t0 #move to t0
		add $t0, $t0, $t2 #4*i+4
		add $t0, $t0, $t1 #the_list[4*i+4]
		addi $v0 $0, 5 #ask for user input
		syscall #syscall
		sw $v0, ($t0) #store element of list in the_list
	
		lw $t0, -12($fp) #i
		addi $t0, $t0, 1 #add i by 1
		sw $t0, -12($fp) #store i
	
		j enter_elements #loop enter_elements for number of size
		
return_1:	#return the_list
		lw $v0, -4($fp) #load the_list into v0 as return value

		addi $sp, $sp, 12 #deallocate local variables
		lw $fp, 0($sp) #load fp
		lw $ra, 4($sp) #load ra
		addi $sp, $sp, 8 #deallocate fp and ra
		
		addi $fp, $sp, 0 #set fp to current sp
		
		jr $ra #jump return to jal link saved earlier

get_minimum:	#get minimum value of the_list
		addi $sp, $sp, -8 #allocate space for ra and fp
		sw $ra, 4($sp) #store ra
		sw $fp, 0($sp) #store fp
		
		addi $fp, $sp, 0 #set fp to current sp
		
		addi $sp, $sp, -20 #allocate space for local variables
		
		sw $0, -20($fp) #0
		sw $0, -16($fp) #min
		sw $0, -12($fp) #size
		sw $0, -8($fp) #i
		sw $0, -4($fp) #item
		
		lw $a0, 8($fp) #load address of list
		lw $t0, ($a0) #load size into t0 (since first element of list is size)
		sw $t0, -12($fp) #store this into a local variable
		
if:		#check if size is greater than 0, then set the first element
		#of the_list to min
		lw $t0, -12($fp) #size
		lw $t1, -20($fp) #0
		slt $t0, $t1, $t0 #check if size is greater than 0
		beq $t0, $0, else_0 #if not go to else_0
		
		lw $a0, 8($fp) #address of list
		lw $t0, 4($a0) #getting the second value of the list, list[0]
		sw $t0, -16($fp) #storing the first value of list into min
		
		addi $t0, $0, 1 #set t0 as 1
		sw $t0, -8($fp) #store t0 as i
		
		j check_for_min
		
check_for_min:	#loop from 1 to n (n-1 times) and sets the element i of list
		#as item, there is an if statement to check if min is greater
		#than item
		lw $t0, -8($fp) #load i
		lw $t1, -12($fp) #load size
		slt $t0, $t0, $t1 #check whether i is smaller than size
		beq $t0, $0, return_2 #if not go to return_2
		
		lw $a0, 8($fp) #load address of list
		lw $t0, ($a0) #load size into t0
		lw $t1, -8($fp) #load i
		addi $t2, $0, 4 #put 4 as value of t2
		mult $t1, $t2 #4*i
		mflo $t3 #move to t3
		add $t4, $t3, $a0 #list[4*i]
		lw $t0, 4($t4) #load list[4*i+4]
		sw $t0, -4($fp) #store the value into item
		
		lw $t0, -16($fp) #load min
		lw $t1, -4($fp) #load item
		slt $t0, $t1, $t0 #check if item is smaller than min
		beq $t0, $0, i_increment #if not go to i_increment
		
		lw $t1, -4($fp) #load item
		sw $t1, -16($fp) #store item into min
		
		j i_increment #jump to next function (optional)
		
i_increment:	#increase i by 1
		lw $t0, -8($fp) #load i
		addi $t0, $t0, 1 #increment i by 1
		sw $t0, -8($fp) #store i
		
		j check_for_min #loop check_for_min
		
return_2:	#return minimum value of the_list
		lw $v0, -16($fp) #load min in v0

		addi $sp, $sp, 20 #deallocate local variables
		lw $fp, 0($sp) #load fp
		lw $ra, 4($sp) #load ra
		addi $sp, $sp, 8 #deallocate fp and ra
		
		jr $ra	#jump back to ra address	
		
else_0:		#returns 0 when the size is not greater than 0
		sw $0, -8($fp) #store 0 as i
		lw $v0, -8($fp) #load v0 as 0

		addi $sp, $sp, 20 #deallocate local variables
		lw $fp, 0($sp) #load fp
		lw $ra, 4($sp) #load ra
		addi $sp, $sp, 8 #deallocate fp and ra
		
		jr $ra	#jump back to ra address	
			
exit:
   		addi $v0, $0, 10 #exit program
    		syscall #syscall
