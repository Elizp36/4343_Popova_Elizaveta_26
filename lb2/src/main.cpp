#include <iostream>
#include <vector>
#include <algorithm>
#include <tuple>
#include <climits>
#include <iomanip>
using namespace std;

const int INF = INT_MAX / 2;
const bool DEBUG = true;

struct Result {
    int cost;
    vector<int> path;
    bool exists;
};

class DSU {
    vector<int> parent, rank_;
public:
    DSU(int n) {
        parent.resize(n);
        rank_.assign(n, 0);
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    bool unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        if (rank_[px] < rank_[py]) swap(px, py);
        parent[py] = px;
        if (rank_[px] == rank_[py]) rank_[px]++;
        return true;
    }
};

int calculateMST(const vector<vector<int>>& g, const vector<bool>& available) {
    int n = g.size();
    int availableCount = 0;
    for (bool b : available) if (b) availableCount++;
    if (availableCount <= 1) return 0;

    vector<tuple<int, int, int>> edges;
    edges.reserve(n * n);
    for (int i = 0; i < n; i++) {
        if (!available[i]) continue;
        for (int j = i + 1; j < n; j++) {
            if (!available[j] || g[i][j] >= INF) continue;
            edges.emplace_back(g[i][j], i, j);
        }
    }
    sort(edges.begin(), edges.end());

    DSU dsu(n);
    int mstWeight = 0, edgesUsed = 0;
    for (const auto& [w, u, v] : edges) {
        if (dsu.unite(u, v)) {
            mstWeight += w;
            if (++edgesUsed == availableCount - 1) break;
        }
    }
    return (edgesUsed != availableCount - 1) ? INF : mstWeight;
}

class TSP_Little {
    vector<vector<int>> costs;
    int n;
    int bestCost;
    vector<int> bestPath;
    int depth;

    void printIndent() {
        if (!DEBUG) return;
        for (int i = 0; i < depth; i++) cout << "  ";
    }

    int reduceRow(vector<vector<int>>& m, int row) {
        int minVal = INF;
        for (int j = 0; j < n; j++)
            if (m[row][j] < INF) minVal = min(minVal, m[row][j]);
        if (minVal == INF) return 0;
        for (int j = 0; j < n; j++)
            if (m[row][j] < INF) m[row][j] -= minVal;
        return minVal;
    }

    int reduceCol(vector<vector<int>>& m, int col) {
        int minVal = INF;
        for (int i = 0; i < n; i++)
            if (m[i][col] < INF) minVal = min(minVal, m[i][col]);
        if (minVal == INF) return 0;
        for (int i = 0; i < n; i++)
            if (m[i][col] < INF) m[i][col] -= minVal;
        return minVal;
    }

    int reduceMatrix(vector<vector<int>>& m) {
        int c = 0;
        for (int i = 0; i < n; i++) c += reduceRow(m, i);
        for (int j = 0; j < n; j++) c += reduceCol(m, j);
        return c;
    }

    int nearestNeighbor(int start, vector<int>& path) {
        vector<bool> vis(n, false);
        vis[start] = true;
        path = {start};
        int curr = start;
        int cost = 0;

        for (int step = 1; step < n; ++step) {
            int bestNext = -1;
            int minDist = INF;
            for (int j = 0; j < n; ++j) {
                if (!vis[j] && costs[curr][j] < INF && costs[curr][j] < minDist) {
                    minDist = costs[curr][j];
                    bestNext = j;
                }
            }
            if (bestNext == -1) return INF;
            vis[bestNext] = true;
            path.push_back(bestNext);
            cost += minDist;
            curr = bestNext;
        }
        if (costs[curr][start] >= INF) return INF;
        cost += costs[curr][start];
        return cost;
    }

