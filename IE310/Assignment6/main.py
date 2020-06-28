from prettytable import PrettyTable
import math
filename = "output.txt"
f = open(filename, 'w+')

t = PrettyTable(['k', 'x f(x)', 'j', 'd', 'y(j)', 'landa', 'y(j+1)'])


class GoldenSection:

    def __init__(self, I):
        self.index = 0
        self.L = I
        self.a = 0
        self.b = 0
        self.landa = 0
        self.miuo = 0
        self.f_landa = 0
        self.f_miuo = 0 
        self.answer = 0
        self.f_answer = 0
        self.alfa = 0.618
        self.y = []
        self.d = []

    def initialStep(self):
        self.landa = self.a + (1.0 - self.alfa) * (self.b - self.a)
        self.miuo = self.a + (self.alfa * (self.b - self.a))
        self.f_landa = self.function1(self.landa)
        self.f_miuo = self.function1(self.miuo)
        self.index = 1

    def mainStep(self):
        if self.b - self.a < self.L:
            self.answer = (self.a + self.b) / 2
            self.f_answer = self.function1(self.answer)
            return
        elif self.f_landa > self.f_miuo:
            self.step2()
        elif self.f_landa <= self.f_miuo:
            self.step3()
    
    def step2(self):
        self.a = self.landa
        self.landa = self.miuo
        self.f_landa = self.f_miuo
        self.miuo = self.a + (self.alfa * (self.b - self.a))
        self.f_miuo = self.function1(self.miuo)
        self.step4()
    
    def step3(self):
        self.b = self.miuo
        self.miuo = self.landa
        self.f_miuo = self.f_landa
        self.landa = self.a + ((1.0 - self.alfa) * (self.b - self.a))
        self.f_landa = self.function1(self.landa)
        self.step4()

    def step4(self):
        self.index+=1
        self.mainStep()

    def function1(self, x):
        result = 0.0
        temp1 = (5 * (self.y[0] + x * self.d[0])) - (self.y[1] + x * self.d[1])
        temp2 = self.y[0] + x * self.d[0] - 2
        temp3 = (self.y[0] + x * self.d[0]) - (2 * (self.y[1] + x * self.d[1]))
        result = temp1 ** 4 + temp2 ** 2 + temp3 + 12
        return result      
            

class CyclicCoordinate:
    
    def __init__(self, input):
        self.epsilon = 0.001
        self.d1 = [1,0]
        self.d2 = [0,1]
        self.x = input[:]
        self.y = []
        self.f_x = 0
        self.j = 0
        self.k = 0
        self.landa = 0


    def initialStep(self):
        self.y = self.x[:]
        self.k = 1
        self.j = 1

    def mainStep(self):
        tempY = []
        
        while self.j <= 2:
            gs = GoldenSection(0.001)
            gs.a = -9.0
            gs.b = 2.0
            gs.y = self.y[:]

            if self.j == 1:
                gs.d = self.d1[:]
            else:
                gs.d = self.d2[:]
            gs.initialStep()
            gs.mainStep()
            self.landa = gs.answer
            if self.j == 1:
                tempY = self.y[:]
                self.y[0] = tempY[0] + (self.landa * self.d1[0])
                self.y[1] = tempY[1] + (self.landa * self.d1[1])
                t.add_row([str(self.k), "(" + str('{0:.6f}'.format(self.x[0])) + " , " + str('{0:.6f}'.format(self.x[1])) + ")", self.j, "(" + str(self.d1[0])+" , " + str(self.d1[1]) + ")", "(" + str('{0:.6f}'.format(tempY[0])) + " , " + str('{0:.6f}'.format(tempY[1])) + ")", '{0:.6f}'.format(self.landa), "(" + str('{0:.6f}'.format(self.y[0])) + " , " + str('{0:.6f}'.format(self.y[1])) + ")"])
            elif self.j == 2:
                tempY = self.y[:]
                self.y[0] = tempY[0] + (self.landa * self.d2[0])
                self.y[1] = tempY[1] + (self.landa * self.d2[1])
                self.f_x = self.function(self.x)
                t.add_row([str(self.k), str('{0:.6f}'.format(self.f_x)), self.j, "(" + str(self.d2[0])+" , " + str(self.d2[1]) + ")", "(" + str('{0:.6f}'.format(tempY[0])) + " , " + str('{0:.6f}'.format(tempY[1])) + ")", '{0:.6f}'.format(self.landa), "(" + str('{0:.6f}'.format(self.y[0])) + " , " + str('{0:.6f}'.format(self.y[1])) + ")"])
            self.j+=1
        self.step2()
    
    def step2(self):
        tempX = []
        tempX = self.x[:]
        self.x = self.y[:]
        minusX = [0.0,0.0]
        minusX[0] = self.x[0] - tempX[0]
        minusX[1] = self.x[1] - tempX[1] 
        norm2 = self.Norm2(minusX)
        if norm2 < self.epsilon:
            return False
        else:
            self.y = self.x[:]
            self.j = 1   
            self.k+=1
            return self.mainStep()
    
    def Norm2(self, param):
        temp = param[0] ** 2 + param[1] ** 2
        result = math.sqrt(temp)
        return result
    
    def function(self, x):
        result = 0
        temp1 = 5 * x[0] - x[1]
        temp2 = x[0] - 2
        temp3 = x[0] - (2 * x[1])
        result = temp1 ** 4 + temp2 ** 2 + temp3 + 12
        return result



