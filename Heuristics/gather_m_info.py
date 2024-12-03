## This is a script to gather information about the M matrix in order to see if the ones that we generate have too poor compatibility.
from Parse_Validate import parse_and_validate_input_file
import os
import glob

def sum_Matrix(m):
    sum = 0
    for i in range(len(m)):
        for j in range(len(m[i])):
            sum += m[i][j]
    return sum

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "Datasets")
    file_paths = glob.glob(os.path.join(data_dir, "*.dat"))
    
    #custom_path = [os.path.join(data_dir, "project.2.dat")]

    for path in file_paths:
        D = None
        n = []
        N = None
        d = []
        m = []
        D, n, N, d, m = parse_and_validate_input_file(path)

        print(f"File {path}\n################")
        print(f"Sum of M: {sum_Matrix(m)}")
        print(f"Average of M: {sum_Matrix(m)/len(m)}")