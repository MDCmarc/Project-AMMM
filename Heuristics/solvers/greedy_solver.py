from .base_solver import BaseSolver
from typing import List

import math


class Greedy(BaseSolver):

    def GreedyCostFunction(self, candidate: int, candidates: List[int], solution: List[int],
                           assigned_count: int) -> float:
        """
        Computes the cost (score) of assigning a `candidate` to the solution.
        """

        def PenalizedAffinity(value: float) -> float:
            """
            Applies a penalty or boost to affinity values.
            """
            if value < 0.15:
                return -math.exp((0.15 - value) * 2)  # Strong penalty for poor affinity
            elif value >= 0.85:
                return value + math.exp((value - 0.85) * 2)  # Boost for strong affinity
            return value

        sum_solution = sum(PenalizedAffinity(self.m[candidate][i]) for i in solution if i != -1)

        sum_candidates = sum(PenalizedAffinity(self.m[candidate][i]) for i in candidates if i != candidate)

        progress_ratio = assigned_count / self.sumN
        score = progress_ratio * sum_solution + (1 - progress_ratio) * sum_candidates
        return score

    def NeedsMiddlemanAndNotFound(self, candidate: int, candidates: List[int], solution: List[int]) -> bool:
        """
        Checks if `candidate` is incompatible with the current solution and if no middleman 
        (future or present) can resolve this incompatibility.
        """
        incompatibles = [i for i in solution if self.m[candidate][i] < 0.15 and i != -1]

        if not incompatibles:
            return False

        return not all(
            self.MiddlemanRestrictionHolds(solution, problem, candidate) or
            self.MiddlemanRestrictionHolds(candidates, problem, candidate)
            for problem in incompatibles
        )

    def FeasibilityFunction(self, candidates: List[int], n: List[int], solution: List[int]) -> List[int]:
        """
        Filters out incompatible candidates based on group space availability and incompatibility with the solution.
        """
        return [
            candidate for candidate in candidates
            if n[self.d[candidate] - 1] > 0 and
            not self.CandidateIncompatible(candidate, solution) and
            not self.NeedsMiddlemanAndNotFound(candidate, candidates, solution)
        ]

    def Solve(self) -> tuple[float, List[int]]:
        """
        Solves the optimization problem using a greedy algorithm.
        """
        candidates = list(range(self.N))
        solution = [-1] * self.sumN
        n = self.n.copy()
        assigned_count = 0

        while assigned_count < self.sumN:
            candidates = self.FeasibilityFunction(candidates, n, solution)

            if not candidates:
                break

            # Choose the best candidate
            best_candidate = max(candidates,
                                 key=lambda x: self.GreedyCostFunction(x, candidates, solution, assigned_count))

            # Assign candidate to the solution
            solution[assigned_count] = best_candidate
            candidates.remove(best_candidate)

            n[self.d[best_candidate] - 1] -= 1
            assigned_count += 1

        return self.CheckAndReturnSolution(solution, output=True)
