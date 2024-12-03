import math
import random
from typing import List


class LocalSearch:
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

    def possible(self, sol: List[int]) -> bool:
        def middleman_restriction_holds(i: int, j: int, sol: List[int]) -> bool:
            return any(
                self.m[i][k] > 0.85 and self.m[k][j] > 0.85
                for k in sol
            )
        for i in range(self.sumN):
            for j in range(i + 1, self.sumN):
                if self.m[sol[i]][sol[j]] <= 0:
                    return False
                
                if self.m[sol[i]][sol[j]] < 0.15:
                    if not middleman_restriction_holds(sol[i], sol[j], sol):
                        return False
        return True

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
                    if not middleman_restriction_holds(self.solution[i], self.solution[j]):
                        print("An assigment was found but the middleman restriction was not met")
                        return

        self.solution.sort()
        print(f"OBJECTIVE: {self.fitness(self.solution)}")
        print("Commission:", " ".join(str(s + 1) for s in self.solution))

    def local_search(self, intitial_solution: List[int] ,max_iterations=100) -> None:
        self.solution = intitial_solution
        current_solution = intitial_solution
        current_fitness = self.fitness(current_solution)
        
        for _ in range(max_iterations):
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

        self.solution = current_solution  # Update solution with best found

    def generate_neighbors(self, sol: List[int]) -> List[List[int]]:
        neighbors = []

        for i in range(len(sol)): # 3 8 14 16 17
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
