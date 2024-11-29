import math
from typing import List


class GreedySolver:
    def __init__(self, D, N, n, d, m):
        self.D = D
        self.N = N
        self.n = n
        self.d = d
        self.m = m
        self.sumN = sum(n)
        self.solution = [-1] * self.sumN
        self.gaussSum = (self.sumN * (self.sumN - 1) / 2)
        self.assigned_count = 0

    def fitness(self, sol: List[int]) -> float:
        average = 0
        for i in range(self.sumN):
            for j in range(i + 1, self.sumN):
                average += self.m[sol[i]][sol[j]]

        return average / self.gaussSum

    def possible(self, candidate: int) -> bool:
        for s in self.solution:
            if s < 0:
                break
            if self.m[candidate][s] <= 0:
                return False
        return True


    def needs_and_not_found_middleman(self, candidate: int, candidates: List[int]) -> bool:
        incompatibles = [i for i in self.solution if i != -1 and self.m[candidate][i] < 0.15]

        if not incompatibles:
            return False

        def incompatibility_fixed(problem: int) -> bool:
            for i in self.solution:      # Check for a middleman in the current solution
                if i == -1:
                    break
                if self.m[problem][i] > 0.85 and self.m[i][candidate] > 0.85:
                    return True
            return any(
                self.m[problem][i] > 0.85 and self.m[i][candidate] > 0.85
                for i in candidates
            )

        return not all(incompatibility_fixed(problem) for problem in incompatibles)

    def calculate_score(self, candidate: int, candidates: List[int]) -> float:
        def penalized_affinity(value: float) -> float:
            if value < 0.15:
                return -math.exp((0.15 - value)*2)  # Strong penalty for poor affinity
            elif value >= 0.85:
                return value + math.exp((value-0.85)*2)  # Boost for strong affinity
            return value

        sum1 = sum(penalized_affinity(self.m[candidate][i])
                    for i in self.solution if i != -1)
        
        sum2 = sum(penalized_affinity(self.m[candidate][i])
                    for i in candidates if i != candidate)

        progress_ratio = (self.assigned_count / max(1, self.sumN))  # Progress from 0 to 1

        weight_sum1 = progress_ratio
        weight_sum2 = (1 - progress_ratio)

        score = weight_sum1 * sum1 + weight_sum2 * sum2

        #print(f"Candidate {candidate} has a score of: {score} (sum1: {sum1}, sum2: {sum2}, "
        #    f"weight_sum1: {weight_sum1:.2f}, weight_sum2: {weight_sum2:.2f})")

        return score
        
    def purge_and_resort(self, candidates: List[int], spaces_in_groups: List[int]) -> List[int]:
        candidates = [
            candidate for candidate in candidates 
            if spaces_in_groups[self.d[candidate] - 1] > 0 and 
            self.possible(candidate) and
            not self.needs_and_not_found_middleman(candidate, candidates)
        ]

        # Re-sort
        return sorted(candidates, 
            key=lambda x: self.calculate_score(x, candidates),
            reverse=True
        )

    def solve2(self) -> None:
        candidates = list(range(self.N))  # Initialize the candidate list
        spaces_in_groups = self.n
        self.assigned_count = 0
 
        while self.assigned_count < self.sumN:
            candidates = self.purge_and_resort(candidates, spaces_in_groups)
            #print(candidates)
            if not candidates:
                break

            selected_candidate = candidates.pop(0)
            group_index = self.d[selected_candidate] - 1

            self.solution[self.assigned_count] = selected_candidate
            spaces_in_groups[group_index] -= 1
            self.assigned_count += 1

    def print_solution(self) -> None:
        if self.solution[-1] == -1:
            print(f"An assignment of {self.sumN} elements could not be constructed.")
            return

        def middleman_restriction_holds(i: int, j: int) -> bool:
            return any(
                self.m[i][k] > 0.85 and self.m[k][j] > 0.85
                for k in self.solution
            )

        for i in range(self.sumN):
            for j in range(i + 1, self.sumN):
                if self.m[self.solution[i]][self.solution[j]] < 0.15:
                    if not middleman_restriction_holds(i, j):
                        print("An assigment was found but the middleman restriction was not met")
                        return

        self.solution.sort()
        print(f"OBJECTIVE: {self.fitness(self.solution)}")
        print("Commission:", " ".join(str(s + 1) for s in self.solution))