    void solveBranch(vector<vector<int>> matrix, vector<int>& path,
                     vector<bool>& visited, int currentLB) {
        if (DEBUG) {
            printIndent();
            cout << "[Depth " << depth << "] Path: ";
            for (int v : path) cout << v << " ";
            cout << "| LB: " << currentLB << "| Best: " << bestCost << "\n";
        }

        if (path.size() == n) {
            if (costs[path.back()][path[0]] < INF) {
                int actualCost = 0;
                for (size_t i = 0; i < n; ++i)
                    actualCost += costs[path[i]][path[(i + 1) % n]];
                
                if (actualCost < bestCost || (actualCost == bestCost && path < bestPath)) {
                    bestCost = actualCost;
                    bestPath = path;
                    if (DEBUG) {
                        printIndent();
                        cout << "New best solution found! Cost: " << actualCost << "\n";
                        printIndent();
                        cout << "  Path: ";
                        for (int v : path) cout << v << " ";
                        cout << "\n";
                    }
                }
            }
            return;
        }

        if (currentLB >= bestCost) {
            if (DEBUG) {
                printIndent();
                cout << "Branch pruned (LB >= best)\n";
            }
            return;
        }

        int last = path.back();
        for (int next = 0; next < n; ++next) {
            if (!visited[next] && costs[last][next] < INF) {
                visited[next] = true;
                path.push_back(next);
                depth++;

                vector<vector<int>> nextMatrix = matrix;
                for (int i = 0; i < n; ++i) nextMatrix[last][i] = INF;
                for (int i = 0; i < n; ++i) nextMatrix[i][next] = INF;
                nextMatrix[next][last] = INF;

                int reduction = reduceMatrix(nextMatrix);
                if (DEBUG && reduction > 0) {
                    printIndent();
                    cout << "Matrix reduced by: " << reduction << "\n";
                }

                vector<bool> avail(n, false);
                for (int i = 0; i < n; ++i) if (!visited[i]) avail[i] = true;
                int mstRem = calculateMST(costs, avail);

                int newLB = currentLB + reduction + (mstRem < INF ? mstRem : 0);
                
                if (DEBUG) {
                    printIndent();
                    cout << "Try edge " << last << "→" << next;
                    cout << " | Reduction: " << reduction;
                    cout << " | MST(rem): " << (mstRem < INF ? to_string(mstRem) : "INF");
                    cout << " | New LB: " << newLB << "\n";
                }

                if (newLB <= bestCost) {
                    solveBranch(nextMatrix, path, visited, newLB);
                } else if (DEBUG) {
                    printIndent();
                    cout << "Branch skipped (newLB > best)\n";
                }

                path.pop_back();
                visited[next] = false;
                depth--;
            }
        }
    }

public:
    TSP_Little(const vector<vector<int>>& g) : n(g.size()), bestCost(INF), depth(0) {
        costs = g;
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                if (costs[i][j] == -1) costs[i][j] = INF;
    }

    Result solve(int start = 0) {
        if (DEBUG) {
            cout << "=== Starting Little's Algorithm (Branch & Bound) ===\n";
            cout << "Cities: " << n << "\n";
            cout << "Start vertex: " << start << "\n\n";
        }

        vector<vector<int>> matrix = costs;
        int initialReduction = reduceMatrix(matrix);
        
        if (DEBUG && initialReduction > 0) {
            cout << "Initial matrix reduction: " << initialReduction << "\n\n";
        }

        vector<int> approxPath;
        int approxCost = nearestNeighbor(start, approxPath);
        if (approxCost < INF) {
            bestCost = approxCost;
            bestPath = approxPath;
            if (DEBUG) {
                cout << "ABS heuristic result:\n";
                cout << "  Initial path: ";
                for (int v : approxPath) cout << v << " ";
                cout << "\n  Initial cost: " << approxCost << "\n\n";
            }
        }

        vector<int> path = {start};
        vector<bool> visited(n, false);
        visited[start] = true;

        solveBranch(matrix, path, visited, initialReduction);

        if (DEBUG) {
            cout << "\n=== Search Complete ===\n";
        }

        if (bestCost == INF) return {0, {}, false};
        return {bestCost, bestPath, true};
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<vector<int>> graph(n, vector<int>(n));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            cin >> graph[i][j];

    TSP_Little solver(graph);
    Result res = solver.solve(0);

    if (res.exists) {
        // Output format: path first, then cost with .0
        for (size_t i = 0; i < res.path.size(); ++i) {
            if (i > 0) cout << " ";
            cout << res.path[i];
        }
        cout << "\n";
        cout << fixed << setprecision(1) << (double)res.cost << "\n";
    } else {
        cout << "no path\n";
    }

    return 0;
}
