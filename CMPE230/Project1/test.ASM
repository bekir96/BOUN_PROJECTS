


; @aouthor : Bekir Yıldırım_2014400054,  Alkım Ece Toprak_2017400294



				;initializing variables
mov bx ,00			
mov cx , 0000h			;input number (at most 2 bytes)
var1 dw 0000h

digitLoop:
	
	mov ah, 01h
	int 21h
	
	cmp al, 20h		;compare the input character's ASCII code to the ASCII code of "Space"
	jz stackPush	
	
	;operations 

	cmp al, 2Bh		;compare the input character's ASCII code to the ASCII code of "+"
	jz addition		;if same, jump to the corresponding operation label
	
	cmp al, 7Ch		;compare the input character's ASCII code to the ASCII code of "|"
	jz orIng
	
	cmp al, 5Eh		;compare the input character's ASCII code to the ASCII code of "^" 
	jz xorIng
	
	cmp al, 26h		;compare the input character's ASCII code to the ASCII code of "&"
	jz andIng
	
	cmp al, 2Fh		;compare the input character's ASCII code to the ASCII code of "/"
	jz divisionXL
	
	cmp al, 2Ah		;compare the input character's ASCII code to the ASCII code of "*"
	jz multiplicationXL
	
	cmp al, 0Dh		;compare the input character's ASCII code to the ASCII code of "enter"
	jz exitXL		;if same, jump to the exit label
	
	jmp digitLetter		;else, the input character is a letter or a number
	
stackPush: 			

	PUSH cx			;pushes the latest number "cx" to the stack 
	mov cx, 0000h		;and re-initializes the variable "cx" for later use
	jmp digitLoop
	
digitLetter:

	cmp al, 40h		;if the input character is a number
	jle arrangeDigit	;jump to arrangeDigit

	cmp al, 41h		;if the input character is a letter
	jge arrangeLetter	;jump to arrangeLetter
	
arrangeDigit:

	sub al, 48		;subtract 48 from the ASCII code of the number to get its real value
	jmp readInput

divisionXL:

	jmp division

multiplicationXL:

	jmp multiplication

exitXL:

	jmp exit

arrangeLetter:

	sub al, 55		;subtract 55 from the ASCII code of the letter to get its real value 
	jmp readInput
	
readInput:			;(if the number has more than 1 digit, current number is multiplied with 16 and the new digit is added)
	
	mov bl, al		;bl stores the input character
	mov bh, 00h	
	mov ah, 00		;ax stores 10h (16 in decimal)
	mov ax, 10h		
	mul cx			;ax=cx*10h 
	mov cx, ax		;cx becomes ax
	add cx, bx		;cx=cx+bx
	
	jmp digitLoop 
	
addition:			;if the "+" sign is seen, last two elements of the stack are added and stored in cx
	
	POP cx
	POP bx
	add cx, bx
	mov bx, 0000h

	jmp digitLoop

	
orIng:				;if the "|" sign is seen, bitwise or of the last two elements of the stack is stored in cx

	POP ax
	POP cx
	or ax, cx
	mov cx,ax
	mov ax, 0000h
	
	jmp digitLoop

xorIng:				;if the "^" sign is seen, bitwise xor of the last two elements of the stack is stored in cx

	POP ax
	POP cx
	xor ax, cx
	mov cx,ax
	mov ax, 0000h
	
	jmp digitLoop

andIng:				;if the "&" sign is seen, bitwise and of the last two elements of the stack is stored in cx
	
	POP ax
	POP cx
	and ax, cx
	mov cx,ax
	mov ax, 0000h
	
	jmp digitLoop
	
	
division:			;if the "/" sign is seen, last two elements of the stack are divided and stored in cx

	mov ax, 0000h
	mov dx, 0000h
	mov bx, 0000h
	POP bx
	POP ax
	div bx			;divide dx:ax by bx. result in ax
	mov cx, ax		;result is stored in cx
	mov ax, 0000h
	mov dx, 0000h
	
	jmp digitLoop
	
multiplication:			;if the "*" sign is seen, last two elements of the stack are multiplied and stored in cx
	
	POP cx
	POP bx
	mov ax, bx
	mul cx
	mov cx, ax
	mov ax, 0000h
	mov bx, 0000h
	
	jmp digitLoop

exit:				;the latest result calculated before the "enter" input is copied to ax

	mov ax, cx		
	PUSH cx			;and pushed to the stack 
	mov cx, 0001h		
				;stack now contains the final result only
	
exitLoop:
	
	mov bx, 10h
	div bx			;the answer (ax) is divided to 16 and the last digit (remainder of the division) is stored in dx
	mov dx, 0000h
	cmp ax, 0000h		;if ax is not equal to 0, jump to countCX
	jnz countCX
	jmp output		;else jump to output
				;if ax is equal to 0, it means that the whole answer is printed
	
countCX:
	
	inc cx			;cx is our loop counter for exitLoop
				;when the loop ends, cx equals to the number of digits in our result
	jmp exitLoop
	
output:

	POP ax			;ax contains the final result
	mov var1, cx		;var1 contains the number of digits of the final result
	
outputLoop:

	mov bx, 10h 
	div bx 
	PUSH dx			;dx has the last digit of the answer (dx=answer%16)
    	dec cx 			;cx is decreased until all of the digits(dx) are pushed to the stack 
   	 cmp cx, 0000h		;when cx equals 0, every digit of the final result is pushed to the stack 
    	jz final			;if cx=0 jump to the "final" label
	
	jmp outputLoop 		;else if cx is not equal to 0, continue pushing digits to the stack and decreasing cx
	
final:

	mov dl, 10d		;"new line" is printed
	mov ah, 02h
	int 21h
	mov cx, var1		;counter cx contains the number of digits of the final result
	jmp final2

final2:
	
	POP dx			;dx contains the leftmost unprinted digit of the result
	cmp dx, 9		;if the digit is less than or equal to 9, it is a number
	jle arrangeOutputDigit
	cmp dx,10		;else if the digit is greater than or equal to 10, it is a letter 
	jge arrangeOutputLetter
				;since the result must be printed in hex
	
arrangeOutputDigit:
	
	add dx, 48		;number+48=ASCII code of the number
	jmp continue
	
arrangeOutputLetter:

	add dx, 55		;number+55=ASCII code of the letter
	jmp continue

continue:
	
	mov ah, 02h		;the leftmost unprinted digit of the result is now printed
	int 21h
	cmp cx, 0000h		;cx is decreased after each digit is printed
	dec cx
	jnz final2		;if cx is not equal to zero, then there are unprinted digits, jump back to the "final2" label
	
finalExit:

	mov ah, 4ch		;exit
	int 21h
	
	
























