#!/usr/bin/env python3
from sys import exit
import sys
import math

# output and input file variable
OUTPUT_FILE = "output.txt"
INPUT_FILE = ""

# GLOBAL VARIABLES
MAX = 0
OBJECT_NUMBER = 0
TOTAL_PROFIT = 0
KNAPSACK_LIST = []
INPUT_LIST = []

def insertionSort(arr): 
  
    # Traverse through 1 to len(arr) 
    for i in range(1, len(arr)): 
  
        temp_tuple = arr[i]
        key = arr[i][0] 
  
        # Move elements of arr[0..i-1], that are 
        # greater than key, to one position ahead 
        # of their current position 
        j = i-1
        while j >=0 and arr[j][0] < key : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = temp_tuple 

def knapsack(list):
    w = 0
    for i in range(0,len(list)) :
        if w + list[i][2] <= MAX :
            temp_tuple = (list[i][1], list[i][2])
            KNAPSACK_LIST.append(temp_tuple)
            w = w + list[i][2]

if __name__ == "__main__":

    # control number of command line input
    if len(sys.argv) > 2:
        print("You write wrong input. Please try again")
    else:
        INPUT_FILE = sys.argv[1]

    with open(INPUT_FILE) as file:
        temp1, temp2 = file.readline().strip().split("\t")
        MAX = int(temp2)
        for line in file:
            pi,vi = line.strip().split("\t")
            pair_tuple = (int(pi)/int(vi), int(pi),int(vi))
            INPUT_LIST.append(pair_tuple)

    insertionSort(INPUT_LIST) 
    knapsack(INPUT_LIST)
    for i in range(0,len(KNAPSACK_LIST)):
        TOTAL_PROFIT += KNAPSACK_LIST[i][0]
    
    f = open(OUTPUT_FILE, "w")
    f.write("{}: {}\n".format("TOTAL PROFIT", TOTAL_PROFIT))
    f.write("{}: {}".format("OBJECTS", KNAPSACK_LIST))
