from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

#GoodmanPole

# This class constructing a graph so we can detect cycle and sort it topologicaly
class Graph():
    def __init__(self, V):
        self.V = V
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def DFSUtil(self, u, color):
        # GRAY : This vertex is being processed (DFS
        #		 for this vertex has started, but not
        #		 ended (or this vertex is in function
        #		 call stack)
        color[u] = "GRAY"

        for v in self.graph[u]:

            if color[v] == "GRAY":
                return True

            if color[v] == "WHITE" and self.DFSUtil(v, color) == True:
                return True

        color[u] = "BLACK"
        return False

    def isCyclic(self):
        color = ["WHITE"] * self.V

        for i in range(self.V):
            if color[i] == "WHITE":
                if self.DFSUtil(i, color) == True:
                    return True
        return False

        # A recursive function used by topologicalSort

    def topologicalSortUtil(self, v, visited, stack):

        # Mark the current node as visited.
        visited[v] = True

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)

        # Push current vertex to stack which stores result
        stack.append(v)

    # The function to do Topological Sort. It uses recursive
    # topologicalSortUtil()
    def topologicalSort(self):
        # Mark all the vertices as not visited
        visited = [False] * self.V
        stack = []

        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for i in range(self.V):
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)

        # Print contents of the stack
        print(stack[::-1])  # return list in reverse order





# This Method is for constructing the PolyGraph

