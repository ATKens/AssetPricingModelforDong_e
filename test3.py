# 重新导入NumPy库并定义系数矩阵A和常数向量B
import numpy as np

A = np.array([[2, 1, 1], [1, 3, 2], [1, 0, 0]])
B = np.array([4, 5, 6])

# 使用NumPy的linalg.solve方法求解x
x = np.linalg.solve(A, B)

print(x)