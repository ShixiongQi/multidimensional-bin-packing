from gurobipy import quicksum
import gurobipy as gp
from gurobipy import GRB
import random

l = 5 # total 5 nodes available
n = 6 # total 6 functions to be deployed 
m = 2 # 2 kinds of resources

n_r = [random.randint(1,4) for i in range(n)] # the number of Pods requested by function r
a = [[[random.randint(1,5) for i in range(n_r[r])] for r in range(n)] for j in range(m)] # Initailize the amount of resource j that requested by i-th Pod in function r
c = [[10 for i in range(l)] for i in range(m)] # Initailize the resource capacity of each node

try:

    # Create a new model
    model = gp.Model()

    # Create variables
    y = model.addVars(l, vtype=GRB.BINARY, name='node_usage')
    w = [model.addVars(n_r[r], l, vtype=GRB.BINARY, name='func'+str(r)) for r in range(n)] 
    # Set objective
    model.setObjective(quicksum(quicksum(quicksum(w[r][i, k] for i in range(n_r[r])) for r in range(n)) for k in range(l)), GRB.MAXIMIZE)

    # Add constraint: pack each Pod in exactly one node
    # model.addConstrs((quicksum(w[r][i, k] for k in range(l)) <= 1 for i in range(n_r[r]) for r in range(n)), "c0")
    for r in range(n):
        model.addConstrs((quicksum(w[r][i, k] for k in range(l)) <= 1 for i in range(n_r[r])), "c0")

    # Add constraint: node capacity constraints
    # for k in range(l):
        # model.addConstrs((quicksum((a[j][r][i] * w[r][i, k]) for i in range(n_r[r]) for r in range(n)) <= c[j][k] * y[k] for j in range(m)), "c1" + str(k))
    for k in range(l):
        for j in range(m):
            # c[j][k] * y[k]
            req_sum = 0
            for r in range(n):
                temp = 0
                for i in range(n_r[r]):
                    temp = temp + a[j][r][i] * w[r][i,k]
                req_sum = req_sum + temp
            model.addConstr(req_sum <= c[j][k] * y[k])
    
    # Optimize model
    model.optimize()

    # Results
    bin_for_item = [[-1 for i in range(n_r[r])] for r in range(n)]
    for r in range(n):
        for i in range(n_r[r]):
            for k in range(l):
                if w[r][i, k].X > 0.5:
                    bin_for_item[r][i] = k
                    print(k, " ", end="")

    print("Bin assignment for each item: {}".format(bin_for_item))

    # for v in model.getVars():
        # print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % model.objVal)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
    print('Optimization was stopped with status %d' % model.status)
    # do IIS, find infeasible constraints
    model.computeIIS()
    model.write("model.ilp")
    # for c in model.getConstrs():
    #     if c.IISConstr:
    #         print('%s' % c.constrName)