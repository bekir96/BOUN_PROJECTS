import sys
import numpy as np
from sys import exit
import copy
import re
import os

OUTPUT_FILE = 'output.txt'
INPUT_FILE = ''

np.set_printoptions(precision=3)

# Function for exchanging two rows of a matrix 
def swap(Matrix, row1, row2, col): 
    for i in range(col): 
        temp = Matrix[row1][i] 
        Matrix[row1][i] = Matrix[row2][i] 
        Matrix[row2][i] = temp

# Find rank of a matrix 
def rankOfMatrix(Matrix, rank): 
    length = len(Matrix)
    for row in range(0, length): 

        # Before we visit current row  
        # 'row', we make sure that  
        # mat[row][0],....mat[row][row-1]  
        # are 0.  
    
        # Diagonal element is not zero 
        if Matrix[row][row] != 0: 
            for col in range(0, length): 
                if col != row: 
                        
                    # This makes all entries of current  
                    # column as 0 except entry 'mat[row][row]'  
                    multiplier = (Matrix[col][row] /
                                    Matrix[row][row]) 

                    for i in range(rank): 
                        Matrix[col][i] -= (multiplier *
                                            Matrix[row][i]) 
                                                
        # Diagonal element is already zero.  
        # Two cases arise:  
        # 1) If there is a row below it  
        # with non-zero entry, then swap  
        # this row with that row and process  
        # that row  
        # 2) If all elements in current  
        # column below mat[r][row] are 0,  
        # then remove this column by  
        # swapping it with last column and  
        # reducing number of columns by 1.  
        else: 
            reduce = True
            # Find the non-zero element  
            # in current column  
            for i in range(row, length): 
                    
                # Swap the row with non-zero  
                # element with this row. 
                if Matrix[i][row] != 0: 
                    swap(Matrix, row, i, rank) 
                    reduce = False
                    break

            # If we did not find any row with  
            # non-zero element in current  
            # column, then all values in  
            # this column are 0. 
            if reduce: 
                    
                control = True  
                # Reduce number of columns 
                for i in range(row, length):
                    if Matrix[row][i] != 0 : 
                        control = False
                
                if control:
                    rank -= 1
                        
            # process this row again 
            row -= 1

    # if Matrix[0][0] == 0, we check last 
    # index of first row since we maybe
    # find no zero b matrix value.           
    for row in range(len(Matrix)):
        if Matrix[row][row] != 0:
            break
        elif Matrix[row][-1] == 0:
            rank -= 1
            
    return (rank) 


def transposeMatrix(m):
    return list(map(list,zip(*m)))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

def gauss(A):
    n = len(A)
    x = [0 for i in range(n)]
    
    for i in range(n-1, -1, -1):
        if A[i][i] == 0:
            x[i] = 0
        else:
            x[i] = A[i][n]/A[i][i]
        for k in range(i-1, -1, -1):
            A[k][n] -= A[k][i] * x[i]

    return x    

if __name__ == "__main__":

    if os.path.isfile(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    for txt in range(0,3):
        # Each turn we set variables to empty.
        MATRIX_A = []
        MATRIX_B = []
        MATRIX_AB = []
        ENTRIES = 0

        INPUT_FILE = 'Assignment2_Spring2020_Data' + str(txt+1) + '.txt'

        with open(INPUT_FILE) as file:
            ENTRIES = int(file.readline().strip())

            # Although the given matrix n x (n+1), my rank algorithm is work for
            # n x n matrix, so add last row with 0 which does not effect original
            # matrix.
            MATRIX_AB = np.zeros((ENTRIES+1, ENTRIES + 1), dtype=float)  

            # Traverse all line to construct matrix A and matrix B.
            for line in file:
                temp_list = [float(i) for i in line.strip().split(" ")]
                MATRIX_A.append(temp_list[0:ENTRIES])
                MATRIX_B.append(temp_list[-1])

        MATRIX_AB[0:ENTRIES,0:ENTRIES] = MATRIX_A
        MATRIX_AB[0:-1,-1] = MATRIX_B
        TEMP_MATRIX_A = copy.deepcopy(MATRIX_A)
        TEMP_MATRIX_AB = copy.deepcopy(MATRIX_AB[0:ENTRIES+1][0:-1])

        MATRIX_A = np.asarray(MATRIX_A)
        MATRIX_B = np.asarray(MATRIX_B)

        rank_A = rankOfMatrix(MATRIX_A, len(MATRIX_A))
        rank_AB = rankOfMatrix(MATRIX_AB, len(MATRIX_AB))

        if rank_A < rank_AB:
            f = open(OUTPUT_FILE, "a")
            f.write('{}.  '.format(str(txt+1)))
            f.write("Inconsistent problem\n\n")
            f.close()

        elif rank_A == rank_AB and rank_A < ENTRIES:
            arbitrary = ENTRIES-rank_A
            tmp = np.zeros((1, (arbitrary)), dtype=float) 
            f = open(OUTPUT_FILE, "a")
            f.write('{}.  '.format(str(txt+1)))
            f.write('{}: {}\n'.format('Arbitrary variables', str(re.sub('[\[\]]', '', np.array_str(tmp)))))
            f.write('    {}: {}\n\n'.format('Arbitrary solution ', str(re.sub('[\[\]]', '', np.array_str(np.asarray(gauss(MATRIX_AB[0:-1])))))))
            f.close()

        elif rank_A == ENTRIES:
            X = getMatrixInverse(TEMP_MATRIX_A)
            Y = np.reshape(MATRIX_B,(ENTRIES,1))
            result = np.zeros((ENTRIES, 1), dtype=float) 
            for i in range(len(X)):
                # iterate through columns of Y
                for j in range(len(Y[0])):
                    # iterate through rows of Y
                    for k in range(len(Y)):
                        result[i][j] += X[i][k] * Y[k][j]

            f = open(OUTPUT_FILE, "a")
            f.write('{}.  '.format(str(txt+1)))
            f.write('{}: {}\n'.format('Unique solution', str(np.reshape(result,(1,ENTRIES)))[2:-2]))
            f.write('    {0:s}:\n {1:s}\n\n'.format('Inverted A', str(re.sub('[\[\]]', '', np.array_str(np.asarray(X))))))
            f.close()
