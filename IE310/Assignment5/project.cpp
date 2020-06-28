#include <iostream>
#include <cmath>
using namespace std; 
#define EPSILON 0.0001

double phi = (1 + sqrt(5)) / 2;
double resphi = 2.0 - phi;
  
double func(double x) {  return 100.0 + 0.01*x - 0.1*x*x + 0.5*cos(3.0*x);  } 

double difFunc(double x){ return -1.5*sin(3.0*x) - 0.2*x + 0.01; }
    
double dif2Func(double x){  return -4.5*cos(3.0*x) - 0.2;}
  
void bisection(double a, double b) 
{ 
    int iteration = 1;
    double c = a; 
    while ((b-a) >= EPSILON) 
    { 
        c = (a+b)/2; 
  
        if (func(c) == 0.0) 
            break; 
        else if (func(c)*func(a) < 0) 
            b = c; 
        else
            a = c; 
        
        cout << "The value of Bisection root at iteration " << iteration << " is : " <<  c << endl;
        cout << "The value of Bisection at iteration " << iteration << " is : " << func(c) << endl;
        iteration++;
    } 
     
    cout << "The value of Bisection root is : " << c << endl;
    cout << "The value of Bisection is : " << func(c) << endl;
} 

double goldenSectionSearch(double a, double c,double b){
    if(abs(a - b) < EPSILON) return (a + b) / 2.0;
        
    double d = c + resphi * (b - c);
    if(func(d) < func(c))
        return goldenSectionSearch(c, d, b);
    else
        return goldenSectionSearch(d, c, a);
}
    

void newtonRaphson(double a){
    int iteration = 1;
    double h = difFunc(a) / dif2Func(a);

    while (abs(h) >= EPSILON){
        h = difFunc(a) / dif2Func(a);
        a = a - h;

        cout << "The value of Newton root at iteration " << iteration << " is : " <<  a << endl;
        cout << "The value of Newton at iteration " << iteration << " is : " << difFunc(a) << endl;
        iteration++;
    }

    cout << "The value of Newton root is : " << a << endl;
    cout << "The value of Newton is : " << difFunc(a) << endl;
}

void secant(double a, double b){
    int iteration = 1;
    double temp = 0.0;

    while(true){
        if(abs(b-a) < EPSILON)
            break;
        else if((difFunc(b)-dif2Func(a)) == 0){
            cout << "The value of Secant root is : " << b << endl;
            cout << "The value of Secant is : " << difFunc(b) << endl;
        }

        temp = b - (difFunc(b) * (b - a) * 1.0) / (difFunc(b) - difFunc(a));
        a = b;
        b = temp;
        cout << "The value of Secant root at iteration " << iteration << " is : " <<  b << endl;
        cout << "The value of Secant at iteration " << iteration << " is : " << func(b) << endl;
        iteration++;
    }
    cout << "The value of Secant root is : " << b << endl;
    cout << "The value of Secant is : " << func(b) << endl;
}

  
int main() 
{ 
// Bisection Method
    cout << "********** Bisection **********" << endl;
    double a = 0.8, b = 1.8; 
    bisection(a, b); 
    cout << "*******************************" << endl;


// Golden Section Method
    cout << "******** Golden Section *******" << endl;
    int goldenSectionRoot = goldenSectionSearch(a, (-1 + resphi * 2), b);
    cout << "The value of the Golden Section root is : " << goldenSectionRoot << endl;
    cout << "The value of Golden Section is : " << func(goldenSectionRoot) << endl;
    cout << "*******************************" << endl;

// Newton's Method
    cout << "********** Newton's ***********" << endl;
    newtonRaphson(a);
    cout << "*******************************" << endl;

// Secant Method
    cout << "*********** Secant ************" << endl;
    secant(a,b);
    cout << "*******************************" << endl;

    return 0; 
} 