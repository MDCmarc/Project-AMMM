from solvers import Greedy, LocalSearch, GRASP

import random
import os


# 

N = 300
D = 20

#



n = [-1]*D
d = [-1]*N
m = [[-1]*N]*N

def solutionPossible(sol,m):
    def middleman_restriction_holds(i,  j, sol):
        return any(
            m[i][k] > 0.85 and m[k][j] > 0.85
            for k in sol
        )
    for i in range(sum(n)):
        for j in range(i + 1, sum(n)):
            if m[sol[i]][sol[j]] <= 0:
                return False
            
            if m[sol[i]][sol[j]] < 0.15:
                if not middleman_restriction_holds(sol[i], sol[j], sol):
                    return False
    return True

# No repetetition (range_j not included)
def get_random_distribution(size, range_i, range_j):
    indices = set()
    while(len(indices) < size):
        indices.add(random.randrange(range_i,range_j))
     
    return sorted(indices)

def generate_m(solution):
    m = [[0.0 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(i, N):  # Only generate the upper triangle, including diagonal
            value = -1
            if i == j:
                value = 1.0  # Diagonal elements set to 1.0

            elif (i in solution) and (j in solution):
                value =  round(random.randint(3, 20) * 0.05, 2) # [0.15 - 1]
            else:
                value = round(random.randint(0, 16) * 0.05, 2) # [0. - 0.8]

            m[i][j] = value
            m[j][i] = value

    return m


def generate_and_create_file(m, solution):
    def count_custom_files(folder_path):
        files = os.listdir(folder_path)
        custom_count = sum(1 for file in files if file.startswith("custom") and os.path.isfile(os.path.join(folder_path, file)))
        return custom_count
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    custom_file_count = count_custom_files(os.path.join(script_dir, "Datasets"))

    output_file = os.path.join(script_dir, "Datasets/custom" + str(custom_file_count) + ".dat")
    
    with open(output_file, 'w') as file:
        file.write(f"D = {D};\n")
        file.write(f"n = [ {' '.join(map(str, n))} ];\n\n")
        file.write(f"N = {N};\n")
        file.write(f"d = [ {' '.join(map(str, d))} ];\n")
        file.write("m = [\n")
        for row in m:
            file.write(f"    [ {' '.join(f'{x:.2f}' for x in row)} ]\n")
        file.write("];\n")
        
        file.write(f"solution = [ {' '.join(map(str, solution))} ];\n\n")

    print(f"File '{output_file}' created successfully.")



if __name__ == "__main__":
    # 2 5 6 7 10 12 15 19 24 26 31 35 36
    indices = get_random_distribution(D-1, 1, N)
    solution=[]
    for i in range(len(indices)+1):
        lower_range = indices[i-1] if (i>0) else 0 
        upper_range = indices[i] if (i < len(indices)) else N
        range_size = max(2, round(2*(upper_range - lower_range +1)/3) )
        for j in range(lower_range,upper_range):
            d[j] = i+1

        n[i]=random.randrange(1,range_size)

        solution_individuals = get_random_distribution(n[i], lower_range, upper_range)

        solution.extend(solution_individuals)
    
    m = generate_m(solution)

    while(not solutionPossible(solution,m)):
        print("Again")
        m = generate_m(solution)

    print(d)
    print(n)
    print(solution)
    print(m)

    generate_and_create_file(m,solution)





