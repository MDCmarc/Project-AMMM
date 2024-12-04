from Parse_Validate import parse_and_validate_input_file
from solvers import Greedy, LocalSearch, GRASP
import os
import glob 

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "Datasets")
    file_paths = glob.glob(os.path.join(data_dir, "*.dat"))
    
    # custom_path = [os.path.join(data_dir, "custom0.dat")]

    for path in file_paths:
        D = None
        n = []
        N = None
        d = []
        m = []
        D, n, N, d, m = parse_and_validate_input_file(path)

        greedy_solver = Greedy(D, N, n, d, m)
        local_search_solver = LocalSearch(D, N, n, d, m)
        GRASP_solver = GRASP(D, N, n, d, m)

        greedy_solution = []
        local_search_sol = []
        grasp_sol = []

        print(f"File {path}\n################")
        
        print("Greedy:")
        greedy_solution = greedy_solver.Solve()

        print("LocalSearch:")
        if greedy_solution:
            local_search_sol = local_search_solver.Solve(greedy_solution)
        else: 
            print("\tCan not do Local Search from an empty solution:")


        print("GRASP:")
        GRASP_solver.Solve()
    
        print("\n")