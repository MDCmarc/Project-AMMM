
from Parse_Validate import parse_and_validate_input_file
from GreedySolver import GreedySolver
import os


if __name__ == "__main__":
    # Ensure file path is relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    #file_path = os.path.join(script_dir, "Datasets/project.1.dat")
    file_paths = [os.path.join(script_dir, "Datasets/project." + str(i) + ".dat") for i in range(1, 9) ]
    #print(file_paths)
    
    for path in file_paths:
        D = None
        n = []
        N = None
        d = []
        m = []
        D, n, N, d, m = parse_and_validate_input_file(path)

        solver = GreedySolver(D, N, n, d, m)
        solver.solve()
        solver.print_solution()