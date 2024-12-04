from .base_solver import BaseSolver
from typing import List

import math

class Greedy(BaseSolver):

    def greedyCostFunction(self, candidate: int, 
                            candidates: List[int],
                            solution: List[int],
                            assigned_count: int) -> float:

        def penalizedAffinity(value: float) -> float:
            if value < 0.15:
                return -math.exp((0.15 - value)*2)  # Strong penalty for poor affinity
            elif value >= 0.85:
                return value + math.exp((value-0.85)*2)  # Boost for strong affinity
            return value

        sum1 = sum(penalizedAffinity(self.m[candidate][i])
                    for i in solution if i != -1)
        
        sum2 = sum(penalizedAffinity(self.m[candidate][i])
                    for i in candidates if i != candidate)

        progress_ratio = assigned_count / self.sumN
        weight_sum1 = progress_ratio
        weight_sum2 = 1 - progress_ratio

        score = weight_sum1 * sum1 + weight_sum2 * sum2

        return score

    def purgeCandidates(self, candidates: List[int], 
                         spaces_in_groups: List[int],
                         solution: List[int] ) -> List[int]:
        """Filter out incompatible candidates."""
        return [
            candidate for candidate in candidates
            if spaces_in_groups[self.d[candidate] - 1] > 0 and
            self.candidateNoIncompatible(candidate, solution) and
            not self.needsMiddlemanAndNotFound(candidate, candidates, solution)
        ]

    def needsMiddlemanAndNotFound(self, candidate: int, 
                                  candidates: List[int],
                                  solution: List[int]) -> bool:
        incompatibles = [i for i in solution if i != -1 and self.m[candidate][i] < 0.15]

        if not incompatibles:
            return False

        def incompatibilityFixed(problem: int) -> bool:
            for i in solution:      # Check for a middleman in the current solution
                if i == -1:
                    break
                if self.m[problem][i] > 0.85 and self.m[i][candidate] > 0.85:
                    return True
            return any(
                self.m[problem][i] > 0.85 and self.m[i][candidate] > 0.85
                for i in candidates
            )

        return not all(incompatibilityFixed(problem) for problem in incompatibles)    


    def sortCandidates(self, candidates: List[int],
                         solution: List[int],
                         assigned_count: int) -> List[int]:
        """Sort based on the greedy cost function."""
        return sorted(candidates, 
            key=lambda x: self.greedyCostFunction(x, candidates, solution, assigned_count),
            reverse=True
        )


    def solve(self) -> List[int]:
        candidates = list(range(self.N))
        solution = [-1]*self.sumN
        spaces_in_groups = self.n.copy()
        assigned_count = 0
 
        while assigned_count < self.sumN:
            filtered_candidates = self.purgeCandidates(candidates, spaces_in_groups, solution)

            if not filtered_candidates:
                break
            
            candidates = self.sortCandidates(filtered_candidates, solution, assigned_count)

            selected_candidate = candidates.pop(0)
            group_index = self.d[selected_candidate] - 1

            solution[assigned_count] = selected_candidate
            spaces_in_groups[group_index] -= 1
            assigned_count += 1

        return self.checkAndReturnSolution(solution)
        