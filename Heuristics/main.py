
from Parse_Validate import parse_and_validate_input_file
from GreedySolver import GreedySolver
import os
import glob 

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "Datasets")
    file_paths = glob.glob(os.path.join(data_dir, "custom*.dat"))
    
    for path in file_paths:
        D = None
        n = []
        N = None
        d = []
        m = []
        D, n, N, d, m = parse_and_validate_input_file(path)

        print(f"File {path}\n################")
        solver = GreedySolver(D, N, n, d, m)
        solver.solve()
        solver.print_solution()
        print("\n")