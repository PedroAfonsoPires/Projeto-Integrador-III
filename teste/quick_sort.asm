add $t2, $t1, 5
sub $t5, $t4, $t1
sw $t0, 0($sp)
BEQ $t0, $zero, L1
sw $t1, 4($sp)
add $t1, $t4, $t7
sw $t2, 8($sp)
jump L2
L1:
sw $t3, 12($sp)
sw $t4, 16($sp)
sw $t5, 20($sp)
add $t3, $t4, $t5
sw $t6, 24($sp)
L2: