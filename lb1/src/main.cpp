#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>
#include <chrono>
#include <cstdint>

using namespace std;
using namespace chrono;

int dim;                     //размер столещницы
int record_k = 100;          //текущий рекорд 
uint64_t row_bits[64] = {0}; //битовая маска
vector<tuple<int, int, int>> final_ans; //лучшее решение
vector<tuple<int, int, int>> trail; //текущий путь
steady_clock::time_point t0;
const int TIMEOUT_MS = 2800; //ограничение на время

const int DEBUG = 1;
int recursion_depth = 0;

void print_grid_state() {
    if (!DEBUG) return;
    
    int squares_count = trail.size();
    int empty_count = 0;
    
    vector<vector<int>> grid(dim, vector<int>(dim, 0));
    int idx = 1;
    for (auto& [r, c, s] : trail) {
        for (int i = r - 1; i < r - 1 + s && i < dim; i++) {
            for (int j = c - 1; j < c - 1 + s && j < dim; j++) {
                grid[i][j] = idx;
            }
        }
        idx++;
    }
    
    for (int i = 0; i < dim; i++) {
        for (int j = 0; j < dim; j++) {
            if (grid[i][j] == 0) empty_count++;
        }
    }
    
    cout << "\nSquares: " << squares_count << ", Empty: " << empty_count << endl;
    
    for (int i = 0; i < dim; i++) {
        for (int j = 0; j < dim; j++) {
            cout << grid[i][j] << " ";
        }
        cout << endl;
    }
}
// создание битовой маски для хранения строк
inline uint64_t mask_of(int len, int shift) {
    return ((1ULL << len) - 1) << shift;
}

//проверка на возмощность размещения
bool fits(int r, int c, int sz) {
    if (r + sz > dim || c + sz > dim) return false;
    uint64_t m = mask_of(sz, c);
    
    for (int i = r; i < r + sz; ++i)
        if (row_bits[i] & m) return false;
    return true;
}

//вставка/удаление блоков
void apply_block(int r, int c, int sz, bool on) {
    uint64_t m = mask_of(sz, c);
    for (int i = r; i < r + sz; ++i)
        on ? (row_bits[i] |= m) : (row_bits[i] &= ~m);
}

//Ищем первый пустой квадрат
bool first_hole(int start_r, int start_c, int &r, int &c) {
    for (int j = start_c; j < dim; ++j) {
        if (!((row_bits[start_r] >> j) & 1)) { r = start_r; c = j; return true; }
    }
    
    for (int i = start_r + 1; i < dim; ++i) {
        if (row_bits[i] != (1ULL << dim) - 1) {
            for (int j = 0; j < dim; ++j)
                if (!((row_bits[i] >> j) & 1)) { r = i; c = j; return true; }
        }
    }
    return false;
}
//оценка нижней границы
int lower_bound_est(int rem, int max_side) {
    if (max_side <= 0) return rem;
    return (rem + max_side * max_side - 1) / (max_side * max_side);
}

vector<tuple<int,int,int>> fast_greedy(int n) {
    uint64_t tmp[64] = {0};
    vector<tuple<int,int,int>> res;
    int filled = 0;
    
    while (filled < n * n) {
        int r = -1, c = -1;
        for (int i = 0; i < n && r == -1; ++i)
            for (int j = 0; j < n; ++j)
                if (!((tmp[i] >> j) & 1)) { r = i; c = j; }
        if (r == -1) break;
        
        int lim = min({n - r, n - c, n - 1});
        for (int s = lim; s >= 1; --s) {
            uint64_t m = mask_of(s, c);
            bool ok = true;
            
            for (int i = r; i < r + s; ++i) {
                if (tmp[i] & m) { ok = false; break; }}
            if (ok) {
                for (int i = r; i < r + s; ++i) tmp[i] |= m;
                res.emplace_back(r + 1, c + 1, s);
                filled += s * s;
                break;
            }
        }
    }
    return res;
}

