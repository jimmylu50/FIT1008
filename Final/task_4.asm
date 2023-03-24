# Author: Maria Garcia de la Banda
# Nine global variables: 3 strings for printing (newline_str, correct, incorrect),
#      3 for the different test cases, and 3 for the expected results
# Aim: Test harness for Task 4 (bubble sort) in Interview prac 1
#      It uses 3 test cases:
#      [4,3,2,1]: should be left as [1,2,3,4]
#      [3,3,1]: should be left as [1,3,3]
#      []: should be left as is
    .data
newline_str:	.asciiz "\n"
correct:	.asciiz "sorted list is correct"
incorrect:	.asciiz "sorted list is incorrect"
test_list1:     .word 4,4,3,2,1
correct_list1:  .word 4,1,2,3,4
test_list2:     .word 3,3,3,1
correct_list2:  .word 3,1,3,3
test_list3:     .word 0
correct_list3:  .word 0
n: 		.word 0
counter_1 : 	.word 1
counter_2 : 	.word 1
item: 		.word 0
item_to_right: 	.word 0
    .text
test:
	# Call bubble_sort(the_list1)
    addi $sp, $sp, -4 # make space for 1 argument
    la $t0, test_list1# $t0 = test_list1
    sw $t0, 0($sp)    # arg 1
    jal bubble_sort   # call
    addi $sp, $sp, 4  # remove the argument

    # determine if correct (correct_list1)
    la $t0, test_list1    # load address of test_list1
    la $t1, correct_list1 # load address of correct_list1
    jal determine_if_correct # determine if correct sorting or not

    # Call bubble_sort(the_list2)
    addi $sp, $sp, -4 # make space for 1 argument
    la $t0, test_list2# $t0 = test_list2
    sw $t0, 0($sp)    # arg 1
    jal bubble_sort   # call
    addi $sp, $sp, 4  # remove the argument

    # determine if correct (correct_list2)
    la $t0, test_list2     # load address of test_list2
    la $t1, correct_list2  # load address of correct_list2
    jal determine_if_correct # determine if correct sorting or not

    # Call bubble_sort(the_list3)
    addi $sp, $sp, -4 # make space for 1 argument
    la $t0, test_list3# $t0 = test_list3
    sw $t0, 0($sp)    # arg 1
    jal bubble_sort   # call
    addi $sp, $sp, 4  # remove the argument

    # determine if correct (correct_list3)
    la $t0, test_list3    # load address of test_list3
    la $t1, correct_list3 # load address of correct_list3
    jal determine_if_correct # determine if correct sorting or not

    # Exit the program
    addi $v0, $0, 10  # $v0 = 10 for exiting the program
    syscall           

determine_if_correct: #address of one list in $t0, the other in $t1
    lw $t2, ($t0) # load the size of the test list 
    lw $t3, ($t1) # load the size of the expected list
    bne $t2, $t3, is_incorrect # if size of array is different go to incorrect
 
loop:    
    beq $t2, $0, is_correct # if all elements compared, go to correct
   
    addi $t0,$t0,4 # compute address of next test_list element
    addi $t1,$t1,4 # compute address of next correct_list element
    lw $t3, ($t0)  # load test_list[i]
    lw $t4, ($t1)  # load correct_list[i]
    bne $t3, $t4, is_incorrect # if elements are different go to incorrect

    addi $t2, $t2, -1 # decrement loop index
    
    j loop

is_correct:    
   la $a0, correct  # $a0 = string that indicates sorting  is correct
   addi $v0, $0, 4  # $v0 = 4 to print the string already loaded in $a0
   syscall 
   # print "\n"
   la $a0, newline_str  # $a0 = newline to print a new line (could have added it to the string, but I might have wanted to print where it fails)
   syscall
   jr $ra            # go back to caller
is_incorrect:    
   la $a0, incorrect  # $a0 = string that indicates sorting is incorrect
   addi $v0, $0, 4  # $v0 = 4 to print the string already loaded in $a0
   syscall 
   # print "\n"
   la $a0, newline_str  # $a0 = newline to print a new line (could have added it to the string, but I might have wanted to print where it fails)
   syscall
   jr $ra            # go back to caller

	
bubble_sort:	#bubble_sort acts as the main function
		lw $a0, 0($sp) #load address of the_list
		lw $t0, 0($a0) #load first element of list (size of list)
		sw $t0, n #load the value into n
		
		addi $t1, $0, 1 #set t1 value to 1
		sw $t1, counter_1 #store 1 to counter_1
		
		j for_loop_1 #jump to next function (optional)
		
for_loop_1:	#allows first loop to occur from 0 to n-1
		lw $t0, counter_1 #counter_1
		lw $t1, n #n
		slt $t2, $t0, $t1 #check if counter_1 is smaller than n
		beq $t2, $0, exit #if not go to exit
		
		lw $t0, counter_1 #looad counter_1
		addi $t0, $t0, 1 #add 1 to counter_1
		sw $t0, counter_1 #store counter_1
		
		addi $t1, $0, 1 #set t1 value to 1
		sw $t1, counter_2 #store 1 to counter_2
		
		j for_loop_2 #jump to next function in line
		
for_loop_2:	#allows second loop to occur from 0 to n-1
		lw $t0, counter_2 #counter_2
		lw $t1, n #n
		slt $t2, $t0, $t1 #check if counter_2 is smaller than n
		beq $t2, $0, for_loop_1 #if not go to for_loop_1
		
		lw $t0, counter_2 #counter_2
		addi $t1, $0, 4 #set t1 value to 4
		mult $t1, $t0 #multiply counter_2 by 4
		mflo $t2 #move the calculated value to t2
		lw $a0, 0($sp) #load address of the_list
		add $t4, $t2, $a0 #the_list[4*i]
		#since counter_2 starts at 1 ->
		lw $t0, 0($t4) #load the_list[4*counter_2] = [4] -> 
		#increases as the loop continues
		lw $t1, 4($t4) #load the_list[4*counter_2+4] = [8] -> 
		#increases as the loop continues
		sw $t0, item #store value of t0 to item
		sw $t1, item_to_right #store value of t1 to item_to_right
		
		lw $t0, item #item
		lw $t1, item_to_right #item_to_right
		slt $t2, $t1, $t0 #check if item_to_right is smaller than item
		beq $t2, $0, counter_incre #if not, go to continue
		
		lw $a0, ($sp) #load address of the list
		lw $t0, item #item
		lw $t1, item_to_right #item_to_right
		lw $t2, counter_2 #counter_2
		addi $t3, $0, 4 #set value of t3 to be 4
		mult $t3, $t2 #4*counter_2
		mflo $t4 #move calculated value to t4
		add $t6, $t4, $a0 #the_list[4*counter_2]
		#since counter_2 starts at 1 ->
		sw $t1, 0($t6) #store item_to_right into the_list[4*counter_2]
		# = [4] -> increases as the loop continues
		sw $t0, 4($t6) #store item into the_list[4*counter_2+4]
		# = [8] -> increases as the loop continues
		
counter_incre:	#counter_increment for counter_2
		lw $t0, counter_2 #counter_2
		addi $t0, $t0, 1 #add 1 to counter_2
		sw $t0, counter_2 #store value of t0 to counter_2
		
		j for_loop_2 #loop through for_loop_2
		
exit:		jr $ra #jump return to the address (only for testing)
	
		addi $v0, $0, 10 #exit program
		syscall #syscall
