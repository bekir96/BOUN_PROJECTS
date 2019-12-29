# Student Name: Bekir Yildirim
# Student Number: 2014400054
# Compile Status: Compiling
# Program Status: Working
# Periodic - Checkered

from sys import exit
import sys
from time import sleep
import numpy as np
from mpi4py import MPI
import math

MATRIX_SIZE = 360

FIND_TOP = "up"
FIND_BELOW = "down"
FIND_LEFT = "left"
FIND_RIGHT = "right"

# Game of life variables
LONELINESS = 2
OVERPOPULATION = 3
REPRODUCTION = 3

# Send-recv tag variables
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
TOP_LEFT = 4
DOWN_RIGHT = 5
TOP_RIGHT = 6
DOWN_LEFT = 7

# iteration variable
ITERATION = sys.argv[1]

if len(sys.argv) > 3:
    TEST_FILE = sys.argv[3]

# output file variable
OUTPUT_FILE = 'output.txt'

comm = MPI.COMM_WORLD

# find top or below rank of current rank
def find_top_below(world_rank, sqrt_slave, world_size, control):
    return int((world_rank - sqrt_slave - 1) % world_size + 1) if control == FIND_TOP else int((world_rank + sqrt_slave - 1) % world_size + 1)

# find left or right rank of current rank
def find_left_right(world_rank, sqrt_slave, world_size, control):
    return int(int((world_rank - 1) / sqrt_slave) * sqrt_slave + (world_rank-2) % sqrt_slave + 1) if control == FIND_LEFT else int(int((world_rank - 1) / sqrt_slave) * sqrt_slave + (world_rank) % sqrt_slave + 1 )

# Send functions
def send_right(temp_array, world_rank, sqrt_slave, world_size):
    comm.send(temp_array[:, -1], dest = find_left_right(world_rank, sqrt_slave, world_size, "right"), tag=RIGHT)

def send_left(temp_array, world_rank, sqrt_slave, world_size):
    comm.send(temp_array[:,0], dest=find_left_right(world_rank, sqrt_slave, world_size, "left"), tag=LEFT)

def send_down(temp_array, world_rank, sqrt_slave, world_size):
    comm.send(temp_array[-1,:], dest=find_top_below(world_rank, sqrt_slave, world_size, "down"), tag=DOWN)

def send_up(temp_array, world_rank, sqrt_slave, world_size):
    comm.send(temp_array[0,:], dest=find_top_below(world_rank, sqrt_slave, world_size, "up"), tag=UP)

def send_top_left(temp_array, world_rank, sqrt_slave, world_size):
    comm.send(temp_array[0,0], dest = find_left_right(find_top_below(world_rank, sqrt_slave, world_size, "up"), sqrt_slave, world_size, "left"), tag=TOP_LEFT)

def send_top_right(temp_array, world_rank, sqrt_slave, world_size):
    comm.send(temp_array[0,-1], dest = find_left_right(find_top_below(world_rank, sqrt_slave, world_size, "up"), sqrt_slave, world_size, "right"), tag=TOP_RIGHT)

def send_down_left(temp_array, world_rank, sqrt_slave, world_size):
    comm.send(temp_array[-1,0], dest = find_left_right(find_top_below(world_rank, sqrt_slave, world_size, "down"), sqrt_slave, world_size, "left"), tag=DOWN_LEFT)

def send_down_right(temp_array, world_rank, sqrt_slave, world_size):
    comm.send(temp_array[-1,-1], dest = find_left_right(find_top_below(world_rank, sqrt_slave, world_size, "down"), sqrt_slave, world_size, "right"), tag=DOWN_RIGHT)

# Recv functions
def recv_top(world_rank, sqrt_slave, world_size):
    return comm.recv(source = find_top_below(world_rank, sqrt_slave, world_size, "up"), tag=DOWN)

def recv_down(world_rank, sqrt_slave, world_size):
    return comm.recv(source = find_top_below(world_rank, sqrt_slave, world_size, "down"), tag=UP)

def recv_left(world_rank, sqrt_slave, world_size):
    return comm.recv(source = find_left_right(world_rank, sqrt_slave, world_size, "left"), tag=RIGHT)

def recv_right(world_rank, sqrt_slave, world_size):
    return comm.recv(source = find_left_right(world_rank, sqrt_slave, world_size, "right"), tag=LEFT)

def recv_top_left(world_rank, sqrt_slave, world_size):
    return comm.recv(source = find_left_right(find_top_below(world_rank, sqrt_slave, world_size, "up"), sqrt_slave, world_size, "left"), tag=DOWN_RIGHT)