cyclic = CyclicCoordinate([6,34])
cyclic.initialStep()
cyclic.mainStep()
f.write("-" * 20 + "   Cyclic Coordinate   " + "-" * 20 + "\n\n" )
f.write(t.get_string())

t1 = PrettyTable(['k', 'x f(x)', 'j', 'y(j)', 'd(j)', 'landa', 'y(j+1)', 'd', 'landa_had', 'y(j) + landa_had*d'])

class HookeAndJeeves:

    def __init__(self, input):
        self.epsilon = 0.0001
        self.d1 = [1,0]
        self.d2 = [0,1]
        self.x = input[:]
        self.x_previous = self.x[:]
        self.y = []
        self.f_x = 0
        self.j = 0
        self.k = 0
        self.landa = 0
        self.answer = 0
        self.tempY = [0.0, 0.0]

    def initialStep(self):
        self.y = self.x[:]
        self.k = 1
        self.j = 1

    def mainStep(self):
        while self.j <= 2:
            gs = GoldenSection(0.0001)
            gs.a = -9.0
            gs.b = 2.0
            gs.y = self.y[:]

            if self.j == 1:
                gs.d = self.d1[:]
            else:
                gs.d = self.d2[:]
            gs.initialStep()
            gs.mainStep()
            self.landa = gs.answer
            if self.j == 1:
                self.tempY = self.y[:]
                self.y[0] = self.tempY[0] + (self.landa * self.d1[0])
                self.y[1] = self.tempY[1] + (self.landa * self.d1[1])
                t1.add_row([str(self.k), "(" + str('{0:.6f}'.format(self.x[0])) + " , " + str('{0:.6f}'.format(self.x[1])) + ")", self.j, "(" + str('{0:.6f}'.format(self.tempY[0])) + " , " + str('{0:.6f}'.format(self.tempY[1])) + ")", "(" + str(self.d1[0])+" , " + str(self.d1[1]) + ")",  '{0:.6f}'.format(self.landa), "(" + str('{0:.6f}'.format(self.y[0])) + " , " + str('{0:.6f}'.format(self.y[1])) + ")", "_", "_", "_"])
            elif self.j == 2:
                self.tempY = self.y[:]
                self.y[0] = self.tempY[0] + (self.landa * self.d2[0])
                self.y[1] = self.tempY[1] + (self.landa * self.d2[1])
                self.f_x = self.function(self.x)
            self.j+=1
        self.j = 2
        self.x_previous = self.x[:]
        self.x = self.y[:]
        if not self.haltCondition(self.x_previous, self.x):
            return False
        else:
            self.step2()

    def haltCondition(self, a, b):
        minus = [0.0, 0.0]
        minus[0] = b[0] - a[0]
        minus[1] = b[1] - a[1]
        norm2 = self.Norm2(minus)
        if norm2 < self.epsilon:
            return False
        else:
            return True

    def Norm2(self, param):
        temp = param[0] ** 2 + param[1] ** 2
        result =  math.sqrt(temp)
        return result

    def step2(self):
        d = [0.0, 0.0]
        d[0] = self.x[0] - self.x_previous[0]
        d[1] = self.x[1] - self.x_previous[1]
        gs2 = GoldenSection(0.001)
        gs2.a = -9.0
        gs2.b = 2.0
        gs2.d = d[:]
        gs2.y = self.x[:]
        gs2.initialStep()
        gs2.mainStep()
        self.answer = gs2.answer
        y2 = [0.0, 0.0]
        y2[0] = self.x[0] + (self.answer * d[0])
        y2[1] = self.x[1] + (self.answer * d[1])
        t1.add_row([str(self.k), str('{0:.6f}'.format(self.f_x)), self.j, "(" + str('{0:.6f}'.format(self.tempY[0])) + " , " + str('{0:.6f}'.format(self.tempY[1])) + ")", "(" + str(self.d2[0])+" , " + str(self.d2[1]) + ")",  '{0:.6f}'.format(self.landa), "(" + str('{0:.6f}'.format(self.y[0])) + " , " + str('{0:.6f}'.format(self.y[1])) + ")", "(" + str('{0:.6f}'.format(d[0])) + " , " + str('{0:.6f}'.format(d[1])) + ")", '{0:.6f}'.format(self.answer), "(" + str('{0:.6f}'.format(y2[0])) + " , " + str('{0:.6f}'.format(y2[1])) + ")"])
        self.y = y2[:]
        self.k+=1
        self.j=1
        return self.mainStep()

    def function(self, x):
        result = 0
        temp1 = 5 * x[0] - x[1]
        temp2 = x[0] - 2
        temp3 = x[0] - (2 * x[1])
        result = temp1 ** 4 + temp2 ** 2 + temp3 + 12
        return result


