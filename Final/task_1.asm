.data
	x: .word 4
	y: .word 5
	result: .word 0
	print_line: .asciiz "result is: "
	new_line: .asciiz "\n"
	
    .text

test:
    # test x = 11, y = 50, result should be 4 (y//x) as x>0, x<=y
    addi $t0, $0, 11   # $t0 = 11
    sw $t0, x          # x = 11
    addi $t0, $0, 50   # $t0 = 50
    sw $t0, y          # y = 50
    jal if              # execute the if and come back
    
    # test x = -1, y = -1, result should be 1 (x*y) as not x>0, x==y
    addi $t0, $0, -1   # $t0 = -1
    sw $t0, x          # x = -1
    sw $t0, y          # y = -1
    jal if              # execute the if and come back
    
    # test x = 20, y = 13, result should be 6 (y//2) as x>0 but not x<=y, not x==y, not y<0
    addi $t0, $0, 20   # $t0 = 20
    sw $t0, x          # x = 20
    addi $t0, $0, 13   # $t0 = 13
    sw $t0, y          # y = 13
    jal if             # execute the if and come back

    j exit             # finish the program
    
if: 	#first part of if statement
	lw $t0, x #x
	slt $t1, $0, $t0 #check if 0 is smaller than x
	bne $t1, $0, and_if #if yes, go to go_and
	
elif:	#first part of elif statement
	lw $t0, x #x
	lw $t1, y #y
	bne $t0, $t1, elif_2 #if yes, go to second elif
	
result_2: #result for the second statement
	lw $t0, x #x
	lw $t1, y #y
	mult $t0, $t1 #multiplying x and y
	mflo $t0 #move value to t0
	sw $t0, result #set value of t0 as result
	
	la $a0, print_line #load string from .data
	addi $v0, $0, 4 #print string 
	syscall #syscall
		
	lw $a0, result #load integer from .data
	addi $v0, $0, 1 #print integer
	syscall #syscall
	
	la $a0, new_line #load string from .data
	addi $v0, $0, 4 #print string 
	syscall #syscall
	
	j end #jump to end
	
elif_2:	#second part of elif statement
	lw $t0, y #y
	slt $t0, $t0, $0 #check if y is smaller than 0
	beq $t0, $0, else #if not go to else
	
	j result_2 #jump to result_2
	
and_if:  #second 'and' part for the first if statement
	lw $t0, x #x
	lw $t1, y #y
	slt $t2, $t1, $t0 #check if y is smaller than x
	bne $t2, $0, elif #if yes, go to elif, if not continue
	
	lw $t0, x #x
	lw $t1, y #y
	div $t1, $t0 #x//y
	mflo $t0 #move quotient to t0
	sw $t0, result #store value of t0 to result in .data
	
	la $a0, print_line #load string from .data
	addi $v0, $0, 4 #print string
	syscall #syscall
	
	lw $a0, result #load word from .data
	addi $v0, $0, 1 #print integer
	syscall #syscall
	
	la $a0, new_line #load string from .data
	addi $v0, $0, 4 #print string 
	syscall #syscall
	
	j end #jump to end
		
else: 	#else statement as the third statement
	lw $t0, y #y
	addi $t1, $0, 2 #set value of t1 to be 2
	div $t0, $t1 #y//2
	mflo $t0 #move the calculated value to t0
	sw $t0, result #store value of t0 to result in .data
		
	la $a0, print_line #load string from .data
	addi $v0, $0, 4 #print string
	syscall #syscall
	
	lw $a0, result #load word from .data
	addi $v0, $0, 1 #print integer
	syscall #syscall
	
	la $a0, new_line #load string from .data
	addi $v0, $0, 4 #print string 
	syscall #syscall
	
	j end #jump to end

end:	#only added for testing
	jr $ra #jump return to link

exit:	
	addi $v0, $0, 10 #exit program
	syscall #syscall
