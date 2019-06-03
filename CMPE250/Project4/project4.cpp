#include <iostream>
#include <queue>
using namespace std;
int ar[1200][1200];
int Dist[1200][1200];
bool Visited[1200][1200];
int dir[4][2] = {{0 ,1}, {0, -1}, {1, 0}, {-1, 0}};
struct Node {
    int x,y;
    int cost;
    Node(int x,int y,int cost) : x(x), y(y), cost(cost) {}
};
bool operator < (const Node& a, const Node& b) {
    return a.cost > b.cost;
}
void init(int n, int m) {
    for(int i = 1; i <= n; i++)
        for(int j = 1; j <= m; j++) {
            Dist[i][j] = 1000000000;
            Visited[i][j] = false;
        }
}
int main(int argc, char* argv[]) {
    assert(argc == 3);
    freopen(argv[1], "r", stdin); // File read
    freopen(argv[2], "w", stdout); // File write
    int n,m;
    scanf(" %d %d", &n, &m);
    for(int i = 1; i <= n; i++) {
        for(int j = 1; j <= m; j++) {
            scanf(" %d", &ar[i][j]);
        }
    }
    int Q;
    scanf(" %d", &Q);
    while(Q--) {
        init(n, m);
        int sX, sY, fX, fY;
        scanf(" %d %d %d %d", &sX, &sY, &fX, &fY);
        priority_queue <Node> q;
        q.push(Node(sX, sY, 0));
        Dist[sX][sY] = 0;
        while(!q.empty()) {
            Node cur = q.top();
            q.pop();
            if(cur.x == fX && cur.y == fY) {
                printf("%d\n", cur.cost);
                break;
            }
            if(Visited[cur.x][cur.y]) continue;
            Visited[cur.x][cur.y] = true;
            for(int k = 0; k < 4; k++) {
                int newX = cur.x + dir[k][0];
                int newY = cur.y + dir[k][1];
                if(ar[newX][newY] == 0) continue;
                int newCost = max(cur.cost, abs(ar[newX][newY] - ar[cur.x][cur.y]));
                if(Dist[newX][newY] > newCost) {
                    Dist[newX][newY] = newCost;
                    q.push(Node(newX, newY, newCost));
                }
            }
        }
    }
    return 0;
}
