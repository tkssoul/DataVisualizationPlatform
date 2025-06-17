import numpy as np

# 生成一个形状为 (100,) 的随机数组，数组元素为 0 到 100 之间的整数
random_data = np.random.randint(0, 100, size=(100,))

# 保存数组到 npy 文件
np.save('random_data.npy', random_data)

print("随机的 npy 文件已生成，文件名为 random_data.npy")    