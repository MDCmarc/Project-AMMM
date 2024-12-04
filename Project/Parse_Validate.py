# Function to parse and validate the input file with semicolons
def parse_and_validate_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize variables
    D = None
    n = []
    N = None
    d = []
    m = []

    # Helper function to raise an error
    def raise_error(message):
        raise ValueError(f"Error in file: {message}")

    # Parse each line
    for i, line in enumerate(lines):
        line = line.strip().rstrip(";")  # Remove trailing whitespace and semicolon

        if line.startswith("D ="):
            try:
                D = int(line.split("=")[1].strip())
                if D <= 0:
                    raise_error(f"'D' must be a positive integer (line {i+1}).")
            except ValueError:
                raise_error(f"Invalid value for 'D' (line {i+1}).")

        elif line.startswith("n ="):
            try:
                n = list(map(int, line.split("=")[1].strip().strip("[]").split()))
                if len(n) != D:
                    raise_error(f"Length of 'n' must equal 'D' (line {i+1}).")
                if any(x <= 0 for x in n):
                    raise_error(f"All values in 'n' must be positive integers (line {i+1}).")
            except ValueError:
                raise_error(f"Invalid format for 'n' (line {i+1}).")

        elif line.startswith("N ="):
            try:
                N = int(line.split("=")[1].strip())
                if N <= 0:
                    raise_error(f"'N' must be a positive integer (line {i+1}).")
            except ValueError:
                raise_error(f"Invalid value for 'N' (line {i+1}).")

        elif line.startswith("d ="):
            try:
                d = list(map(int, line.split("=")[1].strip().strip("[]").split()))
                if len(d) != N:
                    raise_error(f"Length of 'd' must equal 'N' (line {i+1}).")
                if any(x <= 0 or x > D for x in d):
                    raise_error(f"All values in 'd' must be between 1 and 'D' (line {i+1}).")
            except ValueError:
                raise_error(f"Invalid format for 'd' (line {i+1}).")

        elif line.startswith("m = ["):
            # Begin reading the matrix
            matrix_start = i + 1
            for j, matrix_line in enumerate(lines[matrix_start:], start=matrix_start):
                matrix_line = matrix_line.strip().rstrip(";")
                if matrix_line == "]":
                    break
                try:
                    row = list(map(float, matrix_line.strip().strip("[]").split()))
                    if len(row) != N:
                        raise_error(f"Matrix row {j-matrix_start+1} must have 'N' columns (line {j+1}).")
                    m.append(row)
                except ValueError:
                    raise_error(f"Invalid format in matrix row {j-matrix_start+1} (line {j+1}).")

    # Final validations
    if len(m) != N:
        raise_error("The matrix 'm' must have 'N' rows.")

    return D, n, N, d, m
