import os
from collections import defaultdict

import pandas as pd

conflicts_path = 'E:/PycharmProjects/Analyzer/conflict_blocks'
conf_files = defaultdict(list)
file_conf_times = {}

def get_conf_csvs():
    print("---获取各版本冲突信息---")
    for root, lists, files in os.walk(conflicts_path):
        for file in files:
            version = file.split('-merge')[0]
            write = os.path.join(root, file)
            print("%s %s" % (version, write))
            conf_files[version] = get_conf_files(write)
    return conf_files


def get_conf_files(merge_file: str):
    confs = []
    data = pd.read_csv(merge_file, usecols=[4])
    for index, row in data.iterrows():
        # print(row['Conf_details'])
        for item in row['Conf_details'][1:-1].split(', '):
            if item != '':
                # print(item)
                confs.append(item[1:-1])
    return confs

def get_all_conf_files(version_2_files: defaultdict):
    all_conf_files = []
    for key, value in version_2_files.items():
        for file_path in value:
            all_conf_files.append(file_path)
    return all_conf_files

def process_file_conf_times(data: list):
    for file in data:
        if file in file_conf_times.keys():
            file_conf_times[file] += 1
        else:
            file_conf_times[file] = 1

def list_to_csv(csv_path, data):
    with open(csv_path, 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in data.items()]


if __name__ == '__main__':
    process_file_conf_times(get_all_conf_files(get_conf_csvs()))
    list_to_csv("./conf_files_times.csv", file_conf_times)