def polygraph(read, write):
    transCount = []
    for i in range(len(read[1])):
        if read[1][i] not in transCount:
            transCount.append(read[1][i])

    for i in range(len(write[1])):
        if write[1][i] not in transCount:
            transCount.append(write[1][i])
    # print(transCount)

    polyGraphBeta = [[0 for i in range(len(transCount) + 1)] for j in range((len(transCount) + 1) * 2)]
    polyGraph = [[0 for i in range(len(transCount) + 1)] for j in range((len(transCount) + 1))]
    g = Graph(len(transCount) + 2)

    # print(polyGraph)
    # print(polyGraphBeta)
    # with open('polyGraph.txt','a') as f:

    for i in range(0,len(read[0])):
        for j in range(0,len(write[0])):
            # print("This is i:",i)
            # print("This is j:",j)
            if read[0][i] == 0:
                # print("?")
                g.addEdge(0, read[1][i])
                polyGraph[0][read[1][i] - 1] = 1
                polyGraphBeta[0][read[1][i] - 1] = 1
                if polyGraphBeta[1][read[1][i] - 1]==0:
                    polyGraphBeta[1][read[1][i] - 1] = read[2][i]
                else:
                    polyGraphBeta[1][read[1][i] - 1] += read[2][i]
                # print("This is polygraph:",polyGraphBeta)
                break
            else:
                if write[0][j] < read[0][i] and read[2][i] == write[2][j]:
                    m=j+1
                    n=j
                    while m<len(write[0]):
                        if write[0][m] < read[0][i] and read[2][i] == write[2][m]:
                            n=m
                        m+=1
                    # print("??")
                    g.addEdge(write[1][n], read[1][i])
                    polyGraph[write[1][n]][read[1][i] - 1] = 1
                    polyGraphBeta[write[1][n] * 2][read[1][i] - 1] = 1
                    if polyGraphBeta[(write[1][n] * 2) + 1][read[1][i] - 1] ==0:
                        polyGraphBeta[(write[1][n] * 2) + 1][read[1][i] - 1] = read[2][i]
                    else:
                        polyGraphBeta[(write[1][n] * 2) + 1][read[1][i] - 1] += read[2][i]
                    # print("This is graph 23:",polyGraphBeta)
                    break

                elif write[0][j] < read[0][i] and read[2][i] != write[2][j]:
                    continue
                else:
                    # print("???")
                    g.addEdge(0, read[1][i])
                    polyGraph[0][read[1][i] - 1] = 1
                    polyGraphBeta[0][read[1][i] - 1] = 1
                    # print(read[1][i] - 1)
                    if polyGraphBeta[1][read[1][i] - 1] ==0:
                        polyGraphBeta[1][read[1][i] - 1] = read[2][i]
                    else:
                        polyGraphBeta[1][read[1][i] - 1] += read[2][i]
                    # print("This is Graph:",polyGraphBeta)
                    break

    # print("This is polyGraph b:",polyGraphBeta)

    # we must add the final writes to the polyGraph
    checked = []
    z = len(write[0]) - 1
    while z >= 0:
        if write[2][z] not in checked:
            checked.append(write[2][z])
            g.addEdge(write[1][z], len(transCount) + 1)
            polyGraph[write[1][z]][len(polyGraph[0]) - 1] = 1
            polyGraphBeta[write[1][z] * 2][len(polyGraph[0]) - 1] = 1
            if polyGraphBeta[(write[1][z] * 2) + 1][len(polyGraph[0]) - 1] ==0:
                polyGraphBeta[(write[1][z] * 2) + 1][len(polyGraph[0]) - 1] = write[2][z]
            else:
                polyGraphBeta[(write[1][z] * 2) + 1][len(polyGraph[0]) - 1] += write[2][z]

        z -= 1
    # Making a copy of the Graph
    gBeta = g
    # print(g.graph)
    # print(gBeta.graph)

    # we must apply the rule 3 of the polyGraph to make it complete
    print("PolyGraph Matrix before applying rule 3:\n",polyGraph)
    print("----------------------------------------------------------------")
    print("PolyGraph Matrix with its elements before applying rule 3:\n",polyGraphBeta)
    print()
    print("----------------------------------------------------------------")

    checkList = []
    i = 1
    while i < len(polyGraphBeta):
        # print("11")
        for j in range(len(polyGraphBeta[0])):
            if polyGraphBeta[i][j]==0:
                continue
            else:
                for k in range(len(polyGraphBeta[i][j])):
                    # print("12")
                    if polyGraphBeta[i][j][k] not in checkList:
                        checkList.append(polyGraphBeta[i][j][k])
                        # print(checkList)

                        # This Loop is for finding all of the Writes which is related to that specific data
                        writes = []
                        for x in range(len(write[0])):
                            # print("13")
                            if write[2][x] == polyGraphBeta[i][j][k]:
                                writes.append(write[1][x])

                        # print("Writes", writes)
                        # This Loop is for finding the relations which is related to that specific data
                        relations = []
                        z = 1
                        while z < len(polyGraphBeta):
                            # print("14")
                            for y in range(len(polyGraphBeta[0])):
                                if polyGraphBeta[z][y]==0:
                                    continue
                                else:
                                    for h in range(len(polyGraphBeta[z][y])):
                                        # print("15")
                                        if polyGraphBeta[z][y][h] == polyGraphBeta[i][j][k]:
                                            relations.append((int((z - 1) / 2), y + 1))
                            z += 2

                        # print("Relation:", relations)
                        # In this loop we check if there is a new relation to adding it to the graph or not
                        for m in range(len(writes)):
                            # print("16")
                            flag = 0
                            for n in range(len(relations)):
                                # print("17")
                                if writes[m] != relations[n][0] and writes[m] != relations[n][1]:
                                    if relations[n][0] == 0:
                                        gBeta.addEdge(relations[n][1],writes[m])
                                        if gBeta.isCyclic() == True:
                                            # flag += 1
                                            gBeta = g
                                            continue
                                        else:
                                            g = gBeta
                                            polyGraph[relations[n][1]][writes[m] - 1]=1


                                    elif relations[n][1] == len(transCount) + 1:
                                        gBeta.addEdge(writes[m], relations[n][0])
                                        if gBeta.isCyclic() == True:
                                            # flag += 1
                                            gBeta = g
                                            continue
                                        else:
                                            g = gBeta
                                            polyGraph[writes[m]][relations[n][0] - 1]=1

                                    else:
                                        gBeta.addEdge(writes[m], relations[n][0])
                                        if gBeta.isCyclic() == True:
                                            # flag += 1
                                            gBeta = g
                                            continue
                                        else:
                                            g = gBeta
                                            polyGraph[writes[m]][relations[n][0] - 1]=1

                                        gBeta.addEdge(relations[n][1], writes[m])
                                        if gBeta.isCyclic() == True:
                                            # flag += 1
                                            gBeta = g
                                            continue
                                        else:
                                            g = gBeta
                                            polyGraph[relations[n][1]][writes[m] - 1]=1
                                    if g.isCyclic()==True:
                                        print("The PolyGraph is Cyclic so The Schedule is not VSR")
                                        print("GoodmanPole")
                                        return


        i += 2

    print("The PolyGraph which is saved in a matrix:\n",polyGraph)
    print("----------------------------------------------------------------")
    print("The PolyGraph which is saved in a matrix with its data element:\n",polyGraphBeta)
    print()
    print("----------------------------------------------------------------")



    # Ploting the graph


     # saving the graph in a file
    with open('polyGraph.txt', 'w') as f:
        f.writelines('\n')

    i=0
    while i<len(polyGraph):
        for j in range(len(polyGraph[0])):
            if polyGraph[i][j]==1:
                str1 = str(i)
                str1+=" "
                str1 += str(j+1)
                # str1 += " 1"
                with open('polyGraph.txt', 'a') as f:
                    f.writelines(str1)
                    f.writelines('\n')
        i+=1

    #Ploting the PolyGraph

    G3=nx.read_edgelist('D:\pycharm\PolyGraph/polyGraph.txt',create_using=nx.DiGraph,nodetype=int)
    print("PolyGraph Info:",nx.info(G3))
    print()
    print("----------------------------------------------------------------")
    nx.draw(G3,with_labels=True)
    plt.show()



    # Now we are going to find the Transaction order with the help of the Topological Sort
    print("This is the PolyGraph:",g.graph)
    print("----------------------------------------------------------------")
    print("The Given Schedule is VSR and here is the Topological order for the Schedule:")
    g.topologicalSort()
    print("----------------------------------------------------------------")
    print("GoodmanPole")
    return


