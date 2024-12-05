import time
import random

from .base_solver import BaseSolver
from .local_search import LocalSearch
from .greedy_solver import Greedy

from typing import List


class GRASP(BaseSolver):
    def __init__(self, D, N, n, d, m, alpha=0.7):
        super().__init__(D, N, n, d, m)
        self.greedy_solver = Greedy(D, N, n, d, m)
        self.local_search_solver = LocalSearch(D, N, n, d, m)
        self.alpha = alpha
        print(self.alpha)

    def ConstructRCL(self, candidates: List[int], solution: List[int], assigned_count: int) -> List[int]:
        """
        Select the top candidates based on their greedy cost function score and the alpha parameter.
        """
        candidates_with_scores = [
            (candidate, self.greedy_solver.GreedyCostFunction(candidate, candidates, solution, assigned_count))
            for candidate in candidates
        ]

        # Take max and minimum from the sorted candidates. They are pairs (candidate,score).
        sorted_candidates = sorted(candidates_with_scores, key=lambda x: x[1], reverse=True)
        q_max = sorted_candidates[0][1]
        q_min = sorted_candidates[-1][1]

        threshold = q_max - self.alpha * (q_max - q_min)  # We are doing a RCL_max

        RCL = [candidate for candidate, score in sorted_candidates if score >= threshold]

        return RCL

    def DoConstructionPhase(self):
        """
        Generates a GRASP solution with a variation of the greedy. It selects the candidate randomly from the RCL.
        """
        candidates = list(range(self.N))
        solution = [-1] * self.sumN
        n = self.n.copy()
        assigned_count = 0

        while assigned_count < self.sumN:
            candidates = self.greedy_solver.FeasibilityFunction(candidates, n, solution)

            if not candidates:
                break

            # Randomly choose a candidate from the top candidates
            RCL = self.ConstructRCL(candidates, solution, assigned_count)
            selected_candidate = random.choice(RCL)

            # Assign candidate to the solution
            solution[assigned_count] = selected_candidate
            candidates.remove(selected_candidate)

            n[self.d[selected_candidate] - 1] -= 1
            assigned_count += 1

        return self.CheckAndReturnSolution(solution, output=False)[1]

    def Solve(self, max_iterations=100, max_time=500) -> tuple[float, List[int]]:
        """
        Solves the optimization problem using a greedy algorithm.
        The default parameters are 200 iterations and 500 seconds.
        """
        start_time = time.time()
        best_solution, best_fitness = ([], -1)

        for iteration in range(max_iterations):
            if time.time() - start_time >= max_time:
                print(f"Terminating search after {iteration} iterations and {time.time() - start_time:.2f} seconds.")
                break

            new_solution = self.DoConstructionPhase()
            if not new_solution:
                continue

            new_fitness, new_solution = self.local_search_solver.Solve(new_solution, output=False)

            if new_fitness > best_fitness:
                best_solution, best_fitness = new_solution, new_fitness

        return self.CheckAndReturnSolution(best_solution, output=True)