void explore(int cnt, int used, int last_r, int last_c) {
    if (duration_cast<milliseconds>(steady_clock::now() - t0).count() > TIMEOUT_MS) return;
    if (cnt >= record_k) return;

    int r, c;
    if (!first_hole(last_r, last_c, r, c)) {
        if (cnt < record_k) {
            record_k = cnt;
            final_ans = trail;
        }
        return;
    }

    if (DEBUG) {
        recursion_depth++;
        cout << "\nExtracting a new state from the stack:" << endl;
        print_grid_state();
        
        int rem_h = dim - r;
        int rem_w = dim - c;
        int max_sz = min({rem_h, rem_w, dim - 1});
        cout << "We start with the cell (" << (r+1) << "," << (c+1) << "), we try sizes from " 
             << max_sz << " to " << max_sz << endl;
    }

    int rem_h = dim - r;
    int rem_w = dim - c;
    int max_sz = min({rem_h, rem_w, dim - 1});
    int left = dim * dim - used;

    if (max_sz == 1) {
        if (DEBUG) {
            cout << "Heuristic: immediately " << left << "  squares (1x1). We put the new state on the stack." << endl;
        }
        
        if (cnt + left < record_k) {
            for (int i = 0; i < dim; i++){
                for (int j = 0; j < dim; j++){
                    if (!((row_bits[i] >> j) & 1)) {
                        trail.emplace_back(i + 1, j + 1, 1);
                    }
                }
            }
            record_k = cnt + left;
            final_ans = trail;
        }
        if (DEBUG) recursion_depth--;
        return;
    }
    

    int min_req = lower_bound_est(left, max_sz);
    if (cnt + min_req >= record_k) {
        if (DEBUG) {
            cout << "\nAssessment compartments. Even filling in the best possible way can't improve the record." << endl;
        }
        if (DEBUG) recursion_depth--;
        return;
    }
    if (rem_h == 1 || rem_w == 1) {
        if (cnt + left >= record_k) {
            if (DEBUG) recursion_depth--;
            return;
        }
    }

    for (int s = max_sz; s >= 1; --s) {
        if (s == 1 && max_sz > 3 && cnt + 1 >= record_k) continue;
        
        if (fits(r, c, s)) {
            if (DEBUG) {
                cout << "square " << s << "x" << s << " in (" << (r+1) << "," << (c+1) << "). ";
                cout << "We put the new state on the stack." << endl;
                
                int new_left = left - s * s;
                int new_min_req = lower_bound_est(new_left, max_sz);
                if (new_min_req > 0) {
                    cout << "Heuristic: immediately " << new_min_req << " square (" << s << "x" << s;
                    if (new_min_req > 1) {
                        cout << ", 1x1, 1x1";
                    }
                    cout << "). We put the new state on the stack." << endl;
                }
            }
            
            apply_block(r, c, s, true);
            trail.emplace_back(r + 1, c + 1, s);
            
            explore(cnt + 1, used + s * s, r, c);
            
            if (DEBUG) {
                cout << "Return (removing the square " << s << "x" << s << ")" << endl;
            }
            trail.pop_back();
            apply_block(r, c, s, false);
        }
    }
    if (DEBUG) recursion_depth--;
}

