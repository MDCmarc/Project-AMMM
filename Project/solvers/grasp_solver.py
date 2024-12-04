import time
import random

from .base_solver import BaseSolver
from .local_search import LocalSearch
from .greedy_solver import Greedy


from typing import List


class GRASP(BaseSolver):
    def __init__(self, D, N, n, d, m):
        super().__init__(D, N, n, d, m)
        self.greedy_solver = Greedy(D, N, n, d, m)
        self.local_search_solver = LocalSearch(D, N, n, d, m)
        self.alpha = 0.7

    
    def SelectTopCandidates(self, candidates: List[int], solution: List[int], assigned_count: int) -> List[int]:
        """
        Select the top candidates based on their greedy cost function score and the alpha parameter.
        """
        candidates_with_scores = [
            (candidate, self.greedy_solver.GreedyCostFunction(candidate, candidates, solution, assigned_count)) 
            for candidate in candidates
        ]
        
        sorted_candidates = sorted(candidates_with_scores, key=lambda x: x[1], reverse=True)
        best_score = sorted_candidates[0][1] # They are pairs (candidate,score)
        
        threshold = best_score - (1 - self.alpha) * abs(best_score) if best_score < 0 else self.alpha * best_score

        alpha_candidates = [candidate for candidate, score in sorted_candidates if score >= threshold]

        return alpha_candidates
              
    def GenerateGRASPSolution(self):
        """
        Generates a GRASP solution with a variation of the greedy. It selects the candidate randomly from the RCL.
        """
        candidates = list(range(self.N))
        solution = [-1]*self.sumN
        spaces_in_groups = self.n.copy()
        assigned_count = 0
 
        while assigned_count < self.sumN:
            candidates = self.greedy_solver.PurgeCandidates(candidates, spaces_in_groups, solution)

            if not candidates:
                break
            
            top_candidates = self.SelectTopCandidates(candidates, solution, assigned_count)

            # Randomly choose a candidate from the top candidates
            selected_candidate = random.choice(top_candidates)
            candidates.remove(selected_candidate)

            # Assign candidate to the solution
            group_index = self.d[selected_candidate] - 1
            solution[assigned_count] = selected_candidate
            spaces_in_groups[group_index] -= 1
            assigned_count += 1

        return self.CheckAndReturnSolution(solution, output=False)
        

    def GenerateAndImprove(self):
        """
        Generates a GRASP solution and improves it using local search.
        """
        generated_solution = self.GenerateGRASPSolution()
        if not generated_solution:
            return [],-1

        improved_solution = self.local_search_solver.Solve(generated_solution, output=False)
        current_fitness = self.Fitness(improved_solution)

        return improved_solution,current_fitness
        

    def Solve(self, max_iterations=200, max_time=500) -> List[int]:
        start_time = time.time()
        best_solution, best_fitness = ([], -1)

        for iteration in range(max_iterations):
            if time.time() - start_time >= max_time:
                print(f"Terminating search after {iteration} iterations and {time.time() - start_time:.2f} seconds.")
                break

            new_solution,new_fitness = self.GenerateAndImprove()

            if new_fitness > best_fitness:
                best_solution, best_fitness = new_solution, new_fitness
        
        self.CheckAndReturnSolution(best_solution, output=True)



