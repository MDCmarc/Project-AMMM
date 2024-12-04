import time

from .base_solver import BaseSolver
from typing import List

class LocalSearch(BaseSolver):

    def possible(self, sol: List[int]) -> bool:
        for i in range(self.sumN):
            for j in range(i + 1, self.sumN):
                if self.m[sol[i]][sol[j]] <= 0:
                    return False
                
                if self.m[sol[i]][sol[j]] < 0.15:
                    if not self.middlemanRestrictionHolds(sol, i, j, ):
                        return False
        return True


    def generate_neighbors(self, sol: List[int]) -> List[List[int]]:
        neighbors = []
        for i in range(len(sol)):
            department_i = self.d[sol[i]] 

            possibles = [j for j in range(len(self.d)) if self.d[j] == department_i]

            for candidate in possibles:
                if candidate in sol:
                    continue
                neighbor = sol.copy()
                neighbor[i] = candidate
                if self.possible(neighbor):
                    neighbors.append(neighbor)
        return neighbors

    def solve(self, intitial_solution: List[int],
              max_iterations=100, max_time=120,
              cout: bool = True) -> None:
        start_time = time.time()
        current_solution = intitial_solution
        current_fitness = self.fitness(current_solution)
        
        for _ in range(max_iterations):
            elapsed_time = time.time() - start_time
            if elapsed_time >= max_time:
                print(f"Terminating search after {elapsed_time:.2f} seconds.")
                break
        
            neighbors = self.generate_neighbors(current_solution)
            best_neighbor = None
            best_fitness = current_fitness
            
            for neighbor in neighbors:
                fitness = self.fitness(neighbor)
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_neighbor = neighbor

            if best_neighbor is not None:
                current_solution = best_neighbor
                current_fitness = best_fitness
            else:
                break  # No improvement, exit early
        
        return self.checkAndReturnSolution(current_solution, cout)
