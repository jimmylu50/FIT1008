    .data
size_prompt:	.asciiz "Enter list size: "
element_prompt:	.asciiz "Enter element "
min_str:	.asciiz "The minimum element in this list is "
colon_str:	.asciiz ": "
newline_str:	.asciiz "\n"
size:		.word 0
the_list:	.word 0
i:		.word 0
min:		.word 0
item:		.word 0

    .text
    	j test #added so the test harness would work
    	
main:  	#getting size input, allocating space for the_list in heap,
	la $a0, size_prompt #print line from .data
    	addi $v0, $0, 4 #print function 
    	syscall #syscall
    
    	addi $v0, $0, 5 #ask for user integer input
    	syscall #syscall
    	sw $v0, size #store the integer as new 'size' value in .data 

    	addi $v0, $0, 9 #allocate space 
    	lw $t0, size #get the size of list
    	addi $t1, $0, 4 #make a register with value of 4
   	mult $t0, $t1 #multiply them
    	mflo $t1 #move to t1 register
    	addi $a0, $t1, 4 #add a 4 on top of that, so the entire space required
    	syscall #space required is 4*size+4
    	sw $v0, the_list #store the list at this address
    	sw $t0, ($v0) #store the size in the first element of address
    
    	sw $0, i #make i to be 0 (to make sure it is 0, not something else)
    	
enter_elements:	#enter elements for each i elements
	lw $t0, i #load i
	lw $t1, size #size
	slt $t0, $t0, $t1 #check if i is smaller than size
	beq $t0, $0, compute_min #if so then go to compute_min function
	
	lw $t0, i #i
	lw $t1, the_list #the_list
	addi $t2, $0, 4 #t2 = 4
	mult $t0, $t2 #4*i
	mflo $t0 #4*i = t0
	add $t0, $t0, $t1 #the_list[4*i]
	
	la $a0, element_prompt #call from global variable
	addi $v0, $0, 4 #print line
	syscall #syscall
	
	lw $a0, i #load i
	addi $v0, $0, 1 #print integer
	syscall #syscall
	
    	la $a0, colon_str #print characters from .data
   	addi $v0, $0, 4 #print line
   	syscall #syscall
   	
	addi $v0 $0, 5 #allow for user input
	syscall #syscall
	sw $v0, 4($t0) #store into the_list[4*i+4]
	
	lw $t0, i #i
	addi $t0, $t0, 1 #i += 1
	sw $t0, i #store i
	
	j enter_elements #loop enter_elements for the size of list
	
compute_min:  #check if size is greater than 0, then set first element
		#of the_list as min
	lw $t0, size #size
	lw $t1, i #i
	slt $t2, $t1, $t0 #check if i is smaller than size
	beq $t2, $0, exit #if yes exit the program
	
	lw $t0, the_list #the_list
	lw $t1, 4($t0) #load the_list[0] into t1
	sw $t1, min #store into min
	
	addi $t3, $0, 1 #make t3 to be 1
	sw $t3, i #store i as 1
	j check_for_min #jump to next function (optional)
	
check_for_min: #loop i through 1 to size and set ith element in list 
		#as item, check if min is greater than item, if yes,
		#min = item
	lw $t0, i #i
	lw $t1, size #size
	slt $t1, $t0, $t1 #check if i is smaller than size
	beq $t1, $0, print 
			
	lw $t0, i #i
	lw $t1, the_list #the_list
	addi $t2, $0, 4 #t2 = 4
	mult $t0, $t2 #4*i
	mflo $t0 #t0 = 4*i
	add $t0, $t0, $t1 #the_list[4*i]
	lw $t2, 4($t0) #load the_list[4*i+4]
	sw $t2, item #store value as item
		
	lw $t0, min #min
    	lw $t1, item #item
    	slt $t2, $t1, $t0 #check if item is smaller than min
    	beq $t2, $0, no_swap #if yes continue, if not go to no_swap
    	
    	lw $t1, item #load item value
    	sw $t1, min #store into min value
		
