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

    
    def SelectTopCandidates(self, candidates: List[int],
                         solution: List[int],
                         assigned_count: int) -> List[int]:
        candidates_with_scores = [
            (candidate, self.greedy_solver.greedyCostFunction(candidate, candidates, 
                                                 solution, assigned_count)) 
            for candidate in candidates
        ]
        
        sorted_candidates = sorted(candidates_with_scores, key=lambda x: x[1], reverse=True)
        
        best_score = sorted_candidates[0][1] # They are pairs (candidate,score)
        if best_score < 0:
            threshold = best_score - (1-self.alpha) * abs(best_score )
        else:
            threshold = self.alpha * best_score

        # Select candidates whose scores are above or equal to the threshold.
        alpha_candidates = [
            candidate for candidate, score 
            in sorted_candidates 
            if score >= threshold
        ]

        # Fallback if no candidates are selected
        if not alpha_candidates:
            print("Warning: No candidates selected. Returning best candidate.")
            alpha_candidates = [sorted_candidates[0][0]]  # Return the best candidate

        return alpha_candidates
              
    def generateGRASPSolution(self):
        candidates = list(range(self.N))
        solution = [-1]*self.sumN
        spaces_in_groups = self.n.copy()
        assigned_count = 0
 
        while assigned_count < self.sumN:
            candidates = self.greedy_solver.purgeCandidates(candidates, spaces_in_groups, solution)

            if not candidates:
                break
            
            top_candidates = self.SelectTopCandidates(candidates, solution, assigned_count)

            selected_candidate = random.choice(top_candidates)
            candidates.remove(selected_candidate)
            group_index = self.d[selected_candidate] - 1

            solution[assigned_count] = selected_candidate
            spaces_in_groups[group_index] -= 1
            assigned_count += 1

        return self.checkAndReturnSolution(solution, False)
        

    def generateAndImprove(self ):
        generated_solution = self.generateGRASPSolution()
        if not generated_solution:
            return [],-1

        improved_solution = self.local_search_solver.solve(generated_solution, cout=False)
        current_fitness = self.fitness(improved_solution)

        return improved_solution,current_fitness
        

    def solve(self, max_iterations=200, max_time=500) -> List[int]:
        start_time = time.time()
        best_solution, best_fitness = self.generateAndImprove()

        for i in range(max_iterations):
            elapsed_time = time.time() - start_time
            if elapsed_time >= max_time:
                print(f"Terminating search after {elapsed_time:.2f} seconds.")
                break

            new_solution,new_fitness = self.generateAndImprove()

            if new_fitness > best_fitness:
                best_solution = new_solution
                best_fitness = new_fitness
        
        self.checkAndReturnSolution(best_solution)



