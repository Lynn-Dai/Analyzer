import csv
import json
from collections import defaultdict

import pandas as pd


def get_conflict_files(path: str):
    with open(path, encoding="utf-8") as f:
        conf_info = []
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            conf_details = []
            for index, column in enumerate(row):
                if index == 0:
                    # merge id
                    conf_details.append(column)
                elif index == 1:
                    # conf files num
                    conf_details.append(column)
                elif index == 2:
                    # conf java files num
                    conf_details.append(column)
                elif index == 3:
                    line = column.replace('\'', '\"')
                    ast = json.loads(line)
                    conf_files = []
                    conf_loc = []
                    sum_loc = 0
                    block_sum = 0
                    for file in ast:
                        # print(file[0])
                        conf_files.append(file[0])
                        conf_lines = 0
                        for customized_conf in file[1]:
                            block_sum = block_sum + 1
                            conf_lines = conf_lines + customized_conf[2]
                        sum_loc = sum_loc + conf_lines
                        conf_loc.append(conf_lines)
                    # conf_details.append(len(conf_files))
                    conf_details.append(str(conf_files))
                    conf_details.append(sum_loc)
                    conf_details.append(block_sum)
                    conf_details.append(conf_loc)
            conf_info.append(conf_details)
    return conf_info

def list_to_csv(data):
    name_attribute = ['Merge', 'Conf_files', 'Conf_javas', 'Conf_details', 'Loc', 'Block', 'Loc_details']
    writerCSV = pd.DataFrame(columns=name_attribute, data=data)
    writerCSV.to_csv('./conflicts/new-lineage-16.0-merge.csv', encoding='utf-8')


if __name__ == '__main__':
    ast_csv = "E:/PycharmProjects/DataExtraction/CustomizedAndroid/history/android_base/ast/lineage/lineage-16.0-merge.csv"
    list_to_csv(get_conflict_files(ast_csv))
