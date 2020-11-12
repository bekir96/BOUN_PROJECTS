# CmpE 436 ASSIGNMENT 1

## MUTUAL EXCLUSION AT SWAP

### Usage

`$ java -jar SwapThread.jar`

### Properties

1. Mutual Exclusion
- Assume both P0 and P1 are in critical section. 
- P0 is in CS && P1 is in CS 
- This satisfies only when two process pass (wantCS[i]) can be true.  
- It is cannot be true since wantCS[i] cannot have two values, if one can get true, other can get false. Contradiction

2. Progress 
- Assume it is violated. Then both processes are stuck. That is,
- if(wantCS[0]) and if(wantCS[1]) true
- This is not possible since wantCS[i] cannot have true values at same. Contradiction

3. Starvation
- P1 is blocked only if P0 repeatedly enters the critical section.
- Processes have to alternate to enter the critical section, if one of them is not interested then the other is stuck.
- One process can get lock at each time so do not satisfy starvation property. 

