# 用于记录在这个机构实习时用到的工具代码

import numpy as np
import pandas as pd
import datetime
import pdfplumber

def get_sheet_rows(get_target_subjects: bool = False) -> dict:

    """
    默认报表的科目名称
    """

    rows = {} 

    rows['资产负债表'] = """货币资金
    以公允价值计量且其变动计入当期损益的金融资产
    衍生金融资产
    应收票据及应收账款
    应收票据
    应收账款
    预付款项
    应收利息
    应收股利
    其他应收款
    存货
    消耗性生物资产
    合同资产
    待摊费用
    持有待售资产
    一年内到期的非流动资产
    结算备付金
    拆出资金
    应收保费
    应收分保账款
    应收分保合同准备金
    买入返售金融资产
    其他流动资产
    流动资产差额(特殊报表科目)
    流动资产差额(合计平衡项目)
    流动资产合计
    债权投资
    其他债权投资
    可供出售金融资产
    其他权益工具投资
    持有至到期投资
    长期应收款
    长期股权投资
    投资性房地产
    固定资产
    固定资产清理
    在建工程
    工程物资
    生产性生物资产
    油气资产
    无形资产
    开发支出
    商誉
    长期待摊费用
    递延所得税资产
    发放贷款及垫款
    其他非流动资产
    非流动资产差额(特殊报表科目)
    非流动资产差额(合计平衡项目)
    非流动资产合计
    资产差额(特殊报表科目)
    资产差额(合计平衡项目)
    资产总计
    短期借款
    以公允价值计量且其变动计入当期损益的金融负债
    衍生金融负债
    应付票据及应付账款
    应付票据
    应付账款
    预收款项
    合同负债
    应付职工薪酬
    应交税费
    应付利息
    应付股利
    其他应付款
    预提费用
    持有待售负债
    一年内到期的非流动负债
    应付短期债券
    其他流动负债
    向中央银行借款
    吸收存款及同业存放
    拆入资金
    卖出回购金融资产款
    应付手续费及佣金
    应付分保账款
    保险合同准备金
    代理买卖证券款
    代理承销证券款
    流动负债差额(特殊报表科目)
    流动负债差额(合计平衡项目)
    流动负债合计
    长期借款
    应付债券
    长期应付款（合计）
    长期应付款
    专项应付款
    长期应付职工薪酬
    预计负债
    递延所得税负债
    递延收益
    其他非流动负债
    非流动负债差额(特殊报表科目)
    非流动负债差额(合计平衡项目)
    非流动负债合计
    负债差额(特殊报表科目)
    负债差额(合计平衡项目)
    负债合计
    实收资本
    其他权益工具
    其他权益工具：优先股
    其他权益工具：永续债
    资本公积
    减：库存股
    专项储备
    盈余公积
    其他综合收益
    一般风险准备
    外币报表折算差额
    未确认的投资损失
    未分配利润
    所有者权益差额(特殊报表科目)
    所有者权益差额(合计平衡项目)
    归属于母公司所有者权益合计
    少数股东权益
    所有者权益合计
    负债及所有者权益差额(特殊报表科目)
    负债及所有者权益差额(合计平衡项目)
    负债和所有者权益总计"""

    rows['利润表'] = """营业总收入
    其中：营业收入 
    利息收入 
    手续费及佣金收入 
    已赚保费 
    营业总成本
    其中：营业成本 
    利息支出 
    手续费及佣金支出 
    退保金 
    赔付支出净额 
    提取保险合同准备金净额 
    保单红利支出 
    分保费用 
    税金及附加 
    销售费用 
    管理费用 
    研发费用 
    财务费用 
        财务费用：利息费用 
        财务费用：利息收入 
    资产减值损失 
    信用减值损失 
    其他收益 
    投资收益 
    汇兑收益 
    净敞口套期收益 
    公允价值变动收益 
    资产处置收益 
    营业利润差额(特殊报表科目) 
    营业利润差额(合计平衡项目) 
    营业利润
    加：营业外收入 
    减：营业外支出 
    利润总额差额(特殊报表科目) 
    利润总额差额(合计平衡项目) 
    利润总额
    减：所得税 
    净利润差额(特殊报表科目) 
    净利润差额(合计平衡项目) 
    净利润
    归属于母公司所有者的净利润 
    少数股东损益 
    综合收益总额
    减：归属于少数股东的综合收益总额
    归属于母公司普通股东综合收益总额"""

    rows['现金流量表'] = """销售商品、提供劳务收到的现金 
    收到的税费返还 
    收到其他与经营活动有关的现金 
    客户存款和同业存放款项净增加额 
    向中央银行借款净增加额 
    向其他金融机构拆入资金净增加额 
    收到原保险合同保费取得的现金 
    收到再保险业务现金净额 
    保户储金及投资款净增加额 
    收取利息、手续费及佣金的现金 
    拆入资金净增加额 
    回购业务资金净增加额 
    经营活动现金流入差额(特殊报表科目) 
    经营活动现金流入差额(合计平衡项目) 
    经营活动现金流入小计 
    购买商品、接受劳务支付的现金
    支付给职工以及为职工支付的现金
    支付的各项税费
    支付其他与经营活动有关的现金
    客户贷款及垫款净增加额
    存放央行和同业款项净增加额
    支付原保险合同赔付款项的现金
    支付利息、手续费及佣金的现金
    支付保单红利的现金
    经营活动现金流出差额(特殊报表科目)
    经营活动现金流出差额(合计平衡项目)
    经营活动现金流出小计 
    经营活动产生的现金流量净额 
    收回投资收到的现金
    取得投资收益收到的现金
    处置固定资产、无形资产和其他长期资产收回的现金净额
    处置子公司及其他营业单位收到的现金净额
    收到其他与投资活动有关的现金
    投资活动现金流入差额(特殊报表科目)
    投资活动现金流入差额(合计平衡项目)
    投资活动现金流入小计 
    购建固定资产、无形资产和其他长期资产支付的现金 
    投资支付的现金 
    质押贷款净增加额 
    取得子公司及其他营业单位支付的现金净额 
    支付其他与投资活动有关的现金 
    投资活动现金流出差额(特殊报表科目) 
    投资活动现金流出差额(合计平衡项目) 
    投资活动现金流出小计 
    投资活动产生的现金流量净额 
    吸收投资收到的现金 
    取得借款收到的现金 
    发行债券收到的现金 
    收到其他与筹资活动有关的现金 
    筹资活动现金流入差额(特殊报表科目) 
    筹资活动现金流入差额(合计平衡项目) 
    筹资活动现金流入小计 
    偿还债务支付的现金 
    分配股利、利润或偿付利息支付的现金 
    支付其他与筹资活动有关的现金 
    筹资活动现金流出差额(特殊报表科目) 
    筹资活动现金流出差额(合计平衡项目) 
    筹资活动现金流出小计 
    筹资活动产生的现金流量净额 
    汇率变动对现金及现金等价物的影响 
    现金及现金等价物净增加额 
    期初现金及现金等价物余额 
    期末现金及现金等价物余额"""

    if get_target_subjects: return [get_target_subjects(x) for x in rows]
    else: return rows

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


