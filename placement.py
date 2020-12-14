#!/usr/bin/env python3.7

# This example formulates and solves the following Multidimensional Bin Packing (BIP) model:
# l nodes, n pods
#  maximize
#        sum(sum(i) for i in w)
#  subject to
#        x + 2 y + 3 z <= 4
#        x +   y       >= 1
#        x, y, z binary

import gurobipy as gp
from gurobipy import GRB

l = 5 # total 5 nodes available
n = 20 # total 20 pods to be allocated 
m = 2 # 2 kinds of resources

w = [[0 for i in range(l)] for i in range(n)] # Initailize the placement decision matrix
a = [[0 for i in range(m)] for i in range(n)] # Initailize the resource request of each Pod
c = [[0 for i in range(m)] for i in range(l)] # Initailize the resource capacity of each node

try:

    # Create a new model
    # m = gp.Model("mip1")
    m = gp.Model("bip")

    # Create variables
    # x = m.addVar(vtype=GRB.BINARY, name="x")
    for k in range (0, l):
        for i in range (0, n):
            var_name = "w[" + str(k) + "][" + str(i) + "]"
            w[i][k] = m.addVar(vtype=GRB.BINARY, name=var_name)

    # Set objective
    # m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)
    m.setObjective(sum(sum(i) for i in w), GRB.MAXIMIZE)

    # Add constraint: resource constraints
    # m.addConstr(x + 2 * y + 3 * z <= 4, "c0")
    condition_idx = 0
    for k in range(l):
        for j in range(m):
            resource_request = 0
            for i in range(n):
                resource_request = resource_request + a[i][j] * w[i][k]
            m.addConstr(resource_request <= c[j][k] * y[k], "c1-" + str(condition_idx))
            condition_idx = condition_idx + 1

    # Add constraint: Pod can only be placed to one node
    condition_idx = 0
    for i in range(n):
        sum_w = 0
        for k in range(l):
            sum_w = sum_w + w[i][k]
        m.addConstr(sum_w == 1, "c2-" + str(condition_idx))
        condition_idx = condition_idx + 1
            

    # Optimize model
    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')