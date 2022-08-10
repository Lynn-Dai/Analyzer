import csv
import os
from collections import defaultdict

import pandas as pd

path = 'E:/ASE/实验数据/3-侵入式修改'
Intrusive_files = 'ownership_file_count'
conflicts_path = 'E:/PycharmProjects/Analyzer/conflicts'
intrusives = defaultdict(list)
conffiles = defaultdict(list)

def get_final_ownership():
    for root, lists, files in os.walk(path):
        for file in files:
            if Intrusive_files in file:
                version = root.split('\\')[-1]
                write = os.path.join(root, file)
                print('%s %s' % (version, write))
                intrusives[version] = get_intrusive_files(write)
    return intrusives

def get_intrusive_files(ownership_file: str):
    intrusive = []
    with open(ownership_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['intrusive'] != '':
                intrusive.append(row['file'])
    return intrusive

def get_merge_files():
    for root, lists, files in os.walk(conflicts_path):
        for file in files:
            version = file.split('-merge')[0]
            write = os.path.join(root, file)
            print("%s %s" % (version, write))
            conffiles[version] = get_conf_files(write)
    return conffiles

def get_conf_files(merge_file: str):
    confs = []
    data = pd.read_csv(merge_file, usecols=[4])
    for index, row in data.iterrows():
        # print(row['Conf_details'])
        for item in row['Conf_details'][1:-1].split(','):
            if item != '':
                confs.append(item[1:-1])
    return confs


def list_to_csv(csv_path, data):
    with open(csv_path, 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in data.items()]


if __name__ == '__main__':
    # list_to_csv('./Intrusive_files.csv', get_final_ownership())
    # list_to_csv('./conf_files.csv', get_merge_files())
    get_final_ownership()
    get_merge_files()
