#include <vector>
#include <numeric>
#include <algorithm>
#include <iostream>

class GreedySolver {
private:
    int D; 
    int N; 
    std::vector<int> n;
    std::vector<int> d;
    std::vector<std::vector<double>> m;
    std::vector<int> solution;

public:
    GreedySolver(int D, int N, const std::vector<int>& n, const std::vector<int>& d, const std::vector<std::vector<double>>& m)
        : D(D), N(N), n(n), d(d), m(m), solution(5,-1) {}


    double Fitness(const std::vector<int>& sol) const {
        double average = 0;
        for (size_t i = 0; i < 5; ++i) {
            for (size_t j = i + 1; j < 5; ++j) {
                average += m[sol[i]][sol[j]];
            }
        }
        average /= 10;
        return average;
    }

    void SortGroup(std::vector<int>& group) const {
        auto sort_func = [this](int a1, int a2) {
            double sum1 = -1;
            for(auto m_a : m[a1]){
                if(m_a < 0.15) sum1-=(0.15-m_a);  
                 sum1+=m_a;
            }
            
            double sum2 = -1;
            for(auto m_a : m[a2]){
                if(m_a < 0.15) sum2-=(0.15-m_a);  
                sum2+=m_a;
            }
            return sum1 > sum2; // The higher the value the better
        };
        std::sort(group.begin(), group.end(), sort_func);
        
        std::cout << "Sort: ";
        for (auto s : group) {
            std::cout << s+1 << " ";
        }
        std::cout << std::endl;
    }

    bool possible(const std::vector<int>& solution, int candidate) {
        for (const auto& s : solution) {
            if (s < 0) continue;
            if (m[candidate][s] <= 0) return false;
        }
        return true;
    }

    void Solve() {
        std::vector<int> a = {0, 1, 2, 3, 4, 5, 6, 7};
        int g1 = 2;
        int g2 = 3;

        SortGroup(a);
        int number = 0;
        
        for (int i = 0; i < a.size() && number < 5; ++i) {
            if (possible(solution, a[i])) {
                if(a[i] <= 2 && g1 > 0) {
                    --g1;                       
                    solution[number] = a[i];
                    std::cout << " Added: "<< a[i]+1<< "\n";
                    ++number;
                }
                else if(a[i] > 2 && g2 > 0) {
                    --g2;
                    solution[number] = a[i];
                    std::cout << " Added: "<< a[i]+1<< "\n";
                    ++number;
                }
            }
        }


        /**
        if (number != 3) {
            std::cerr << "Could not fill solution with 3 elements from a1.\n";
            exit(0);
        }

        for (int i = 0; i < a2.size() && number < 6; ++i) {
            if (possible(solution, a2[i])) {
                solution[number] = a2[i];
                ++number;
            }
        }
            */
        // Final check
        if(number != 5){
            std::cerr << "Could not complete the solution with 6 elements.\n";
            exit(0);
        }
    }


    bool found(int i, int j) const {
        for(int k = 0 ; k < 5 ; ++k ){
            if(m[solution[i]][solution[k]] > 0.85  
                && m[solution[k]][solution[j]]) return true;
        }
        return false;
    }

    void PrintSolution() const {

        for(int i = 0 ; i < 5 ; ++i) {
            for ( int j = i+1 ; j < 5 ; ++j){
                if(m[solution[i]][solution[j]] < 0.15){
                    if(!found(i,j) ){
                        std::cerr << "Could not complete the solution with 6 elements.\n";
                        exit(0);
                    }
                }
            }
        }

        std::cout << "Solution: ";
        for (auto s : solution) {
            std::cout << s+1 << " ";
        }
        std::cout << "\nFitness: " << Fitness(solution) << std::endl;
    }
};

int main() {
    /**  Instance 1
    int D = 2;
    std::vector<int> n = {3, 3};
    int N = 8;
    std::vector<int> d = {1, 1, 1, 1, 2, 2, 2, 2};
    std::vector<std::vector<double>> m = {
        {1.00, 0.50, 0.75, 0.90, 0.15, 0.40, 1.00, 0.90},
        {0.50, 1.00, 0.00, 0.00, 0.60, 0.80, 1.00, 0.00},
        {0.75, 0.00, 1.00, 0.25, 0.55, 0.75, 1.00, 0.60},
        {0.90, 0.00, 0.25, 1.00, 0.40, 0.20, 1.00, 0.10},
        {0.15, 0.60, 0.55, 0.40, 1.00, 0.15, 1.00, 0.15},
        {0.40, 0.80, 0.75, 0.20, 0.15, 1.00, 1.00, 0.20},
        {1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00},
        {0.90, 0.00, 0.60, 0.10, 0.15, 0.20, 1.00, 1.00}
    };
    */

    /** Instance 2
    // Define constants
    const int D = 2;
    std::vector<int> n = {3, 3};

    const int N = 8;
    std::vector<int> d = {1, 1, 1, 1, 2, 2, 2, 2};

    // Define the matrix
    std::vector<std::vector<double>> m = {
        {1.00, 0.50, 0.75, 0.90, 0.15, 0.40, 0.50, 0.90},
        {0.50, 1.00, 0.00, 0.00, 0.60, 0.80, 0.50, 0.00},
        {0.75, 0.00, 1.00, 0.25, 0.55, 0.75, 0.50, 0.60},
        {0.90, 0.00, 0.25, 1.00, 0.40, 0.20, 0.50, 0.10},
        {0.15, 0.60, 0.55, 0.40, 1.00, 0.15, 0.50, 0.15},
        {0.40, 0.80, 0.75, 0.20, 0.15, 1.00, 0.50, 0.20},
        {0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 1.00, 0.50},
        {0.90, 0.00, 0.60, 0.10, 0.15, 0.20, 0.50, 1.00}
    };
     */

    const int D = 2;
    std::vector<int> n = {2, 3};

    const int N = 8;
    std::vector<int> d = {1, 1, 1, 1, 2, 2, 2, 2};

    // Define the matrix
    std::vector<std::vector<double>> m = {
        {1.00, 0.50, 0.75, 0.80, 0.10, 0.40, 0.50, 0.80},
        {0.50, 1.00, 0.00, 0.00, 0.60, 0.80, 0.50, 0.00},
        {0.75, 0.00, 1.00, 0.25, 0.55, 0.75, 0.50, 0.60},
        {0.80, 0.00, 0.25, 1.00, 0.40, 0.20, 0.50, 0.10},
        {0.10, 0.60, 0.55, 0.40, 1.00, 0.15, 0.50, 0.15},
        {0.40, 0.80, 0.75, 0.20, 0.15, 1.00, 0.50, 0.20},
        {0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 1.00, 0.50},
        {0.80, 0.00, 0.60, 0.10, 0.15, 0.20, 0.50, 1.00}
    };

    GreedySolver solver(D, N, n, d, m);

    solver.Solve();
    solver.PrintSolution();

    return 0;
}
