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

dvar boolean x[1..N];
dvar boolean y[1..N][1..N];
dvar float+ z;

int T = sum(dep in 1..D) n[dep];
float G = (T - 1) * T / 2; // Gauss sum

//<<<<<<<<<<<<<<<<



// Write here the objective function.

//>>>>>>>>>>>>>>>>

maximize z;

//<<<<<<<<<<<<<<<<

subject to {

    // Write here the constraints.

    //>>>>>>>>>>>>>>>>    
    
	// 1. Each department dep must have exactly n[dep] participants
	forall(dep in 1..D)
		sum(p in 1..N: d[p] == dep) x[p] == n[dep];
        
	// 2. No incompatible individuals
	forall(i in 1..N, j in i+1..N: m[i][j] == 0)
		x[i] + x[j] <= 1;
	
	// 3. Middleman friend
	forall(i in 1..N, j in i+1..N: 0 < m[i][j] < 0.15) {
		sum(k in 1..N: k != i && k != j && m[i][k] > 0.85 && m[k][j] > 0.85) 
			x[k] >= x[i] + x[j] - 1;
	}
	
	// 5. Linear:
	forall(i in 1..N, j in i+1..N) {
	    y[i][j] <= x[i];
	    y[i][j] <= x[j];
	    y[i][j] >= x[i] + x[j] - 1; 
  	}
	
	// 4. Average compatibility
	z <= 
		(sum(i in 1..N, j in i+1..N) y[i][j] * m[i][j]) 
		/ G;
      
    //<<<<<<<<<<<<<<<<
}

// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>
execute {
	writeln("The commission is formed by: ");
	write("{");
	for (var i = 1; i <= N; ++i) {
		if (x[i] == 1) {
			write(i + ", ");
		}
	}
	writeln("}");

	var total = 0.0;
	for (var i = 1; i <= N; ++i) {
		if (x[i] == 1) {
			writeln("Selected person: " + i);
			for (var j = i + 1; j <= N; ++j) {
				if (x[j] == 1) {
					total += m[i][j];
					writeln("     with: " + j + " is " + m[i][j]);
				}
			}
		}
	}
	writeln("Total compatibility score: " + total);
	writeln("Average compatibility: " + total / G);
}
//<<<<<<<<<<<<<<<<