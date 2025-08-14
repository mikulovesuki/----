import numpy as np
import pandas as pd
from xlsxwriter import Workbook

print("正在读取数据 ...")
df = pd.read_excel("data_process/profit_filtered.xlsx")

print("数据预处理 ...")
df = df[["单品编码", "销量(千克)", "销售单价(元/千克)"]].values

def merge_table(data):
    first_col = data[:, 0]
    unique_vals, idx_first_occur = np.unique(first_col, return_index=True)
    
    sums = []
    for val in unique_vals:
        mask = (first_col == val)
        sum_val = np.sum(data[mask, 1])
        sums.append(sum_val)
    
    # 直接取首次出现的第三列值
    third_col = data[idx_first_occur, 2]
    
    result = np.column_stack((unique_vals, sums, third_col))
    return result

print("数据读取完成。开始合并数据 ...")
merged_data = merge_table(df)

print("数据合并完成。正在保存结果 ...")
merged_df = pd.DataFrame(merged_data, columns=["单品编码", "总销量(千克)", "销售单价(元/千克)"])
# merged_df.to_excel("fitting/merged_data.xlsx", index=False)

with pd.ExcelWriter("fitting/merged_data.xlsx", engine="xlsxwriter") as writer:
    merged_df.to_excel(writer, index=False, sheet_name="合并数据")
    
    # 获取工作簿和工作表对象
    workbook = writer.book
    worksheet = writer.sheets["合并数据"]
    
    # 创建数值格式（不显示科学计数法）
    number_format = workbook.add_format({"num_format": "0"})
    
    # 应用格式到第二列（B列）
    worksheet.set_column("A:A", None, number_format)