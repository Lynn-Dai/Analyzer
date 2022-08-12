import csv
import os
from collections import defaultdict

import pandas as pd

from process_intrustive import get_file_pkg

path = './coupling'


def process_coupling_pkg():
    for root, lists, files in os.walk(path):
        for file in files:
            result = defaultdict(list)
            version = file.split('.')[0]
            print(version)
            coupling_file_data = pd.read_csv(os.path.join(root, file), keep_default_na=False)
            for index, row in coupling_file_data.iterrows():
                pkg = get_file_pkg(row['filename'])
                count = []
                for key, num in row.items():
                    if 'Unnamed' in key or key == 'filename':
                        continue
                    if num == '':
                        count.append(0)
                    else:
                        count.append(float(num))
                # count = [row['FinalDel'], row['AccessibilityModify'], row['HiddenApi'],
                #          row['HiddenModify'], row['ParameterListModifyDep'], row['InnerExtensionClassUseDep'],
                #          row['InheritExtension'], row['ImplementExtension'],
                #          row['AggregationExtensionInterfaceClassDep'],
                #          row['InheritanceNative'], row['ImplementNative'], row['AggregationAOSPClassDep'],
                #          row['PublicInterfaceUseDep'], row['ReflectUse'], row['Conflict_times']]
                # print(count)
                if pkg in result.keys():
                    for i in range(len(count)):
                        # if count[i] == '':
                        #     result.get(pkg)[i] = result.get(pkg)[i] + 0
                        # else:
                        result.get(pkg)[i] = result.get(pkg)[i] + count[i]
                else:
                    result[pkg] = count
            # print(result)
            list_to_csv(os.path.join('./coupling-pkg/', version + '-pkg.csv'), result)


def list_to_csv(csv_path, data: defaultdict):
    header = ['filename', 'FinalDel', 'AccessibilityModify', 'HiddenApi', 'HiddenModify', 'ParameterListModifyDep',
              'InnerExtensionClassUseDep', 'InheritExtension', 'ImplementExtension',
              'AggregationExtensionInterfaceClassDep',
              'InheritanceNative', 'ImplementNative', 'AggregationAOSPClassDep', 'PublicInterfaceUseDep', 'ReflectUse',
              'Conflict_times']
    convert_result = []
    for key, value in data.items():
        temp = [key]
        temp.extend(value)
        convert_result.append(temp)
    writerCSV = pd.DataFrame(columns=header, data=convert_result)
    writerCSV.to_csv(csv_path, encoding='utf-8')
    # with open(csv_path, 'a', newline='', encoding='utf-8') as f:
    #     writer = csv.DictWriter(f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
    #     writer.writeheader()  # 写入列名
    #     [f.write('{0},{1}\n'.format(key, value)) for key, value in data.items()]
    # for key, value in data.items():
    #     f.write(key)
    #     for i in value:
    #         if i == 0:
    #             f.write('')
    #         else:
    #             f.write(str(i))
    #     f.write('\n')


if __name__ == '__main__':
    process_coupling_pkg()
