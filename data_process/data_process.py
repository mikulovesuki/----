import pandas as pd
import numpy as np
import xlwings as xw

print("正在读取附录2 ...")
with xw.Book('附件2.xlsx') as book1:
    sheet1 = book1.sheets[0]
    df1 = sheet1.used_range.options(pd.DataFrame, header=True, index=False).value

    print("正在读取附录3 ...")
    with xw.Book('附件3.xlsx') as book2:
        sheet2 = book2.sheets[0]
        df2 = sheet2.used_range.options(pd.DataFrame, header=True, index=False).value

        print("正在计算利润 ...")
        for idx, row in df1[:].iterrows():
            if idx % 1000 == 0:
                print(f"Processing row {idx + 1} of {len(df1)}, {idx / len(df1) * 100:.2f}% complete")
            product_code = row['单品编码']
            wholesale_price = df2.loc[df2['单品编码'] == product_code, '批发价格(元/千克)']
            if not wholesale_price.empty:
                profit = row['销售单价(元/千克)'] - wholesale_price.values[0]
                df1.at[idx, '利润'] = profit

    print("正在过滤异常值 ...")

    data_series = df1['利润']
    mean_val = data_series.mean()
    std_val = data_series.std()

    lower_bound = mean_val - 3 * std_val
    upper_bound = mean_val + 3 * std_val
    print(f"利润的均值: {mean_val}, 标准差: {std_val}")

    # 记录被删除的行号
    removed_indices = df1.index[
        (~((data_series >= lower_bound) & (data_series <= upper_bound))) & (~data_series.isna())
    ]
    print(f"被删除的行号: {list(removed_indices)}")

    # 将利润写入H列
    sheet1.range('H1').value = '利润'
    sheet1.range('H2').options(index=False, header=False).value = df1['利润'].values.reshape(-1, 1)
    sheet1.range('H:H').api.HorizontalAlignment = -4108  # -4108 代表xlHAlignCenter

    # 删除异常值对应的行（Excel中行号需加2，因为DataFrame索引从0开始且Excel有表头）
    for idx in removed_indices:
        excel_row = idx + 2
        sheet1.range(f"{excel_row}:{excel_row}").delete()

    # 保存结果
    book1.save('profit_filtered.xlsx')

    print("数据处理完成。结果已保存到 'profit_filtered.xlsx'。")