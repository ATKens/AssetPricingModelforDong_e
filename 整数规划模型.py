""" 下列代码用于定义一个决策变量的集合，这些变量代表是否选择与某个经销商进行交易的二元决策（即，买或不买）。
在接下来的优化模型中，可以使用这些变量来添加必要的约束条件，以形成完整的数学模型，从而解决如何以最优成本进行采购的问题"""
import pulp

dealers = ["X", "Y", "Z"]
# 定义了两个成本字典 variable_costs 和 fixed_costs
variable_costs = {"X": 500, "Y": 350, "Z": 450}#各个商家的变动成本
fixed_costs = {"X": 4000, "Y": 2000, "Z": 6000}#各个商家的固定成本



"""
创建的字典这个样子
{'X': quantity_X, 'Y': quantity_Y, 'Z': quantity_Z}
{'X': orders_X, 'Y': orders_Y, 'Z': orders_Z}
"""
# 通过pulp库创建决策变量，返回值是字典，quantity是决策变量的前缀名，dealers是变量列表，lowBound=0指定最小值为0，cat=pulp.LpInteger指定数据类型为int型
quantities = pulp.LpVariable.dicts("quantity", dealers, lowBound=0, cat=pulp.LpInteger)
"""
通过pulp库创建决策变量，返回值是字典类型，orders是决策变量的前缀，dealers是变量列表，类型是二进制类型
例如，对于一个经销商 "X"，如果决定从他那里订购商品，则 "orders_X" 的值为 1；如果决定不从他那里订购，则 "orders_X" 的值为 0
"""
is_orders = pulp.LpVariable.dicts("orders", dealers, cat=pulp.LpBinary)

# 用PuLP库来定义和求解成本最小化问题的对象
model = pulp.LpProblem("A_cost_minimization_problem", pulp.LpMinimize)

""" 
向model添加目标函数,具体内容是variable_costs["X"]*quantities["X"] + fixed_costs["X"]*is_orders["X"]+\
variable_costs["Y"]*quantities["Y"] + fixed_costs["Y"]*is_orders["Y"]+\
variable_costs["Z"]*quantities["Z"] + fixed_costs["Z"]*is_orders["Z"]
"""
model += sum([variable_costs[i]*quantities[i] + fixed_costs[i]*is_orders[i] for i in dealers]), "Minimize_portfolio_cost"

"""
 添加∑ = quantities[i],具体内容
 quantities["X"]==150\
 quantities["Y"]==150\
 quantities["Z"]==150
 将上述约条件添加到model中
"""
model += sum([quantities[i] for i in dealers]) == 150, "Total_contracts_required"

# Other constraints (The exact names of constraints are not clear from the image)
model += is_orders["X"]*30 <= quantities["X"] <= is_orders["X"]*100, "Boundary_of_total_volume_of_X"
model += is_orders["Y"]*30 <= quantities["Y"] <= is_orders["Y"]*90, "Boundary_of_total_volume_of_Y"
model += is_orders["Z"]*30 <= quantities["Z"] <= is_orders["Z"]*70, "Boundary_of_total_volume_of_Z"

# Solve the model
model.solve()

# 打印优化结果
print("Minimization Results:")
for variable in model.variables():
    print(f"{variable.name} = {variable.varValue}")

# 打印总成本
print("Total cost: %s" % pulp.value(model.objective))
