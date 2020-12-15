
from gurobipy import quicksum
import gurobipy as gp
from gurobipy import GRB
import random

l = 5 # total 5 nodes available
n = 20 # total 20 pods to be allocated 
m = 2 # 2 kinds of resources

# w = [[0 for i in range(l)] for i in range(n)] # Initailize the placement decision matrix
a = [[random.randint(1,5) for i in range(n)] for i in range(m)] # Initailize the resource request of each Pod
c = [[10 for i in range(l)] for i in range(m)] # Initailize the resource capacity of each node

try:

    # Create a new model
    model = gp.Model()

    # Create variables
    w = model.addVars(n, l, vtype=GRB.BINARY, name='pod_matrix')
    y = model.addVars(l, vtype=GRB.BINARY, name='node')

    # Set objective
    model.setObjective(quicksum(quicksum(w[i, k] for i in range(n)) for k in range(l)), GRB.MAXIMIZE)

    # Add constraint: pack each Pod in exactly one node
    model.addConstrs(quicksum(w[i, j] for j in range(l)) == 1 for i in range(n))

    # Add constraint: node capacity constraints
    model.addConstrs(quicksum((a[j][i] * w[i, k]) for i in range(n)) <= c[j][k] * y[k] for j in range(m) for k in range(l))

    # Optimize model
    model.optimize()

    # Results
    bin_for_item = [-1 for i in range(n)]
    for i in range(n):
        for j in range(l):
            if w[i, j].X > 0.5:
                bin_for_item[i] = j

    print("Bin assignment for each item: {}".format(bin_for_item))

    for v in model.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % model.objVal)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')