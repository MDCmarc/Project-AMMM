# AMMM Project

## How to Use the Solvers
To execute any of the solvers, import the corresponding model:
```python
from solvers import Greedy, LocalSearch, GRASP
```

Instantiate the solver as follows:
```python
greedy_solver = Greedy(D, N, n, d, m)
local_search_solver = LocalSearch(D, N, n, d, m)
grasp_solver = GRASP(D, N, n, d, m, alpha=0.3)  # If `alpha` is not specified, the default value is 0.3
```

Run the solvers by calling their Solve methods:
```python
greedy_solver.Solve()
local_search_solver.Solve(greedy_solution,  max_iterations=100, max_time=120)
GRASP_solver.Solve(max_iterations=200, max_time=500)
```
### Notes:
- ```max_iterations``` and ```max_time``` are optional parameters. If not specified, default values will be used.
- The *LocalSearch solver* requires an initial solution to improve upon.

Each ```Solve``` method returns a ```tuple[float, List[int]]```, where:
- The first value is the fitness of the solution.
- The second value is the constructed solution.

## Example Execution
The ```main.py``` file demonstrates how to run the three solvers for all datasets in the ```Datasets/``` directory ( ```*.dat``` files)
```python
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "Custom/Path/Goes/Here")
file_paths = glob.glob(os.path.join(data_dir, "*.dat"))
```

The main function uses the ```parse_validate.py``` script to parse and validate the data extracted from the  ```*.dat``` files.

## Instance Generator
To generate new instances, edit the following lines in the instance generator script to specify the number of faculty members and departments:

```python
#
N = 65  # Number of faculty members
D = 2   # Number of departments
#
```
The program will randomly generate the rest of the data.

## Alpha Tunning
To run the experiments for tuning the alpha value, the Python notebook ```alpha_tunning.ipynb``` has been used.

## Report
All the plots have been created with TikZ + PGFPlots, and the source code can be found in the folder ```latex```.

---
---
**Developed by Pau Adell and Marc Díaz**

