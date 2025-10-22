# 用于记录在CCXI实习时用到的工具代码

import numpy as np
import pandas as pd

# def fill_report(src_df: pd.DataFrame, target_subjects: list) -> pd.DataFrame:
#     """
#     把「短报表」里的数值，按科目名称填到「长报表」对应科目行中；若科目不存在于短报表，则数值留空（""）。

#     参数
#     ----
#     src_df : pd.DataFrame
#         短报表，必须包含两列：'科目'(str) 和 '数值'(str)
#     target_subjects : list[str]
#         长报表的所有科目，顺序即最终输出顺序

#     返回
#     ----
#     pd.DataFrame
#         与 target_subjects 等长，两列均为字符串：'科目', '数值'
#     """
#     # 先把短报表做成字典：{科目: 数值}，方便快速查找
#     mapping = dict(zip(src_df['科目'].astype(str), src_df['数值'].astype(str)))

#     # 按长报表顺序逐个取值，找不到就留空字符串
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
    把「短报表」里的数值，按科目名称填到「长报表」对应科目行中；
    若短报表中该科目为 '-' 或不存在，则输出缺失值 NaN（后续可留空或按需要再转回空字符串）。

    参数
    ----
    src_df : pd.DataFrame
        短报表，必须包含两列：'科目'(str) 和 '数值'(str)
    target_subjects : list[str]
        长报表的所有科目，顺序即最终输出顺序

    返回
    ----
    pd.DataFrame
        与 target_subjects 等长，两列均为字符串：'科目', '数值'
        其中 '数值' 列缺失值用 NaN 表示（DataFrame 显示为空白）
    """
    # 先把短报表做成字典：{科目: 数值}，方便快速查找
    mapping = dict(zip(src_df['科目'].astype(str), src_df['数值'].astype(str)))

    # 按长报表顺序逐个取值
    filled_values = []
    for subj in target_subjects:
        val = mapping.get(str(subj), None)
        if val == '-':
            val = None
        filled_values.append(val)

    # 构造结果 DataFrame，显式指定 dtype=str 会让 NaN 变成字符串 'nan'，
    # 所以先允许 float 型 NaN，再整体转回字符串，NaN 会保留为缺失值
    result = pd.DataFrame({'科目': target_subjects, '数值': filled_values})

    # 把缺失值保持为 NaN，但列仍保持对象类型（object）
    # 如需导出 Excel/CSV 时留空，可直接使用
    return result