def get_data(df, preprocess_profit_statement: bool = False): 
    """
    把我从各种材料(主要是pdf比较难搞)上面粘过来的字符串改写成 DataFrame
    ---
    参数
    ----
    df : str
        我从pdf上黏贴过来的字符串
    preprocess_profit_statement : bool
        是否对利润表进行预处理
    """

    res = pd.DataFrame([x.strip().split(' ') for x in df.split('\n')])

    if preprocess_profit_statement: return res
    else: return preprocess_income_statement(res)


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



def preprocess_income_statement(data: pd.DataFrame) -> pd.DataFrame:
    """
    对利润表进行预处理
    """
    res = data.copy()
    res.iloc[:,0] = ( 
        res.iloc[:,0]
        .replace('（损失以“－”号填列）', '')
        .replace('（净亏损以“－”号填列）', '')
        .replace('（亏损总额以“－”号填列）', '')
        .replace('减：所得税费用', '减：所得税')
        .replace('一、', '')
        .replace('二、', '')
        .replace('三、', '')
        .replace('四、', '')
        .replace('五、', '')
        .replace('六、', '')
        .replace('七、', '')
        .replace('1、', '')
        .replace('2、', '')
        .replace('(一)', '')
        .replace('(二)', '')
        .replace('加：其他收益', '其他收益')
    )
    return res


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


def delay(date:datetime.datetime) -> datetime.datetime: 
    """若不是工作日 则往后推到第一个工作日"""
    if date.weekday() == 5:
        return date + datetime.timedelta(days=2)
    elif date.weekday() == 6:
        return date + datetime.timedelta(days=1)
    else:
        return date
    

def workday_earlier(date:datetime.datetime, earlier:int = 10) -> datetime.datetime:
    """从特定日期出发，找到之前的第 earlier 个工作日"""
    count = 0
    while count < earlier:
        date -= datetime.timedelta(days=1)
        if date.weekday() < 5:
            count += 1
    return date


def take_workday(year, month, loc=20)->datetime.datetime:
    """计算某月第 loc 个工作日"""
    date = datetime.datetime(year, month, 1)
    count = 0 if date.weekday() >= 5 else 1 
    while count < loc:
        date += datetime.timedelta(days=1)
        if date.weekday() < 5:
            count += 1
    return date


def find_nth_workday(start_date: datetime.datetime, n: int, forward: bool = True) -> datetime.datetime:
    """从特定日期出发，找到之后/之前的第 n 个工作日"""
    count = 0
    while count < n:
        if forward:
            start_date += datetime.timedelta(days=1)
        else:
            start_date -= datetime.timedelta(days=1)
        if start_date.weekday() < 5:
            count += 1
    return start_date

def display_dates(dates_lst: list[datetime.datetime]) -> None:
    """按照公司的需求打印"""

    res = [d.strftime("%Y-%m-%d") for d in dates_lst]
    print(";".join(res) + ";")
