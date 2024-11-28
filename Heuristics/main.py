


class GreedySolver:
    def __init__(self, D, N, n, d, m):
        self.D = D
        self.N = N
        self.n = n
        self.sumN = sum(n)
        self.d = d
        self.m = m
        self.solution = [-1] * 5

    def fitness(self, sol):
        average = 0
        for i in range(self.sumN):
            for j in range(i + 1, self.sumN):
                average += self.m[sol[i]][sol[j]]
        average /= 10
        return average

    def sort_group(self, group):
        def sort_func(a1, a2):
            sum1 = -1
            for m_a in self.m[a1]:
                if m_a < 0.15:
                    sum1 -= (0.15 - m_a)
                sum1 += m_a

            sum2 = -1
            for m_a in self.m[a2]:
                if m_a < 0.15:
                    sum2 -= (0.15 - m_a)
                sum2 += m_a

            return sum1 > sum2  # The higher the value, the better
        
        # Sorting group using the custom sort function
        group.sort(key=lambda x: sum(-1 if ma < 0.15 else ma + (ma < 0.15) * (0.15 - ma) for ma in self.m[x]), reverse=True)

        print("Sort:", " ".join(str(s + 1) for s in group))

    def possible(self, solution, candidate):
        for s in solution:
            if s < 0:
                continue
            if self.m[candidate][s] <= 0:
                return False
        return True

    def solve(self):

        a = list(range(0, N-1))
        spaces_in_groups = n
        ranges_in_groups = [[0, 0] for _ in range(len(n))]
        ranges_in_groups[0] = [0, n[0] - 1]
        for i in range(1, len(n)):
            ranges_in_groups[i] = [ranges_in_groups[i-1][1]+1, ranges_in_groups[i-1][1]+n[i]]
        
        print("Ranges in groups:")
        print(ranges_in_groups)


        self.sort_group(a)
        number = 0

        for i in range(len(a)):
            if number >= self.sumN:
                break
            if self.possible(self.solution, a[i]):
                for j in range(0, len(n)-1):
                    if (a[i] >= ranges_in_groups[j][0] and a[i] <= ranges_in_groups[j][1]) and spaces_in_groups[i] > 0:
                        spaces_in_groups[i] -= 1
                        self.solution[number] = a[i]
                        print(f" Added: {a[i] + 1}")
                        number += 1

        # Final check
        if number != self.sumN:
            raise RuntimeError("Could not complete the solution with " + self.sumN + " elements.")

    def found(self, i, j):
        for k in range(self.sumN):
            if self.m[self.solution[i]][self.solution[k]] > 0.85 and self.m[self.solution[k]][self.solution[j]] > 0.85:
                return True
        return False

    def print_solution(self):
        for i in range(5):
            for j in range(i + 1, self.sumN):
                if self.m[self.solution[i]][self.solution[j]] < 0.15:
                    if not self.found(i, j):
                        raise RuntimeError("Could not complete the solution with 5 elements.")

        print("Solution:", " ".join(str(s + 1) for s in self.solution))
        print(f"Fitness: {self.fitness(self.solution)}")


if __name__ == "__main__":

    # values we want to comute from
    D = 2  # Number of dimensions
    n = [2, 3]  # Number of elements in each dimension
    N = 8  # Total number of elements
    d = [1, 1, 1, 1, 2, 2, 2, 2]  # Dimension indices for each element
    m = [
        [1.00, 0.50, 0.75, 0.90, 0.15, 0.40, 1.00, 0.90],
        [0.50, 1.00, 0.00, 0.00, 0.60, 0.80, 1.00, 0.00],
        [0.75, 0.00, 1.00, 0.25, 0.55, 0.75, 1.00, 0.60],
        [0.90, 0.00, 0.25, 1.00, 0.40, 0.20, 1.00, 0.10],
        [0.15, 0.60, 0.55, 0.40, 1.00, 0.15, 1.00, 0.15],
        [0.40, 0.80, 0.75, 0.20, 0.15, 1.00, 1.00, 0.20],
        [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
        [0.90, 0.00, 0.60, 0.10, 0.15, 0.20, 1.00, 1.00],
    ]

    solver = GreedySolver(D, N, n, d, m)
    solver.solve()
    solver.print_solution()