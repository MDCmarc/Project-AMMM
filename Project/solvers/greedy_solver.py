from .base_solver import BaseSolver
from typing import List

import math

class Greedy(BaseSolver):

    def GreedyCostFunction(self, candidate: int, candidates: List[int], solution: List[int], assigned_count: int) -> float:
        """
        Computes the cost (score) of assigning a `candidate` to the solution.
        """
        def PenalizedAffinity(value: float) -> float:
            """
            Applies a penalty or boost to affinity values.
            """
            if value < 0.15:
                return -math.exp((0.15 - value)*2)  # Strong penalty for poor affinity
            elif value >= 0.85:
                return value + math.exp((value-0.85)*2)  # Boost for strong affinity
            return value

        sum_solution = sum(PenalizedAffinity(self.m[candidate][i]) for i in solution if i != -1)
        
        sum_candidates = sum(PenalizedAffinity(self.m[candidate][i]) for i in candidates if i != candidate)

        progress_ratio = assigned_count / self.sumN
        score = progress_ratio * sum_solution + (1 - progress_ratio) * sum_candidates
        return score

    
    def SortCandidates(self, candidates: List[int], solution: List[int], assigned_count: int) -> List[int]:
        """
        Sorts candidates based on the greedy cost function in descending order.
        """
        return sorted(candidates, 
            key=lambda x: self.GreedyCostFunction(x, candidates, solution, assigned_count),
            reverse=True
        )
    

    def NeedsMiddlemanAndNotFound(self, candidate: int, candidates: List[int], solution: List[int]) -> bool:
        """
        Checks if `candidate` is incompatible with the current solution and if no middleman 
        (future or present) can resolve this incompatibility.
        """
        incompatibles = [i for i in solution if i != -1 and self.m[candidate][i] < 0.15]

        if not incompatibles:
            return False

        def HasMiddleman(problem: int) -> bool:
            """
            Checks if there is a middleman in the solution or candidates that resolves 
            the incompatibility between `problem` and `candidate`.
            """
            if any(self.m[problem][i] > 0.85 and self.m[i][candidate] > 0.85 for i in solution if i != -1):
                return True
            return any(
                self.m[problem][i] > 0.85 and self.m[i][candidate] > 0.85
                for i in candidates
            )

        return not all(HasMiddleman(problem) for problem in incompatibles)    


    def PurgeCandidates(self, candidates: List[int], spaces_in_groups: List[int], solution: List[int]) -> List[int]:
        """
        Filters out incompatible candidates based on group space availability and incompatibility with the solution.
        """
        return [
            candidate for candidate in candidates
            if spaces_in_groups[self.d[candidate] - 1] > 0 and
            not self.CandidateIncompatible(candidate, solution) and
            not self.NeedsMiddlemanAndNotFound(candidate, candidates, solution)
        ]
    

    def Solve(self) -> List[int]:
        """
        Solves the optimization problem using a greedy algorithm.
        """
        candidates = list(range(self.N))
        solution = [-1]*self.sumN
        spaces_in_groups = self.n.copy()
        assigned_count = 0
 
        while assigned_count < self.sumN:
            filtered_candidates = self.PurgeCandidates(candidates, spaces_in_groups, solution)

            if not filtered_candidates:
                break
            
            candidates = self.SortCandidates(filtered_candidates, solution, assigned_count)

            # Choose the best candidate
            selected_candidate = candidates.pop(0)

            # Assign candidate to the solution
            group_index = self.d[selected_candidate] - 1
            solution[assigned_count] = selected_candidate
            spaces_in_groups[group_index] -= 1
            assigned_count += 1

        return self.CheckAndReturnSolution(solution, output=True)
        