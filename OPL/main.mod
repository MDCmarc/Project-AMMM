main {
	var start = new Date();
    var startTime = start.getTime();
	
	var src = new IloOplModelSource("Template(linear).mod");
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	var model = new IloOplModel(def, cplex);
	var data = new IloOplDataSource("Datasets/custom7.dat");
	
	model.addDataSource(data);
	model.generate();
	
	cplex.tilim = 30*60; // s
	cplex.epgap = 0.01;
	
	if (cplex.solve()) {
	    writeln("OBJECTIVE: " +cplex.getObjValue() )
		writeln("The selected members are : ");
		write("{");
		for (var i = 1; i <= model.N; ++i) {
		    if (model.selected[i] == 1) {
			    if (i == 1) {
			  	  write(i);
			    } else {
			    	write(", " + i);
			    }
		    }
		}
		writeln("}");
	}	
	else {
		writeln("No solution found");
	}
	
	model.end();
	data.end();
	def.end();
	cplex.end();
	src.end();
	
	// Write execution time
    var end = new Date();
    var endTime = end.getTime();
    writeln("\nExecution time: " + (endTime - startTime)/1000 + "s");
};