no_swap: #if min is not greater than item, i increase by 1
	lw $t0, i #load i
	addi $t0, $t0, 1 #add i by 1
	sw $t0, i #store i
		
	j check_for_min #loop check_for_min
	
print:	#print min
	la $a0, min_str #load string from .data
	addi $v0, $0, 4 #print string
	syscall #syscall
	
	lw $a0, min #load word from .data
	addi $v0, $0, 1 #print integer
	syscall #syscall
	
	la $a0, newline_str #load string from .data
	addi $v0, $0, 4 #print string
	syscall #syscall
	
	sw $0, i #store i as 0
	sw $0, min #store min as 0
	sw $0, item #store item as 0
	sw $0, size #store size as 0 (all for multiple testing)
	sw $0, the_list #store the_list as 0 (not required when there is only one go)
	
	jr $ra #jump return
test:   
    # the_list = [2,4,-1] 
    # Allocate the required bytes on the heap via syscall and put the address in the_list
    addi $a0, $0, 16   # 3 elements plus size = 16 bytes
    addi $v0, $0, 9    # allocate the bytes
    syscall
    sw $v0, the_list   # put start address in the_list
    # set global variable size to 3
    addi $t0, $0, 3    # $t0 = 3
    sw $t0, ($v0)      # start of the_list has correct size (3)
    sw $t0, size       # set the global variable size to the correct value so that the rest works
    # write the value of the elements 2, 4, -1
    addi $t0, $0, 2    # $t0 = 2
    sw $t0, 4($v0)     # the_list[0] = 2
    addi $t0, $0, 4    # $t0 = 4
    sw $t0, 8($v0)     # the_list[1] = 4
    addi $t0, $0, -1   # $t0 = -1
    sw $t0, 12($v0)    # the_list[2] = -1

    # go to compute the minimum of the_list = [2,4,-1] and come back
    jal compute_min    # should print -1

    # the_list = [2] 
    # Allocate the required bytes on the heap via syscall and put the address in the_list
    addi $a0, $0, 8    # 1 elements plus size = 8 bytes
    addi $v0, $0, 9    # allocate the bytes
    syscall
    sw $v0, the_list   # put start address in the_list
    # set global variable size to 1
    addi $t0, $0, 1    # $t0 = 1
    sw $t0, ($v0)      # start of the_list has correct size (1)
    sw $t0, size       # set the global variable size to the correct value so that the rest works
    # write the value of the element 2
    addi $t0, $0, 2    # $t0 = 2
    sw $t0, 4($v0)     # the_list[0] = 2
    
    # go to compute the minimum of the_list = [2] and come back
    jal compute_min  # should print 2
    
    # the_list = [0,5] 
    # Allocate the required bytes on the heap via syscall and put the address in the_list
    addi $a0, $0, 12   # 2 elements plus size = 12 bytes
    addi $v0, $0, 9    # allocate the bytes
    syscall
    sw $v0, the_list   # put start address in the_list
    # set global variable size to 2
    addi $t0, $0, 2    # $t0 = 2
    sw $t0, ($v0)      # start of the_list has correct size (2)
    sw $t0, size       # set the global variable size to the correct value so that the rest works
    # write the value of the elements  0,5
    sw $0, 4($v0)      # the_list[0] = 0
    addi $t0, $0, 5    # $t0 = 5
    sw $t0, 8($v0)     # the_list[1] = 5

    # go to compute the minimum of the_list = [0,5] and come back
    jal compute_min   # should print 0

    # the_list = [] 
    # Allocate the required bytes on the heap via syscall and put the address in the_list
    addi $a0, $0, 4    # 0 elements plus size = 4 bytes 
    addi $v0, $0, 9    # allocate the bytes
    syscall
    sw $v0, the_list   # put start address in the_list
    # set global variable size to 0
    sw $0, ($v0)       # start of the_list has correct size (0)
    sw $0, size        # set the global variable size to the correct value so that the rest works
    
    # go to compute the minimum of the_list = [] and come back
    jal compute_min   # should print nothing
    # Exit the program 
    
exit:   addi $v0, $0, 10
    	syscall
    

