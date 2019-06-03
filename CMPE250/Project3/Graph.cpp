#include "Graph.h"

Graph::Graph(int V) {

    this->V = V;

    adj= new list<int>[V];

}

void Graph::addEdge(int v, int w) {

    adj[v].push_back(w - 1);

}

void Graph::topologicalSortUtil(int v, bool visited[], stack<int> &Stack) {

    visited[v] = true;

    list<int>::iterator i;
    for (i = adj[v].begin(); i != adj[v].end(); ++i)
        if (!visited[*i])

            topologicalSortUtil(*i, visited, Stack);

    Stack.push(v);
    
}

void Graph::topologicalSort() {

    stack<int> Stack;

    bool *visited = new bool[V];

    for (int i = 0; i < V; i++)
        visited[i] = false;

    for (int i = 0; i < V; i++)
        if (visited[i] == false)
            topologicalSortUtil(i, visited, Stack);

    while (Stack.empty() == false) {

        graphStack.push(Stack.top());

        Stack.pop();

    }

}

bool Graph::connect(int u , int v) {

    bool connect = false;

    list<int> tempList = adj[u];

    while(tempList.empty() == false){

        int temp = tempList.front();

        if(temp == v){

            connect = true;

            break;
        }

        tempList.pop_front();

    }

    return connect;

}
