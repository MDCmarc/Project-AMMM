from parse_validate import parse_and_validate_input_file
from solvers import Greedy, LocalSearch, GRASP
import os
import glob
import time

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

        print(f"File {path}\n################")

        # ------------------ Greedy Solver ------------------
        print("Greedy:")
        start_time = time.time()
        _, greedy_solution = greedy_solver.Solve()
        end_time = time.time()

        print(f"\tTime: {end_time - start_time:.5f} seconds")
        # ------------------ ###### ###### ------------------

        # ------------------ Local Search ------------------
        print("LocalSearch:")
        start_time = time.time()
        if greedy_solution:
            _, local_search_sol = local_search_solver.Solve(greedy_solution)
        else:
            print("\tCan not do Local Search from an empty solution:")
        end_time = time.time()

        print(f"\tTime: {end_time - start_time:.5f} seconds")
        # ------------------ ##### ###### ------------------

        # ---------------------- GRASP ----------------------
        print("GRASP:")
        start_time = time.time()
        _, grasp_sol = GRASP_solver.Solve()
        end_time = time.time()

        print(f"\tTime: {end_time - start_time:.5f} seconds")
        # ---------------------- ##### ----------------------

        print("\n")
