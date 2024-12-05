import time

from .base_solver import BaseSolver
from typing import List


class LocalSearch(BaseSolver):

    def GenerateNeighbors(self, sol: List[int]) -> List[List[int]]:
        """
        Generates all valid neighboring solutions by replacing each individual in the current solution
        with a candidate from the same department if it is valid.
        """
        neighbors = []
        sol_set = set(sol)  # For better efficiency when checking if candidate is inside solution

        for i, current_candidate in enumerate(sol):
            department_i = self.d[current_candidate]

            possibles = [j for j in range(len(self.d)) if self.d[j] == department_i and j not in sol_set]

            for candidate in possibles:
                neighbor = sol.copy()
                neighbor[i] = candidate

                if self.SolutionIsValid(neighbor):
                    neighbors.append(neighbor)
        return neighbors

    def Solve(self, initial_solution: List[int], max_iterations=100, max_time=120,
              output: bool = True) -> tuple[float, List[int]]:
        """
        Solves the optimization problem using a local search algorithm.
        The default parameters are 100 iterations and 120 seconds.
        """
        start_time = time.time()
        current_solution = initial_solution
        current_fitness = self.Fitness(current_solution)

        for iteration in range(max_iterations):
            if time.time() - start_time >= max_time:
                if output:
                    print(f"Ending search after {iteration} iterations and {time.time() - start_time:.2f} seconds.")
                break

            neighbors = self.GenerateNeighbors(current_solution)
            if not neighbors:
                break

            # Choose the best neighbour
            best_neighbor = max(neighbors, key=self.Fitness, default=None)
            best_fitness = self.Fitness(best_neighbor)

            if best_fitness > current_fitness:
                current_solution, current_fitness = best_neighbor, best_fitness
            else:
                break  # No improvement, exit early

        return self.CheckAndReturnSolution(current_solution, output=output)