def recv_top_right(world_rank, sqrt_slave, world_size):
    return comm.recv(source = find_left_right(find_top_below(world_rank, sqrt_slave, world_size, "up"), sqrt_slave, world_size, "right"), tag=DOWN_LEFT)

def recv_down_left(world_rank, sqrt_slave, world_size):
    return comm.recv(source =  find_left_right(find_top_below(world_rank, sqrt_slave, world_size, "down"), sqrt_slave, world_size, "left"), tag=TOP_RIGHT)

def recv_down_right(world_rank, sqrt_slave, world_size):
    return comm.recv(source = find_left_right(find_top_below(world_rank, sqrt_slave, world_size, "down"), sqrt_slave, world_size, "right"), tag=TOP_LEFT)

# look all neighbor of cell and sum them.
def neighbor_sum_local(proc_grid,row,col):
		return proc_grid[row+1,col+1] + proc_grid[row+1,col] + proc_grid[row+1,col-1] + \
			proc_grid[row,col+1] + proc_grid[row,col-1] + \
			proc_grid[row-1,col+1] + proc_grid[row-1,col] + proc_grid[row-1,col-1]

# provide game of life algorithm with traversing array.
def update_grid(temp_grid, proc_grid):
    number_of_iterate = len(proc_grid)
    for row in range(1,number_of_iterate-1):
        for col in range(1, number_of_iterate-1):
            if proc_grid[row,col] and  neighbor_sum_local(proc_grid, row, col) > OVERPOPULATION:
                temp_grid[row,col] = 0
            elif proc_grid[row,col] and neighbor_sum_local(proc_grid, row, col) < LONELINESS:
                temp_grid[row,col] = 0
            elif neighbor_sum_local(proc_grid, row, col) == REPRODUCTION:
                temp_grid[row,col] = 1
    return temp_grid

# test output with test file
def test(input_array):
    np.savetxt(OUTPUT_FILE, input_array.astype(int), fmt = '%i')
    myResult = np.loadtxt(OUTPUT_FILE, dtype=int)
    forTest = A = np.loadtxt(TEST_FILE, dtype=int)
    if(np.array_equal(myResult, forTest)):
        print("Test case passed")

