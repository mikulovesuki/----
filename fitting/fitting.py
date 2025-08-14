import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def set_font():
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 使用黑体
    plt.rcParams["axes.unicode_minus"] = False    # 解决负号显示问题

set_font()

df = pd.read_excel("fitting/merged_data.xlsx")
x = df["销售单价(元/千克)"]
y = df["总销量(千克)"]

x_ln = np.log(x)
y_ln = np.log(y)

coefficients = np.polyfit(x_ln, y_ln, deg=1)
m, b = coefficients

print(f"斜率 m = {m:.4f}")
print(f"截距 b = {b:.4f}")


plt.figure(figsize=(10, 6))
plt.title("对数变换后的线性拟合 (ln(y) vs ln(x))", fontsize=14)
plt.xlabel("ln(销售单价)", fontsize=12)
plt.ylabel("ln(总销量)", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.text(0.05, 0.95, f"拟合公式: ln(y) = {m:.4f} * ln(x) + {b:.4f}\n"
                     f"幂函数形式: y = {np.exp(b):.4f} * x^{m:.4f}",
         transform=plt.gca().transAxes, fontsize=12,
         verticalalignment="top", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))


plt.scatter(x_ln, y_ln, color="blue", alpha=0.6, label="原始数据点")
y_ln_fit = m * x_ln + b
plt.plot(x_ln, y_ln_fit, color="red", linewidth=2, label=f"拟合直线: y = {m:.4f}x + {b:.4f}")

plt.tight_layout()

plt.savefig("fitting/fitting_plot.png", dpi=300, bbox_inches="tight")
plt.show()