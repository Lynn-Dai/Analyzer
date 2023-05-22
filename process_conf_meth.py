import csv
import json

import pandas as pd


def get_conflict_files(path: str):
    with open(path, encoding="utf-8") as f:
        conf_info = []
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            for index, column in enumerate(row):
                # if index == 0:
                #     # merge id
                #     conf_details.append(column)
                # elif index == 1:
                #     # conf files num
                #     conf_details.append(column)
                # elif index == 2:
                #     # conf java files num
                #     conf_details.append(column)
                # elif index == 3:
                if index == 3:
                    line = column.replace('\'', '\"')
                    ast = json.loads(line)
                    for file in ast:
                        conf_details = []
                        conf_loc = []
                        sum_loc = 0
                        block_sum = 0
                        conf_meths = []
                        print(file[0])
                        conf_details.append(file[0])
                        for customized_conf in file[1]:
                            block_sum = block_sum + 1
                            # print(customized_conf[2])
                            start_line = customized_conf[0]
                            end_line = customized_conf[1]
                            conf_lines = customized_conf[2]
                            sum_loc = sum_loc + conf_lines
                            # print(customized_conf[4])
                            temp_conf_meths = process_meth(customized_conf[4])
                            conf_meths.extend(temp_conf_meths)
                            conf_loc.append((start_line, end_line, conf_lines))
                        conf_details.append(str(conf_meths))
                        conf_details.append(sum_loc)
                        conf_details.append(block_sum)
                        conf_details.append(conf_loc)
                        conf_info.append(conf_details)
    return conf_info


def process_meth(conf_info: list[str]):
    conf_meths = []
    # print(conf_info)
    for meth in conf_info:
        conf_parts = meth.split(" ")
        conf_class = conf_parts[0].replace("<", "").replace(":", "")
        conf_meth_return = conf_parts[1]
        conf_meth_name = conf_parts[2].split("(")[0]
        conf_meth_par = ""
        if not conf_parts[2].split("(")[1].startswith(")"):
            conf_meth_par = conf_parts[2].split("(")[1].split(")")[0]
        conf_meth_qualified_name = conf_class + "." + conf_meth_name
        # print(conf_meth_qualified_name)
        # print(conf_meth_return)
        # print(conf_meth_par)
        conf_meths.append(conf_meth_return+" "+conf_meth_qualified_name+"("+conf_meth_par+")")
    return conf_meths


def list_to_csv(data):
    name_attribute = ['Conf_details', 'Conf_methods', 'Loc', 'Block', 'Loc_details']
    writerCSV = pd.DataFrame(columns=name_attribute, data=data)
    writerCSV.to_csv('./conf_meths/omnirom-12.1-meths.csv', encoding='utf-8')



if __name__ == '__main__':
    ast_csv = "E:/PycharmProjects/DataExtraction/CustomizedAndroid/history/android_base/ast/omnirom/android-12.1-merge.csv"
    list_to_csv(get_conflict_files(ast_csv))
