#ifndef GRAPH_H
#define GRAPH_H
#include <list>
#include <iostream>
#include <stack>
#include <queue>

using namespace std;

class Graph {

public:

    int V;

    list<int> *adj;

    queue<int> graphStack;

    void topologicalSortUtil(int v, bool visited[], stack<int> &Stack);

    Graph(int v);

    void addEdge(int v, int w);

    void topologicalSort();

    bool connect(int u, int v);

};

#endif //PROJECT3_GRAPH_H
