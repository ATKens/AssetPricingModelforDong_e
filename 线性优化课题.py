""" 一个简单的线性优化问题，包含两个变量 """
import pulp

x = pulp.LpVariable("x", lowBound=0)#创建了一个名为 x 的决策变量，并设置其最小可能值为0
y = pulp.LpVariable("y", lowBound=0)#创建了一个名为 y 的决策变量，并设置其最小可能值为0

problem = pulp.LpProblem("A_simple_maximization_objective", pulp.LpMaximize)#这里初始化成求自变量最大值的，也可以设置求最小值的
problem += 3*x + 2*y, "The_objective_function"
problem += 2*x + y <= 100, "1st_constraint"
problem += x + y <= 80, "2nd_constraint"
problem += x <= 40, "3rd_constraint"
problem.solve()
