import csv

import defaultlist as defaultlist
import pandas as pd
from collections import defaultdict

result = defaultdict(list)
common_lineage = []
common_honor = []
common = []


def remove_hidden_class():
    df = pd.read_excel('C:/Users/pc/Documents/3-侵入式修改/hidden/blacklist.xlsx', sheet_name='Sheet1')
    for index, row in df.iterrows():
        # print(index, row['lineage18'], row['lineage19'], row['honor_r'], row['honor_s'])
        if type(row['lineage18']) != float and row['lineage18'].split('.')[-1][0].isupper() is False:
            result['lineage18'].append(row['lineage18'])
        if type(row['lineage19']) != float and row['lineage19'].split('.')[-1][0].isupper() is False:
            result['lineage19'].append(row['lineage19'])
        if type(row['honor_r']) != float and row['honor_r'].split('.')[-1][0].isupper() is False:
            result['honor_r'].append(row['honor_r'])
        if row['honor_s'].split('.')[-1][0].isupper() is False:
            result['honor_s'].append(row['honor_s'])
    return result
    # 新建一个工作簿
    # writer = pd.ExcelWriter('E:\\研究生学习\\python数据\\实验数据\\Excel文件实验数据\\sale_january_2017_in_pandas.xlsx')
    # 使用to_excel将之前读取的工作簿中工作表的数据写入到新建的工作簿的工作表中
    # data_frame.to_excel(writer, sheet_name='jan_2017_output_sheet', index=False)
    # 保存并且关闭工作簿
    # writer.save()


def resolve_common():
    for api in result['lineage18']:
        if api in result['lineage19']:
            print('lineage ' + api)
            common_lineage.append(api)
    for api in result['honor_r']:
        if api in result['honor_s']:
            print('honor ' + api)
            common_honor.append(api)
    for api in common_lineage:
        if api in common_honor:
            common.append(api)


def dict_to_csv(data_dict, file_name):
    with open(file_name, 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in data_dict.items()]
        f.write('{0},{1}\n'.format('common_lineage', common_lineage))
        f.write('{0},{1}\n'.format('common_honor', common_honor))
        f.write('{0},{1}\n'.format('common', common))


if __name__ == '__main__':
    out = remove_hidden_class()
    resolve_common()
    dict_to_csv(out, './blacklist.csv')
