class GreedySolver:
    def __init__(self, D, N, n, d, m):
        self.D = D
        self.N = N
        self.n = n
        self.sumN = sum(n)
        self.d = d
        self.m = m
        self.solution = [-1] * self.sumN

    def fitness(self, sol):
        average = 0
        for i in range(self.sumN):
            for j in range(i + 1, self.sumN):
                average += self.m[sol[i]][sol[j]]
        average /= (self.sumN*(self.sumN-1)/2)
        return average

    def sort_group(self, group):
        # Sorting group using the custom sort function
        # We penalize those assigments that have <0.15 with anyone , the less afinity they have, the more we penalise -[0,0.15]
        group.sort(key=lambda x: sum(
                                    -(0.15 - ma) if ma < 0.15 
                                    else ma 
                                    for ma in self.m[x]), reverse=True)

        # print("Sort:", " ".join(str(s + 1) for s in group))

    def possible(self, solution, candidate):
        for s in solution:
            if s < 0:
                break
            if self.m[candidate][s] <= 0:
                return False
        return True

    def solve(self):

        a = list(range(0, self.N))
        spaces_in_groups = self.n
        self.sort_group(a)
        number = 0

        for i in range(len(a)):
            if number >= self.sumN:
                break
            if self.possible(self.solution, a[i]):
                group_of_i = self.d[a[i]]-1
                if self.n[group_of_i] and spaces_in_groups[group_of_i] > 0:
                    spaces_in_groups[group_of_i] -= 1
                    self.solution[number] = a[i]
                    # print(f" Added: {a[i] + 1}")
                    number += 1

        # Final check
        if number != self.sumN:
            print(f" Could not complete the solution with {self.sumN} elements.")

    def found(self, i, j):
        for k in range(self.sumN):
            if self.m[self.solution[i]][self.solution[k]] > 0.85 and self.m[self.solution[k]][self.solution[j]] > 0.85:
                return True
        return False

    def print_solution(self):
        for i in range(self.sumN):
            for j in range(i + 1, self.sumN):
                if self.m[self.solution[i]][self.solution[j]] < 0.15:
                    if not self.found(i, j):
                        print(f" Could not complete the solution with {self.sumN} elements.")
                        return

        print(f"OBJECTIVE: {self.fitness(self.solution)}")
        print("Commission:", " ".join(str(s + 1) for s in self.solution))