#   Main function; master, which has rank 0, reads the input file and shares them accross to slaves.
#   Then slaves do some calculations to do game of life, then slaves sends it to master process. Then master merges and prints the result to output file.
if __name__ == "__main__":

    # Initializes the MPI.
    world_size = comm.Get_size()-1
    sqrt_slave = int(math.sqrt(world_size))
    world_rank = comm.Get_rank()
    
    
    # If it is master process, reads the input from file. And shares them to slaves.
    # Then it merges results of slaves' operations. Then prints the result to the output file.
    if world_rank == 0:

        input_array = np.genfromtxt(sys.argv[2], delimiter=" ", dtype=int)  # Reads input file.
        rows_per_slave = int(MATRIX_SIZE/math.sqrt(world_size))
        rank_count = 1
        # Shares input to the slaves.
        for i in range(int(math.sqrt(world_size))):
            for j in range(int(math.sqrt(world_size))):
                comm.send(input_array[i*rows_per_slave:i*rows_per_slave+rows_per_slave,
                                      j*rows_per_slave:j*rows_per_slave+rows_per_slave], dest=rank_count, tag=0)
                rank_count += 1

        rank_count = 1

        # Receives result of slaves' operations and merges them.
        for i in range(int(math.sqrt(world_size))):
            for j in range(int(math.sqrt(world_size))):
                input_array[i*rows_per_slave:i*rows_per_slave+rows_per_slave,
                                      j*rows_per_slave:j*rows_per_slave+rows_per_slave] = comm.recv(source=rank_count, tag=rank_count)
                rank_count += 1

        # Prints the result to the output file or console.
        if len(sys.argv) > 3:
            test(input_array)
        else :
            print(input_array)

    # Slaves function; gets own matrix from master. Then does 'ITERATION' executions to do game of life
    # with communicating with other slaves. Then sends result to the master processor.
    else:
        modulus_by_2 = world_rank % 2
        modulus_by_sqrt_slave = int(world_rank/sqrt_slave) % 2
        temp_array = comm.recv(source=0, tag=0)
        length_slave_array = len(temp_array) 
        # 'proc_grid' a variable that can hold arrays sent to corners from other rankings andopen at the beginning of iteration to improve memory usage.
        proc_grid = np.zeros((length_slave_array + 2, length_slave_array + 2), dtype=int)  
        for i in range(int(ITERATION)):
            proc_grid[1:length_slave_array+1,1:length_slave_array+1] = temp_array

            # determine whether rank is even or odd.
            if modulus_by_2 == 0:
                
                # recv of even rank
                proc_grid[1:length_slave_array+1,0] = recv_left(world_rank, sqrt_slave, world_size)
                proc_grid[1:length_slave_array+1,-1] = recv_right(world_rank, sqrt_slave, world_size)
                proc_grid[0,0] = recv_top_left(world_rank, sqrt_slave, world_size)
                proc_grid[0,-1] = recv_top_right( world_rank, sqrt_slave, world_size)
                proc_grid[-1,0] = recv_down_left( world_rank, sqrt_slave, world_size)
                proc_grid[-1,-1] = recv_down_right(world_rank, sqrt_slave, world_size)

                # determine whether line of rank is even or odd.
                if modulus_by_sqrt_slave == 0:
                    send_down(temp_array, world_rank, sqrt_slave, world_size)
                    send_up(temp_array, world_rank, sqrt_slave, world_size)
                    proc_grid[0,1:length_slave_array+1] = recv_top(world_rank, sqrt_slave, world_size)
                    proc_grid[-1,1:length_slave_array+1] = recv_down(world_rank, sqrt_slave, world_size)

                else :
                    proc_grid[0,1:length_slave_array+1] = recv_top(world_rank, sqrt_slave, world_size)
                    proc_grid[-1,1:length_slave_array+1] = recv_down(world_rank, sqrt_slave, world_size)
                    send_up(temp_array, world_rank, sqrt_slave, world_size)
                    send_down(temp_array, world_rank, sqrt_slave, world_size)
                
                # send right part
                send_right(temp_array, world_rank, sqrt_slave, world_size)
                # send top left
                send_left(temp_array, world_rank, sqrt_slave, world_size)
                # send below left
                send_down_left(temp_array, world_rank, sqrt_slave, world_size)
                # send below right
                send_down_right(temp_array, world_rank, sqrt_slave, world_size)
                # send top right
                send_top_right(temp_array, world_rank, sqrt_slave, world_size)
                # send left part
                send_top_left(temp_array, world_rank, sqrt_slave, world_size)

            elif modulus_by_2 == 1:
                
                # send right part
                send_right(temp_array, world_rank, sqrt_slave, world_size)
                # send top left
                send_left(temp_array, world_rank, sqrt_slave, world_size)
                # send below right
                send_down_right(temp_array, world_rank, sqrt_slave, world_size)
                # send below left
                send_down_left(temp_array, world_rank, sqrt_slave, world_size)
                # send top right
                send_top_right(temp_array, world_rank, sqrt_slave, world_size)
                # send left part
                send_top_left(temp_array, world_rank, sqrt_slave, world_size)

                # determine whether line of rank is even or odd.
                if modulus_by_sqrt_slave == 0:
                    send_down(temp_array, world_rank, sqrt_slave, world_size)
                    send_up(temp_array, world_rank, sqrt_slave, world_size)
                    proc_grid[0,1:length_slave_array+1] = recv_top(world_rank, sqrt_slave, world_size)
                    proc_grid[-1,1:length_slave_array+1] = recv_down(world_rank, sqrt_slave, world_size)
                
                else :
                    proc_grid[0,1:length_slave_array+1] = recv_top(world_rank, sqrt_slave, world_size)
                    proc_grid[-1,1:length_slave_array+1] = recv_down(world_rank, sqrt_slave, world_size)
                    send_up(temp_array, world_rank, sqrt_slave, world_size)
                    send_down(temp_array, world_rank, sqrt_slave, world_size)

                # recv of odd rank
                proc_grid[1:length_slave_array+1,0] = recv_left(world_rank, sqrt_slave, world_size)
                proc_grid[1:length_slave_array+1,-1] = recv_right(world_rank, sqrt_slave, world_size)
                proc_grid[0,0] = recv_top_left(world_rank, sqrt_slave, world_size)
                proc_grid[0,-1] = recv_top_right(world_rank, sqrt_slave, world_size)
                proc_grid[-1,0] = recv_down_left(world_rank, sqrt_slave, world_size)
                proc_grid[-1,-1] = recv_down_right(world_rank, sqrt_slave, world_size)

            # 'temp_grid' hold the hard copy of ”procgrid” so that it doesn’t always move throughthe changing array when the game of life algorithm is applied
            temp_grid = np.copy(proc_grid)
            proc_grid = update_grid(temp_grid, proc_grid)
            
            temp_array = proc_grid[1:length_slave_array+1,1:length_slave_array+1]

        # Send the result to the master processor. 
        comm.send(temp_array, dest = 0, tag=world_rank)

    # Finalizes the MPI and process.
    MPI.Finalize()