bool try_patterns() {
    if (dim > 2 && dim % 2 == 0) {
        int h = dim / 2;
        record_k = 4;
        final_ans = {{1,1,h}, {1,h+1,h}, {h+1,1,h}, {h+1,h+1,h}};
        
        if (DEBUG) {
            cout << "\nThe pattern: N is a multiple of 2 -> 2x2" << endl;
            cout << "\nInitial approximation (record): " << record_k << " squares" << endl;
            cout << "\nExtracting a new state from the stack:" << endl;
            
            vector<vector<int>> grid(dim, vector<int>(dim, 0));
            int idx = 1;
            for (auto& [r, c, s] : final_ans) {
                for (int i = r - 1; i < r - 1 + s && i < dim; i++) {
                    for (int j = c - 1; j < c - 1 + s && j < dim; j++) {
                        grid[i][j] = idx;
                    }
                }
                idx++;
            }
            
            cout << "\nSquares: " << final_ans.size() << ", Empty: 0" << endl;
            for (int i = 0; i < dim; i++) {
                for (int j = 0; j < dim; j++) {
                    cout << grid[i][j] << " ";
                }
                cout << endl;
            }
            cout << endl;
        }
        
        return true;
    }

    if (dim > 3 && dim % 3 == 0) {
        int t = dim / 3;
        record_k = 6;
        final_ans = {
            {1, 1, 2*t}, {2*t+1, 1, t}, {1, 2*t+1, t},
            {2*t+1, 2*t+1, t}, {2*t+1, t+1, t}, {t+1, 2*t+1, t}
        };
        if (DEBUG) {
            cout << "\nThe pattern: N is a multiple of 3 -> 3x3" << endl;
            cout << "\nInitial approximation (record): " << record_k << " squares" << endl;
            cout << "\nExtracting a new state from the stack:" << endl;
            
            vector<vector<int>> grid(dim, vector<int>(dim, 0));
            int idx = 1;
            for (auto& [r, c, s] : final_ans) {
                for (int i = r - 1; i < r - 1 + s && i < dim; i++) {
                    for (int j = c - 1; j < c - 1 + s && j < dim; j++) {
                        grid[i][j] = idx;
                    }
                }
                idx++;
            }
            
            cout << "\nSquares: " << final_ans.size() << ", Empty: 0" << endl;
            for (int i = 0; i < dim; i++) {
                for (int j = 0; j < dim; j++) {
                    cout << grid[i][j] << " ";
                }
                cout << endl;
            }
            cout << endl;
        }
        return true;
    }
    if (dim > 5 && dim % 5 == 0) {
        int f = dim / 5;
        record_k = 8;
        final_ans = {
            {1, 1, 3*f}, {3*f+1, 1, 2*f}, {1, 3*f+1, 2*f},
            {3*f+1, 3*f+1, 2*f}, {3*f+1, 2*f+1, f}, {4*f+1, 2*f+1, f},
            {2*f+1, 3*f+1, f}, {2*f+1, 4*f+1, f}
        };
        if (DEBUG) {
            cout << "\nThe pattern: N is a multiple of 5 -> 5x5" << endl;
            cout << "\nInitial approximation (record): " << record_k << " squares" << endl;
            cout << "\nExtracting a new state from the stack:" << endl;
            
            vector<vector<int>> grid(dim, vector<int>(dim, 0));
            int idx = 1;
            for (auto& [r, c, s] : final_ans) {
                for (int i = r - 1; i < r - 1 + s && i < dim; i++) {
                    for (int j = c - 1; j < c - 1 + s && j < dim; j++) {
                        grid[i][j] = idx;
                    }
                }
                idx++;
            }
            
            cout << "\nSquares: " << final_ans.size() << ", Empty: 0" << endl;
            for (int i = 0; i < dim; i++) {
                for (int j = 0; j < dim; j++) {
                    cout << grid[i][j] << " ";
                }
                cout << endl;
            }
            cout << endl;
        }
        return true;
    }
    return false;
}


int main() {
    cout << "~~~~~~~==========~~~~~~~"<< "\n";
    cout << "        ~Lab 1~"<< "\n";
    cout << "~~~~~~~==========~~~~~~~"<< "\n";
    cout << "Enter the size of the tabletop: ";

    ios::sync_with_stdio(false);
    int n;
    if (!(cin >> n)) return 0;
    dim = n;
    t0 = steady_clock::now(); //засекаем время
    
    if (try_patterns()) { //пробуем готовые решения
        cout << record_k << "\n";
        for (auto &[x, y, w] : final_ans) cout << x << " " << y << " " << w << "\n";
        return 0;
    }

    auto guess = fast_greedy(n); //задаём верхнюю границу для отсечений с помощью жадного алгоритма
    record_k = guess.size();
    final_ans = guess;

    if (DEBUG) {
        cout << "Initial approximation (record): " << record_k << " squares" << endl;
    }

    int s1 = n / 2 + 1;
    int s2 = s1 - 1;
    apply_block(0, 0, s1, true); trail.emplace_back(1, 1, s1);
    apply_block(s1, 0, s2, true); trail.emplace_back(s1 + 1, 1, s2);
    apply_block(0, s1, s2, true); trail.emplace_back(1, s1 + 1, s2);

    explore(3, s1*s1 + 2*s2*s2, 0, 0);

    
    cout << "\nResults:"<< "\n";
    cout << record_k << "\n";
    for (auto &[x, y, w] : final_ans) {
        cout << x << " " << y << " " << w << "\n";
    }
    return 0;
}
