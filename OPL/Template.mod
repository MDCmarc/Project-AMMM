// ** PLEASE ONLY CHANGE THIS FILE WHERE INDICATED **
// In particular, do not change the names of the variables.

int                    D = ...;
int              n[1..D] = ...;
int                    N = ...;
int              d[1..N] = ...;
float      m[1..N][1..N] = ...;


// Define here your decision variables and
// any other auxiliary program variables you need.
// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>
dvar boolean selected[1..N];
dvar float+ average;

int total = sum(dep in 1..D) n[dep];
float average_factor = (total - 1) * total / 2; // Gauss sum

//<<<<<<<<<<<<<<<<



// Write here the objective function.

//>>>>>>>>>>>>>>>>
maximize average;
//<<<<<<<<<<<<<<<<

subject to {

    // Write here the constraints.

    //>>>>>>>>>>>>>>>>    
    
	// 1. Each department dep must have exactly n[dep] participants
	forall(dep in 1..D)
		sum(p in 1..N: d[p] == dep) selected[p] == n[dep];
        
	// 2. No incompatible individuals
	forall(i in 1..N, j in i+1..N: m[i][j] == 0)
		selected[i] + selected[j] <= 1;
	
	// 3. Middleman friend
	forall(i in 1..N, j in i+1..N: 0 < m[i][j] < 0.15) {
		sum(k in 1..N: k != i && k != j && m[i][k] > 0.85 && m[k][j] > 0.85) 
			selected[k] >= selected[i] + selected[j] - 1; // if both are selected, from all individuals, at least a friend must be selected
	}
	
	// 4. Average compatibility
	average <= 
		(sum(i in 1..N, j in i+1..N) selected[i] * selected[j] * m[i][j]) 
		/ average_factor;
      
    //<<<<<<<<<<<<<<<<
}

// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>
execute {
	writeln("The commission is formed by: ");
	write("{");
	for (var i = 1; i <= N; ++i) {
		if (selected[i] == 1) {
			write(i + ", ");
		}
	}
	writeln("}");

	var total = 0.0;
	for (var i = 1; i <= N; ++i) {
		if (selected[i] == 1) {
			writeln("Selected person: " + i);
			for (var j = i + 1; j <= N; ++j) {
				if (selected[j] == 1) {
					total += m[i][j];
					writeln("     with: " + j + " is " + m[i][j]);
				}
			}
		}
	}
	writeln("Total compatibility score: " + total);
	writeln("Average compatibility: " + total / average_factor);
}
//<<<<<<<<<<<<<<<<