#Method for indexing read operations
def readIndexer(schedule):
    rCounter = 0

    # finding the number of the Reads and Writes in the given Schedule
    for i in range(0, len(schedule)):
        if schedule[i] == 'r' or schedule[i] == 'R':
            rCounter += 1

    r = [[0 for i in range(rCounter)] for j in range(3)]

    # finding all of the indexes of the Read operation
    j = 0
    for i in range(0, len(schedule)):
        if schedule[i] == 'r' or schedule[i] == 'R':
            r[0][j] = i
            if schedule[i + 2] == '(':
                r[1][j] = int(schedule[i + 1])
                r[2][j] = schedule[i + 3]
                j += 1
            else:
                str = ""
                for x in range(i + 1, len(schedule)):
                    if schedule[x] != '(':
                        str += schedule[x]
                    else:
                        r[2][j] = schedule[x + 1]
                        break
                r[1][j] = int(str)
                j += 1

    return r


#Method for indexing write operations
def writeIndexer(schedule):
    wCounter = 0

    # finding the number of the Reads and Writes in the given Schedule
    for i in range(0, len(schedule)):
        if schedule[i] == 'w' or schedule[i] == 'W':
            wCounter += 1

    w = [[0 for i in range(wCounter)] for j in range(3)]

    # finding all of the indexes of the Writes operation
    j = 0
    for i in range(0, len(schedule)):
        if schedule[i] == 'w' or schedule[i] == 'W':
            w[0][j] = i
            if schedule[i + 2] == '(':
                w[1][j] = int(schedule[i + 1])
                w[2][j] = schedule[i + 3]
                j += 1
            else:
                str = ""
                for x in range(i + 1, len(schedule)):
                    if schedule[x] != '(':
                        str += schedule[x]
                    else:
                        w[2][j] = schedule[x + 1]
                        break
                w[1][j] = int(str)
                j += 1

    return w


string = "r2(B)W2(A)R1(A)r3(A)w1(B)w2(B)W3(B)"
string2="r2(A)r1(A)w1(C)r3(C)w1(B)r4(B)w3(A)r4(C)w2(D)r2(B)w4(A)w4(B)"
read = readIndexer(string2)
write = writeIndexer(string2)
print("----------------------------------------------------------------")
print("This is the 'Read' operations in the Schedule:",read)
print()
print("----------------------------------------------------------------")
print("This is the Writes Operation in the Schedule:",write)
print()
print("----------------------------------------------------------------")
polygraph(read, write)

#GoodmanPole