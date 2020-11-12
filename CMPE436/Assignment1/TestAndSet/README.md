# CmpE 436 ASSIGNMENT 1

## STARVATION AT TEST_AND_SET

### Usage

`$ java -jar TestAndSet.jar`

### Properties

1. Mutual Exclusion
- Assume both P0 and P1 are in critical section. 
- P0 is in CS && P1 is in CS 
- This satisfies only when two process pass (lockFlag.testAndSet(1) != 1)  
- It is cannot be true since lockFlag.testAndSet(1) cannot have two values, if one can get 1, other can get 0. Contradiction

2. Progress 
- Assume it is violated. Then both processes are stuck. That is,
- while(lock == 0) and while(lock == 1) true
- This is not possible since lock cannot have two values. Contradiction

3. Starvation
- P1 is blocked only if P0 repeatedly enters the critical section, that is,
- while(lock == 1) is always true.
- But when P0 release CS, it sets lock 1. So, it cannot re-enter CS. Hence, processes are forced to take turns if they both want to enter critical sections.

