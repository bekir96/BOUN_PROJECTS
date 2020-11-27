import sys

'''
    function damerau_levenshtein_distance takes two input string,(s,t) and calculates 
    Damerau Levenshtein distance and returns it, the corresponding edit table and the 
    sequence of operations needed to transform the first string into the second one.
'''
def damerau_levenshtein_distance(s, t):
    '''
        m represents length of source string, n represents length of target string.
        Construct d with size two greater than the length of the strings because to avoid 
        any "index out of range" error when backtracing. And also while constructing, we give 
        the maximum int value to all indexes. Because our algorithm takes the minimum value of 
        adjacent indexes, we do not want unused rows and columns to break our algorithm.
    '''
    cost = 0
    m = len(s)
    n = len(t)
    d = [[sys.maxsize for x in range(n+3)] for y in range(m+3)] 

    for i in range(1, m+2):     d[i][1] = i-1
    for j in range(1, n+2):     d[1][j] = j-1

    '''
        Traversing through the middle indexes of our 'd array', if the selected indexes of the 
        strings are not equal, we put a cost as 1, and then fill our 'd array' again. In addition, 
        the strings are compared with the diagnoal cell 2 units away, to check whether they are 
        swapped or not.
    '''
    for j in range(2, n+2):
        for i in range(2, m+2):
            if s[i-2] == t[j-2]:
                cost = 0
            else:
                cost = 1    # replace
            
            d[i][j] = min(d[i-1][j] + 1,                # delete
                            d[i][j-1] + 1,              # insert    
                                d[i-1][j-1] + cost)     # copy

            if (i > 2) & (j > 2) & (s[i-2] == t[j-3]) & (s[i-3] == t[j-2]):
                d[i][j] = min(d[i][j],\
                                d[i-2][j-2] + 1)

    '''
       Initialize the 'operations' dictionary in order to properly create the costs, type, input and 
       output values in the operations performed.
    '''        
    operations = {"cost": [],\
                    "operation": [],\
                    "input": [],\
                    "output": []}

    backtracing(d, m+1, n+1, s, t, operations)
    return d[m+1][n+1], d, operations



'''
    The backtracing function determines the operation types by looking at the values in the upper, 
    left and diagonal cells of all cells starting from the bottom right. Proceeding recursively, 
    it returns all operations at base condition. 
'''
def backtracing(d, m, n, s, t, operations):
    control = True
    if (m == 1) & (n == 1):
        return operations
    
    if (d[m-2][n-2] <= d[m][n]):        # Diagnoal cell 2 units away check
        if (s[m-2] == t[n-3]) & (s[m-3] == t[n-2]):

            operations["cost"].append(1)
            operations["operation"].append("swap")
            operations["input"].append(s[m-3] + " " + s[m-2]) 
            operations["output"].append(t[n-3] + " " + t[n-2]) 
            backtracing(d, m-2, n-2, s, t, operations)
            control = False

    if(control):
        if (d[m-1][n] <= d[m-1][n-1]) & (d[m-1][n] <= d[m][n-1]) & (d[m-1][n] <= d[m][n]):          # Diagonal check

            d_cost = d[m][n] - d[m-1][n]
            operations["cost"].append(d_cost)
            if d_cost == 0:
                operations["operation"].append("(copy)")
                operations["input"].append(s[m-2]) 
                operations["output"].append(t[n-2]) 
            else:
                operations["operation"].append("delete")
                operations["input"].append(s[m-2]) 
                operations["output"].append("*") 
            
            backtracing(d, m-1, n, s, t, operations)

        elif (d[m-1][n-1] <= d[m-1][n]) & (d[m-1][n-1] <= d[m][n-1]) & (d[m-1][n-1] <= d[m][n]):    # Left check

            d_cost = d[m][n] - d[m-1][n-1]
            operations["cost"].append(d_cost)
            if d_cost == 0:
                operations["operation"].append("(copy)")
                operations["input"].append(s[m-2]) 
                operations["output"].append(t[n-2]) 
            else:
                operations["operation"].append("replace")
                operations["input"].append(s[m-2]) 
                operations["output"].append(t[n-2]) 
            
            backtracing(d, m-1, n-1, s, t, operations)
            
        elif (d[m][n-1] <= d[m-1][n-1]) & (d[m][n-1] <= d[m-1][n]) & (d[m][n-1] <= d[m][n]):        # Up check
            
            d_cost = d[m][n] - d[m][n-1]
            operations["cost"].append(d_cost)
            if d_cost == 0:
                operations["operation"].append("(copy)")
                operations["input"].append(s[m-2]) 
                operations["output"].append(t[n-2]) 
            else:
                operations["operation"].append("insert")
                operations["input"].append("*") 
                operations["output"].append(t[n-2]) 
            
            backtracing(d, m, n-1, s, t, operations)
        
        

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Run with the following: \n python3 levensthein.py $string_1 $string_2")
        sys.exit(0)

    string_1 = sys.argv[1]
    string_2 = sys.argv[2]
    distance, d, operations = damerau_levenshtein_distance(string_1, string_2)  
    print("(a) The Damerau-Levenshtein edit distance between the two input string: {}\n".format(distance))

    print("(b) the corresponding edit table:")
    print('\n'.join([''.join(['{:4}'.format(d[i][j]) for j in range(1, len(d[i])-1)]) 
      for i in range(1, len(d)-1)]))

    print("\n(c) the sequence of operations needed to transform the first string into the second one: ")
    x = len(operations["cost"])
    print("{:<8} {:<15} {:<10} {:<10}".format('cost','operation','input','output'))
    for i in range(x-1 ,-1, -1):
        print("{:<8} {:<15} {:<10} {:<10}".format(operations["cost"][i],operations["operation"][i],operations["input"][i],operations["output"][i]))