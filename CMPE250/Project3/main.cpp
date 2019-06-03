#include <iostream>
#include <fstream>
#include <queue>
#include <string>
#include "Graph.h"

using namespace std;

int main(int argc,char* argv[]) {

    int numberPiggy;

    string input = argv[1];

    string output = argv[2];

    ifstream infile(input);

    infile >> numberPiggy;

    Graph* piggyBanks = new Graph(numberPiggy);

    for(int i = 0; i < numberPiggy  ; i++){

        int keyNos = 0;

        infile >> keyNos ;

        for(int j = 0 ; j < keyNos ; j++){

            int keyValues;

            infile >> keyValues;

            piggyBanks->addEdge(i, keyValues);

        }

    }

    piggyBanks->topologicalSort();

    queue<int> brokenPiggy;

    stack<int> controlStack;

    int vertex = piggyBanks->graphStack.front();

    controlStack.push(vertex);

    brokenPiggy.push(vertex);

    piggyBanks->graphStack.pop();

    while(piggyBanks->graphStack.size() != 0){

        bool flag = true;

        bool control1 = false;

        bool control2 = false;

        while(flag  && piggyBanks->graphStack.empty() == false ){

            int tempEx = piggyBanks->graphStack.front() ;

            controlStack.push(tempEx);

            flag = piggyBanks->connect(vertex, tempEx);

            piggyBanks->graphStack.pop();

            vertex = tempEx;

            control1 = true;

        }

        stack<int> tempStack = controlStack;

        tempStack.pop();

        while(!flag && tempStack.size() != 0){

            int controlInt = tempStack.top();

            flag = piggyBanks->connect(controlInt, vertex);

            tempStack.pop();

        }

        if(flag){

            control2 = true;

        }

        if(control1 && control2){

        } else {

            brokenPiggy.push(vertex);

        }

    }

    ofstream m;
    
    m.open(output);

    m << brokenPiggy.size() << " ";

    while(brokenPiggy.empty() == false) {

        m << brokenPiggy.front() + 1 << " " ;

        brokenPiggy.pop();

    }

    return 0;

}
