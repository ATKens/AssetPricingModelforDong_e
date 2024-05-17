import numpy as np

# 定义系数矩阵 A 和常数向量 B
A = np.array([[2, 1, 1], [1, 3, 2], [1, 0, 0]])
B = np.array([4, 5, 6])

# 使用 numpy.linalg.solve 解方程组
x = np.linalg.solve(A, B)

print("解向量 x:", x)
