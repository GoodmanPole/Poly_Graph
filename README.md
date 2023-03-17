# Poly_Graph
Implementing Poly Graph for Checking VSR (View-Serializability)
In the implementation of this method, it is done as follows:
First, by receiving the Schedule in String format in the following format:
"r2(A)r1(A)w1(C)r3(C)w1(B)r4(B)w3(A)r4(C)w2(D)r2(B)w4(A)w4(B)"
We specify all reads and writes and store it in two 3-dimensional arrays named read and write.
In the first line of arrays, the operator index is stored in String.
Transaction number is stored in the second line of arrays.
In the third line of the arrays, the name of the data is also stored (A, B,...)
With the help of the above arrays, we find the relationships between Reads and Writes and store it in a matrix called PolyGraph. Also, with the help of the built Graph class, we convert it to a graph.
After that, we apply rule number 3 in the PolyGraph drawing to complete the graph.
In the meantime, by adding each edge with the help of the Graph Coloring algorithm, we check it for the presence of a round, and if there is a round, we come to the conclusion that the Schedule cannot be a VSR.
Finally, if there is no distance in the graph, we write its topological order using the TopologicalSort method.
Finally, we draw and display the graph.
#) During the execution of the program, the program ends by closing the window related to the drawn PolyGraph.
