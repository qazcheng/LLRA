import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件为DataFrame
df = pd.read_excel('data.xlsx')

# 获取数据列
list_1 = df['time']
list_3 = df['100']
list_4 = df['103']

# 创建折线图
plt.figure(figsize=(10, 6))
plt.plot(list_1, list_3, label='List 3', marker='o', color='blue', linestyle='-', linewidth=2)
plt.plot(list_1, list_4, label='List 4', marker='x', color='red', linestyle='-', linewidth=2)

# 设置图例
plt.legend()

# 设置图标题和坐标轴标签
plt.title('Line Plot of List 3 and List 4')
plt.xlabel('Time (seconds)')
plt.ylabel('Values')

# 显示图
plt.grid(True)
plt.show()
