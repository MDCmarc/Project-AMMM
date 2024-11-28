import random
import os

######################################################
################# CHOOSE VARIABLES ###################

# How many files to create
numInstances = 4

# Number of departments (same values => just that value)
minNumDepartments = 3
maxNumDepartments = 3

# Total number of members (same values => just that value)
minNumMembers = 10
maxNumMembers = 20

######################################################
######################################################


# Function to generate `d`
def generate_d(D, N):
    # Base count for each value
    base_count = N // D
    remainder = N % D

    # Create the vector
    vector = []
    for i in range(1, D + 1):
        vector.extend([i] * base_count)

    # Distribute the remainder
    for i in range(remainder):
        vector.append(i + 1)

    # Shuffle the vector to randomize
    random.shuffle(vector)
    return vector

# Function to calculate `n` based on `d`
def calculate_n(D, d):
    """Calculate `n` as a list of random numbers from 1 to the count of occurrences of each dimension in `d`."""
    return [random.randint(1, d.count(dim)) if d.count(dim) > 0 else 0 for dim in range(1, D + 1)]

# Function to order `d`
def order_d(D, d):
    """Return `d` ordered with all 1s first, then 2s, and so on."""
    ordered = []
    for dim in range(1, D + 1):
        ordered.extend([dim] * d.count(dim))
    return ordered

# Function to generate `m`
def generate_m(N):
    """Generate `m` as an N x N symmetric triangular matrix with specified conditions."""
    # Initialize an empty matrix
    m = [[0.0 for _ in range(N)] for _ in range(N)]

    # Populate the matrix
    for i in range(N):
        for j in range(i, N):  # Only generate the upper triangle, including diagonal
            if i == j:
                m[i][j] = 1.0  # Diagonal elements set to 1.0
            else:
                # Generate a value that is a multiple of 0.05
                value = round(random.randint(0, 20) * 0.05, 2)
                m[i][j] = value
                m[j][i] = value  # Mirror the value in the lower triangle

    return m

# Function to generate values and create the file
def generate_and_create_file(file_path, D, N):
    # Generate `d` and calculate `n`
    aux_d = generate_d(D, N)
    d = order_d(D, aux_d)
    n = calculate_n(D, d)
    # Generate the matrix `m`
    m = generate_m(N)

    # Create the file
    with open(file_path, 'w') as file:
        file.write(f"D = {D};\n")
        file.write(f"n = [ {' '.join(map(str, n))} ];\n\n")
        file.write(f"N = {N};\n")
        file.write(f"d = [ {' '.join(map(str, d))} ];\n")
        file.write("m = [\n")
        for row in m:
            file.write(f"    [ {' '.join(f'{x:.2f}' for x in row)} ];\n")
        file.write("];\n")
    print(f"File '{file_path}' created successfully.")
    return n, d, m

def count_custom_files(folder_path):
    files = os.listdir(folder_path)
    # Count files that start with "custom"
    custom_count = sum(1 for file in files if file.startswith("custom") and os.path.isfile(os.path.join(folder_path, file)))
    return custom_count

if __name__ == "__main__":
    # Example usage
    script_dir = os.path.dirname(os.path.abspath(__file__))
    #file_path = os.path.join(script_dir, "Datasets/project.1.dat")
    custom_file_count = count_custom_files(os.path.join(script_dir, "Datasets"))
    #print(custom_file_count)

    if numInstances == 1:
        D = minNumDepartments
        N = minNumMembers
    else:
        D_Values = [round(minNumDepartments + i * (maxNumDepartments - minNumDepartments) / (numInstances - 1))
                        for i in range(numInstances)]
        N_Values = [round(minNumMembers + i * (maxNumMembers - minNumMembers) / (numInstances - 1))
                        for i in range(numInstances)]

    print(D_Values)
    print(N_Values)

    for i in range(numInstances):
        D = D_Values[i]  # Number of dimensions
        N = N_Values[i]  # Total number of elements
        output_file = os.path.join(script_dir, "Datasets/custom" + str(custom_file_count) + ".txt")

        n, d, m = generate_and_create_file(output_file, D, N)
        custom_file_count += 1
        # Display generated values
        # print(f"Generated n (counts of each dimension): {n}")
        # print(f"Generated d (dimension assignments): {d}")
        # print("Generated m (matrix):")
        # for row in m:
        #     print(row)