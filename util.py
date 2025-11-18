# 用于记录在这个机构实习时用到的工具代码

import numpy as np
import pandas as pd
import datetime
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
    在转录财报时遇见一个方面数据问题
    - 一些位置填写为 "-" , 需要处理成 NaN
    """
    # 循环遍历表格 将 '-' 替换为 NaN
    for i in range(len(df)):
        for j in range(len(df.columns)):
            if df.iloc[i, j] == '-':
                df.iloc[i, j] = np.nan
    return df

def pdf_to_table(PDF_NAME: str, start_loc: list, end_loc: list, drop_1row: bool = False) -> pd.DataFrame:
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

    drop_1row : bool
        是否删除第一行,默认为 False
    ---

    在财报中我们时常发现,有些表格是跨页的,所以需要用这个函数来提取跨页表格. 
    - start_loc 这个列表的第一个数字是起始页码(其并不是文件中标注的页码,而是真实的页码数的索引(从0开始)
    - start_loc 这个数字表示该页中的表格索引(从0开始). 
    比如在第10个页面中的第2个表格,那么start_loc就是[9, 2]
    end_loc同理,只不过表示的是结束页码和结束表格索引. 

    此外, 第一行经常只是对表格的说明,所以可以设置 drop_1row=True 来删除第一行.
    """

    df = []
    index_to_start = int(drop_1row)
    
    with pdfplumber.open(PDF_NAME) as pdf:
        for i in range(start_loc[0], end_loc[0]+1):
            if i == start_loc[0]:
                df.append( pd.DataFrame(pdf.pages[i].extract_tables()[start_loc[1]] ) )
            elif i == end_loc[0]:
                df.append( pd.DataFrame(pdf.pages[i].extract_tables()[end_loc[1]][index_to_start:] ) )
            else:
                df.append( pd.DataFrame(pdf.pages[i].extract_tables()[0][index_to_start:] ) )
        df = pd.concat(df, axis=0)

    return df



# 下面两个函数用于确定行权日

def dates_from_lst(s: list, filter_rule: list) -> str : 
    """
    从 兑付日清单(跨行长字符串 或者 列表) 中筛选出需要的日期
    ---
    s: 所有的兑付日, 跨行字符串形式
    filter: 用于挑选其中的行权日 如果需要第 19 , 39, 59 个行权日, 则 filter_rule = [19, 39, 59] 即可
    """
    if isinstance(s, str):
        s = s.strip().split('\n')
    # s = s.strip().split('\n')
    s = [ s[x-1] for x in filter_rule]
    s = [ x[0:4] + '-' + x[4:6] + '-' + x[6:8] for x in s]

    res = ';'.join(s)+';'
    print(res)
    # return res


def dates_after_years(year: int, month: int, day: int, # 起息日
                      filter_rule: list = [3,6,9,12,15], # 行权周期和次数
                      In_Advance: bool = False) -> str: # 是否提前到上一个工作日
    """
    从起息日出发, 生成若干个行权日, 并以特定字符串形式返回. 
    比如，初始起息日为 2025-11-11 每3年一个行权日; 然而如果当天是周末, 需要按照规则, 延后或者提前到下一个工作日!!!
    最后按照工作场景需求整理成特定字符串形式返回.
    ---
    year: 起息日年份
    month: 起息日月份
    day: 起息日日期
    filter_rule: 第几个行权日,, 比如第 3, 6, 9, 12, 15 个行权日. 默认为 [3,6,9,12,15]
    In_Advance: True 表示行权日提前到上一个工作日, False 表示行权日延后到下一个工作日 (默认为 False)
    """

    # 初始化
    dates_to_XingQuan = []

    # 循环生成行权日
    for i in filter_rule:
        d = datetime.datetime( year + i , month , day ) # 周期之后的对应日

        # 工作日判断
        weekday = d.weekday()

        if weekday == 5: # 如果是周六
            if In_Advance: # 提前到上一个工作日
                d = d - datetime.timedelta(days=1)
            else: # 延后到下一个工作日
                d = d + datetime.timedelta(days=2)

        elif weekday == 6: # 如果是周日
            if In_Advance: # 提前到上一个工作日
                d = d - datetime.timedelta(days=2)
            else: # 延后到下一个工作日
                d = d + datetime.timedelta(days=1)

        dates_to_XingQuan.append( d.strftime('%Y-%m-%d') ) # 添加到结果列表中

    print( ';'.join(dates_to_XingQuan)+';' )
    # return ';'.join(dates_to_XingQuan)+';'