hookie = HookeAndJeeves([6,34])
hookie.initialStep()
hookie.mainStep()
f.write("\n\n" + "-" * 20 + "   Hooke And Jeeves   " + "-" * 20 + "\n\n" )
f.write(t1.get_string())
        

t2 = PrettyTable(['k', 'x f(x)', 'j', 'y(j)', 'f(y(j))', 'd(j)', 'landa(j)', 'y(j+1)', 'f(y(j+1))'])

class SteepestandDescent:

    def __init__(self, input):
        self.epsilon = 0.0001
        self.d1 = [1,0]
        self.d2 = [0,1]
        self.x = input[:]
        self.landa1 = 0
        self.landa2 = 0
        self.y = []
        self.x_previous = []
        self.f_x = 0
        self.f_y = 0
        self.j = 0
        self.k = 0
        self.answer = 0

    def initialStep(self):
        self.y = self.x[:]
        self.k = 1
        self.j = 1

    def mainStep(self):
        temp_y = []
        
        while self.j <= 2:
            gs = GoldenSection(0.0001)
            gs.a = -9.0
            gs.b = 2.0
            gs.y = self.y[:]

            if self.j == 1:
                gs.d = self.d1[:]
                gs.initialStep()
                gs.mainStep()
                self.landa1 = gs.answer
                temp_y = self.y[:]
                self.y[0] = temp_y[0] + (self.landa1 * self.d1[0])
                self.y[1] = temp_y[1] + (self.landa1 * self.d1[1])
                f_temp_y = self.function(temp_y)
                self.f_y = self.function(self.y)
                t2.add_row([str(self.k), "(" + str('{0:.6f}'.format(self.x[0])) + " , " + str('{0:.6f}'.format(self.x[1])) + ")", self.j, "(" + str('{0:.6f}'.format(temp_y[0])) + " , " + str('{0:.6f}'.format(temp_y[1])) + ")", '{0:.6f}'.format(f_temp_y),  "(" + str('{0:.6f}'.format(self.d1[0])) + " , " + str('{0:.6f}'.format(self.d1[1])) + ")", '{0:.6f}'.format(self.landa1), "(" + str('{0:.6f}'.format(self.y[0])) + " , " + str('{0:.6f}'.format(self.y[1])) + ")", '{0:.6f}'.format(self.f_y)])
            elif self.j == 2:
                gs.d = self.d2[:]
                gs.initialStep()
                gs.mainStep()
                self.landa2 = gs.answer
                temp_y = self.y[:]
                self.y[0] = temp_y[0] + (self.landa2 * self.d1[0])
                self.y[1] = temp_y[1] + (self.landa2 * self.d1[1])
                f_temp_y = self.function(temp_y)
                self.f_y = self.function(self.y)
                self.f_x = self.function(self.x)
                t2.add_row([str(self.k), str('{0:.6f}'.format(self.f_x)), self.j, "(" + str('{0:.6f}'.format(temp_y[0])) + " , " + str('{0:.6f}'.format(temp_y[1])) + ")", '{0:.6f}'.format(f_temp_y), "(" + str('{0:.6f}'.format(self.d2[0])) + " , " + str('{0:.6f}'.format(self.d2[1])) + ")",  '{0:.6f}'.format(self.landa2), "(" + str('{0:.6f}'.format(self.y[0])) + " , " + str('{0:.6f}'.format(self.y[1])) + ")", '{0:.6f}'.format(self.f_y)])

            self.j+=1

        self.x_previous = self.x[:]
        self.x = self.y[:]
        if not self.haltCondition(self.x_previous, self.x):
            return False
        else:
            self.y = self.x[:]
            self.k+=1
            self.j=1
            self.step3()

    def haltCondition(self, a, b):
        minus = [0.0, 0.0]
        minus[0] = b[0] - a[0]
        minus[1] = b[1] - a[1]
        norm2 = self.Norm2(minus)
        if norm2 < self.epsilon:
            return False
        else:
            return True

    def Norm2(self, param):
        temp = param[0] ** 2 + param[1] ** 2
        result =  math.sqrt(temp)
        return result

    def step3(self):
        aj1 = [0.0, 0.0]
        aj2 = [0.0, 0.0]
        bj1 = [0.0, 0.0]
        bj2 = [0.0, 0.0]
        if self.landa1 == 0:
            aj1 = self.d1[:]
        else:
            aj1[0] = (self.landa1 * self.d1[0]) + (self.landa2 * self.d2[0])
            aj1[1] = (self.landa1 * self.d1[1]) + (self.landa2 * self.d2[1])

        bj1 = aj1[:]
        bj1Norm2 = self.Norm2(bj1)
        self.d1[0] = bj1[0] / bj1Norm2
        self.d1[1] = bj1[1] / bj1Norm2

        if self.landa2 == 0:
            aj2 = self.d2[:]
        else:
            aj2[0] = (self.landa2 * self.d2[0])
            aj2[1] = (self.landa2 * self.d2[1])

        bj2[0] = aj2[0] - (((aj2[0] * self.d1[0]) + (aj2[1] * self.d1[1])) * self.d1[0])
        bj2[1] = aj2[1] - (((aj2[0] * self.d1[0]) + (aj2[1] * self.d1[1])) * self.d1[1])
        bj2Norm2 = self.Norm2(bj2)
        self.d2[0] = bj2[0] / bj2Norm2
        self.d2[1] = bj2[1] / bj2Norm2
        return self.mainStep()

    def function(self, x):
        result = 0
        temp1 = 5 * x[0] - x[1]
        temp2 = x[0] - 2
        temp3 = x[0] - (2 * x[1])
        result = temp1 ** 4 + temp2 ** 2 + temp3 + 12
        return result

steepest = SteepestandDescent([6,34])
steepest.initialStep()
steepest.mainStep()
f.write("\n\n" + "-" * 20 + "   Steepest And Descent   " + "-" * 20 + "\n\n" )
f.write(t2.get_string())
f.close()
        