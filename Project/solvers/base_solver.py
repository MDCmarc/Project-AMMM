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


    def Fitness(self, sol: List[int]) -> float:
        """
        Calculates the fitness of a given solution `sol`.
        The fitness is the average compatibility score between all pairs of elements in the solution.
        """
        total_compatibility  = 0
        for i in range(self.sumN):
            for j in range(i + 1, self.sumN):
                total_compatibility  += self.m[sol[i]][sol[j]]

        return total_compatibility  / self.gaussSum


    def CandidateIncompatible(self, candidate: int, sol: List[int]) -> bool:
        """
        Determines if the given `candidate` is incompatible with any valid element in the solution `sol`.
        """
        return any(self.m[candidate][element] <= 0 for element in sol if element >= 0)
    

    def MiddlemanRestrictionHolds(self, sol: List[int], i: int, j: int) -> bool:
        """
        Checks if there is any middleman for indices `i` and `j` in the solution `sol`.
        """
        return any(self.m[sol[i]][s] > 0.85 and self.m[s][sol[j]] > 0.85 for s in sol if s != -1)

    
    def SolutionIsValid(self, sol: List[int], output: bool = False):
        """
        Validates the solution `sol` by checking pairwise compatibility and the middleman restriction.
        """   
        if not sol or sol[-1] == -1:
            if output:
                print(f"\tAn assignment of {self.sumN} elements could not be constructed.")
            return False
        
        for i in range(self.sumN):
            for j in range(i + 1, self.sumN):
                if self.m[sol[i]][sol[j]] <= 0:
                    if output:
                        print(f"\tIncompatibility found!!!")
                    return False
                
                if self.m[sol[i]][sol[j]] < 0.15:
                    if not self.MiddlemanRestrictionHolds(sol, i, j, ):
                        if output:
                            print("\tAn assigment was found but the middleman restriction was not met")
                        return False
        return True


    def CheckAndReturnSolution(self, sol: List[int], output: bool = False) -> List[int]:
        """
        Validates the solution `sol` and, if valid, prints the objective and returns the solution.
        Otherwise, it returns an empty list.
        """    
        if not self.SolutionIsValid(sol, output):
            return []
        
        sol.sort()
        if output:
            print(f"\tOBJECTIVE: {self.Fitness(sol)}")
            print("\tCommission:", " ".join(str(s + 1) for s in sol)) 
        return sol