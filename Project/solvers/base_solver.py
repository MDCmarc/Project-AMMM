from typing import List

class BaseSolver:
    def __init__(self, D, N, n, d, m):
        self.D = D
        self.N = N
        self.n = n
        self.d = d
        self.m = m
        self.sumN = sum(n)
        self.gaussSum = (self.sumN * (self.sumN - 1) / 2)
    
    def fitness(self, sol: List[int]) -> float:
        """ Calculates the fitness of a given solution """
        average = 0
        for i in range(self.sumN):
            for j in range(i + 1, self.sumN):
                average += self.m[sol[i]][sol[j]]

        return average / self.gaussSum

    def candidateNoIncompatible(self, candidate: int,
                                sol: List[int]) -> bool:
        for s in sol:
            if s < 0:
                break
            if self.m[candidate][s] <= 0:
                return False
        return True
    

    def middlemanRestrictionHolds(self, sol: List[int], 
                                    i: int, j: int) -> bool:
        """ Checks if there is any middleman for two indices """
        return any(
            self.m[sol[i]][s] > 0.85 and self.m[s][sol[j]] > 0.85
            for s in sol
        )

    
    def checkAndReturnSolution(self, sol: List[int], cout: bool = True) -> List[int]:
        if sol == [] or sol[-1] == -1:
            if cout:
                print(f"\tAn assignment of {self.sumN} elements could not be constructed.")
            return []

        for i in range(self.sumN):
            for j in range(i + 1, self.sumN):
                if self.m[sol[i]][sol[j]] >= 0.15:
                    continue

                if not self.middlemanRestrictionHolds(sol, i,j):
                    if cout:
                        print("\tAn assigment was found but the middleman restriction was not met")
                    return  []

        sol.sort()
        if cout:
            print(f"\tOBJECTIVE: {self.fitness(sol)}")
            print("\tCommission:", " ".join(str(s + 1) for s in sol))
        
        return sol