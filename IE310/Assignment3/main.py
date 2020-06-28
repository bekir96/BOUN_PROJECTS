output = "output.txt"
f = open(output, 'w')

class Tableau:

    def __init__(self, filename):
        self.tableau = None
        self.Non_Basis = None
        self.Basis = None
        self.A = None
        self.tableau_n = 0

        self.load_tableau_from_file(filename)


    def __str__(self):

        header = ['z'] + ['x' + str(i) for i in self.Non_Basis]
        sets = "Non Basis: " + str(self.Non_Basis) + "     Basis: " + str(self.Basis)
        z = 'z* = ' + '{0:.3f}'.format(self.tableau[0][0])

        solution = [0.0] * (len(self.tableau[0]) - 1)
        for i in range(0, len(self.Non_Basis)):
            solution[self.Non_Basis[i] - 1] = self.tableau[i + 1][0]

        tmp = [['', 'b'] + ['x' + str(x) for x in range(1, len(self.tableau[0]))]]
        tmp += [[header[i]] + ['{0:.3f}'.format(x) for x in self.tableau[i]] for i in range(0, len(self.tableau))]

        shift = max([len(e) for row in tmp for e in row])

        separator = '+' + '+'.join(['~' * shift for _ in range(0, len(self.tableau[0]) + 1)]) + '+'

        return separator + "\n" + \
               ''.join(['|' + '|'.join('{0:>{shift}}'.format(x, shift=shift) for x in row) + '|\n' for row in tmp]) + \
               separator + \
               "\n" + sets + "\n" + z + '\nx* = (' + ', '.join(['{0:.3f}'.format(s) for s in solution]) + ')'


    def show_tableau(self, out=None, inn=None, answer=None, unboundeness=None):

        if answer is not None:
            info_tableau = "Tableau Final: " + answer
            final_space = "\n\n"
        elif unboundeness is None:
            info_tableau = "Tableau {}: Will enter x{} and leave x{}".format(self.tableau_n, inn, self.Non_Basis[out - 1])
            self.tableau_n += 1
            final_space = ""
        else:
            info_tableau = "Tableau {}: ".format(self.tableau_n)
            self.tableau_n += 1
            final_space = ""

        f.write("\n\n" + info_tableau + "\n" + self.__str__() + final_space)
        # print("\n\n" + info_tableau + "\n" + self.__str__() + final_space)

    # def build_tableau(self, filename):


    def load_tableau_from_file(self, filename):

        error_message = "The file is not in the correct format or the LPP is not in the standard form."

        with open(filename, 'r') as file:
            rows,cols = map(int, file.readline().replace('\n','').split())
            rows+=1
            cols+=rows

            m = rows - 1

            self.tableau = list(list(map(float, file.readline().replace('\n','').split())) for _ in range(0, rows))
            self.tableau[0].extend([0.0]*rows) 
            for i in range(1,len(self.tableau)):
                self.tableau[i][-1:-1] = [0.0] * (i-1) + [1.0] + [0.0] * (m-i)

            for i in range(0, rows):
                self.tableau[i] = [self.tableau[i][-1]] + self.tableau[i][0:-1]

            self.Non_Basis = []
            for j in range(0, cols):
                n_zeros = 0
                n_ones = 0

                jj = j
                for i in range(0, rows):
                    if self.tableau[i][j] == 1.0:
                        n_ones += 1
                        ii = i
                    elif self.tableau[i][j] == 0.0:
                        n_zeros += 1
                    else:
                        break

                if n_ones == 1 and n_zeros == m:
                    self.Non_Basis.append((ii, jj))

            if len(self.Non_Basis) != m:
                raise ValueError(error_message)

            self.Non_Basis.sort(key=lambda tup: tup[0])
            self.Non_Basis = list(list(zip(*self.Non_Basis))[1])
            self.Basis = [j for j in range(1, cols) if j not in self.Non_Basis]  # except 1 because is LD

            self.tableau[0] = [-x for x in self.tableau[0]]  

    def change_base(self, i, j):

        div = self.tableau[i][j]
        self.tableau[i] = list(map(lambda x: x / div, self.tableau[i]))

        tmp_range = range(0, len(self.tableau))

        for ii in tmp_range:
            if ii == i:
                continue
            else:
                b = -self.tableau[ii][j]
                tmp = map(lambda x: x * b, self.tableau[i])
                self.tableau[ii] = list(map(lambda a: sum(a), zip(tmp, self.tableau[ii])))

        self.adjust_basis_or_non(i,j)

    def adjust_basis_or_non(self, i, j):

        tmp = self.Non_Basis[i - 1]
        self.Non_Basis[i - 1] = j
        self.Basis.remove(j)
        self.Basis.append(tmp)
        self.Basis.sort()

    def min_ratio_test(self):
        
        j = min(map(lambda j: (j, self.tableau[0][j]), self.Basis), key=lambda x: x[1])[0] # Find min value with index of z
        l = [i for i in range(1, len(self.tableau))] 
        l = [(self.tableau[i][0] / self.tableau[i][j], i) for i in l if self.tableau[i][0] / self.tableau[i][j] > 0.0]
        if l == []:
            return None, None
        else:
            i = min(l, key=lambda div: div[0])[1]
            self.show_tableau(i, j)
            return i, j

    def has_solution(self):
        return min([self.tableau[0][j] for j in self.Basis]) >= 0.0

    def has_degenerate(self):
        for row in self.tableau[1:]: # 1: only runs in option 1
            if row[0] == 0.0:
                return True
        return False

    def has_multiple_solutions(self):
        return min([self.tableau[0][j] for j in self.Basis]) == 0.0
    

class Simplex:

    def __init__(self, tableau):
        self.tableau = tableau
        self.answer = None

    def run(self):
        self.simplex()
        self.tableau.show_tableau(answer=self.answer)

    def simplex(self):
 
        bnd = False
        while not self.tableau.has_solution():
            i, j = self.tableau.min_ratio_test()
            if i is None:
                bnd = True
                self.answer = "Unboundeness solution"
                return
            else:
                self.tableau.change_base(i, j)

        if not bnd:
            tmp = ""
            if self.tableau.has_degenerate():
                tmp = " and degenerate"

            if self.tableau.has_multiple_solutions():
                self.answer = "Multiple solution" + tmp
            else:
                self.answer = "Unique Solution" + tmp

if __name__ == "__main__":

    for i in range(1,4):
        filename = "Assignment3_Spring2020_Data" + str(i) + ".txt"
        header = "SAMPLE " + str(i) 
        f.write('=' * 60)
        f.write('\n' + header.center(60, ' ') + '\n')
        f.write('=' * 60)
        # print("\n")
        # print(header.center(60, ' '))
        # print('=' * 60)
        tableau = Tableau(filename)
        simplex = Simplex(tableau)
        simplex.run()
    
    f.close()