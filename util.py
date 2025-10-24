# 用于记录在CCXI实习时用到的工具代码

import numpy as np
import pandas as pd
import pdfplumber

# def fill_report(src_df: pd.DataFrame, target_subjects: list) -> pd.DataFrame:
#     """
#     把「短报表」里的数值,按科目名称填到「长报表」对应科目行中；若科目不存在于短报表,则数值留空(""). 

#     参数
#     ----
#     src_df : pd.DataFrame
#         短报表,必须包含两列：'科目'(str) 和 '数值'(str)
#     target_subjects : list[str]
#         长报表的所有科目,顺序即最终输出顺序

#     返回
#     ----
#     pd.DataFrame
#         与 target_subjects 等长,两列均为字符串：'科目', '数值'
#     """
#     # 先把短报表做成字典：{科目: 数值},方便快速查找
#     mapping = dict(zip(src_df['科目'].astype(str), src_df['数值'].astype(str)))

#     # 按长报表顺序逐个取值,找不到就留空字符串
#     filled_values = [mapping.get(str(subj), "") for subj in target_subjects]

#     return pd.DataFrame({'科目': target_subjects, '数值': filled_values}, dtype=str)


def get_data(df): 
    """
    把我从各种材料(主要是pdf比较难搞)上面黏贴过来的字符串改写成 DataFrame
    """
    return pd.DataFrame([x.strip().split(' ') for x in df.split('\n')])


def get_target_subjects(lst_index):
    """
    把我从pdf上黏贴过来的科目列表改写成 list[str]
    """
    return [x.strip() for x in lst_index.split()]


def fill_report(src_df: pd.DataFrame, target_subjects: list) -> pd.DataFrame:
    """
    把「短报表」里的数值,按科目名称填到「长报表」对应科目行中；
    若短报表中该科目为 '-' 或不存在,则输出缺失值 NaN(后续可留空或按需要再转回空字符串). 

    参数
    ----
    src_df : pd.DataFrame
        短报表,必须包含两列：'科目'(str) 和 '数值'(str)
    target_subjects : list[str]
        长报表的所有科目,顺序即最终输出顺序

    返回
    ----
    pd.DataFrame
        与 target_subjects 等长,两列均为字符串：'科目', '数值'
        其中 '数值' 列缺失值用 NaN 表示(DataFrame 显示为空白)
    """
    # 先把短报表做成字典：{科目: 数值},方便快速查找
    mapping = dict(zip(src_df['科目'].astype(str), src_df['数值'].astype(str)))

    # 按长报表顺序逐个取值
    filled_values = []
    for subj in target_subjects:
        val = mapping.get(str(subj), None)
        if val == '-':
            val = None
        filled_values.append(val)

    # 构造结果 DataFrame,显式指定 dtype=str 会让 NaN 变成字符串 'nan',
    # 所以先允许 float 型 NaN,再整体转回字符串,NaN 会保留为缺失值
    result = pd.DataFrame({'科目': target_subjects, '数值': filled_values})

    # 把缺失值保持为 NaN,但列仍保持对象类型(object)
    # 如需导出 Excel/CSV 时留空,可直接使用
    return result

def get_float(num: str) -> float: 
    """
    数值字符串有千分位分隔符, 如 "1,234,567.89" 
    需要处理成一般的浮点数: 1234567.89
    """
    return float(num.replace(',', ''))

def make_table_num(df: pd.DataFrame) -> pd.DataFrame :
    """
    在转录财报时遇见两方面数据问题
    - 数值有千分位分隔符, 需要处理成一般的浮点数
    - 一些位置填写为 "-" , 需要处理成 NaN
    """
    for i in range(len(df)):
        if df.iloc[i, 1] == '-':
            df.iloc[i, 1] = np.nan
        else:
            df.iloc[i, 1] = get_float(df.iloc[i, 1])
    return df

def pdf_to_table(PDF_NAME: list, start_loc: list, end_loc: list) -> pd.DataFrame:
    """
    该函数依赖 pdfplumber 库,用于从 PDF 文件中提取表格数据. 

    参数
    ----
    PDF_NAME : str
    - PDF 文件名 / PDF 文件路径 两者都可以
    start_loc : list[int, int]
        起始页码和起始表格索引
    end_loc : list[int, int]
    - 结束页码和结束表格索引
    ---

    在财报中我们时常发现,有些表格是跨页的,所以需要用这个函数来提取跨页表格. 
    - start_loc 这个列表的第一个数字是起始页码(其并不是文件中标注的页码,而是真实的页码数的索引(从0开始)
    - start_loc 这个数字表示该页中的表格索引(从0开始). 
    比如在第10个页面中的第2个表格,那么start_loc就是[9, 2]
    end_loc同理,只不过表示的是结束页码和结束表格索引. 
    """
    with pdfplumber.open(PDF_NAME) as pdf:
        df = []
        for i in range(start_loc[0], end_loc[0]+1):
            if i == start_loc[0]:
                df.append(pd.DataFrame(pdf.pages[i].extract_tables()[start_loc[1]]))
            elif i == end_loc[0]:
                df.append(pd.DataFrame(pdf.pages[i].extract_tables()[end_loc[1]]))
            else:
                df.append(pd.DataFrame(pdf.pages[i].extract_tables()[0]))
        df = pd.concat(df, axis=0)
    return df.copy()



