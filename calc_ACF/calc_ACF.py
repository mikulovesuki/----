import os
import pandas as pd
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
import matplotlib.pyplot as plt

def set_font():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

def find_max_acf_lag(series, l, r):
    """
    在滞后区间 [l, r] 上找到最大 ACF 值对应的滞后阶数
    
    参数:
    series -- 时间序列数据 (pd.Series 或 np.array)
    l -- 最小滞后阶数 (整数)
    r -- 最大滞后阶数 (整数)
    
    返回值:
    max_lag -- 最大 ACF 值对应的滞后阶数
    max_acf -- 最大 ACF 值
    """
    # 计算 ACF 在 [0, r] 上的所有滞后阶数)
    acf_values = acf(series, nlags=r, fft=True)

    # 提取区间 [l, r] 的 ACF 值
    acf_subset = acf_values[l:r+1]

    # 找到最大 ACF 值的索引(+l 是因为跳过了前面的 l 个滞后阶数)
    raw_index = np.argmax(acf_subset)
    max_index = raw_index + l
    
    # 获取最大 ACF 值
    max_acf = acf_subset[raw_index]

    return max_index, max_acf

set_font()

print("正在读取数据 ...")
print(f"当前工作目录: {os.getcwd()}")
df = pd.read_excel('data_process/profit_filtered.xlsx')

print("数据预处理 ...")
# df['销售日期'] = pd.to_datetime(df['销售日期'], errors='coerce')
df['销售日期'] = pd.to_datetime(df['销售日期'])
df.set_index('销售日期', inplace=True)
df['销量(千克)'] = (df['销量(千克)'] - df['销量(千克)'].mean()) / df['销量(千克)'].std()

print("数据读取完成。开始计算自相关函数(ACF) ...")
# 绘制自相关图
plt.figure(figsize=(60, 30))

quarter_len = len(df['销量(千克)']) // 4
plot_acf(df['销量(千克)'], lags=quarter_len, alpha=0.05)  # alpha=0.05表示95%置信区间
plt.title("自相关函数(ACF)")
plt.xlabel('滞后阶数')
plt.ylabel('自相关系数')
plt.grid(True)
# plt.show()

print("自相关函数(ACF)计算绘制图形完成，正在保存图形 ...")
plt.savefig('ACF_plot.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.savefig('ACF_plot.svg', bbox_inches='tight', pad_inches=0.1)

plt.xlim(110000, 120000)
plt.savefig('ACF_plot_zoomed.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.savefig('ACF_plot_zoomed.svg', bbox_inches='tight', pad_inches=0.1)

print("图形保存完成。 开始查找最大 ACF 值 ...")
max_index, max_acf = find_max_acf_lag(df['销量(千克)'], 110000, 120000)
print(f"最大 ACF 值 {max_acf:.4f} 对应的滞后阶数为 {max_index}。") # 输出: 最大 ACF 值 0.0588 对应的滞后阶数为 115951。

print("结束")