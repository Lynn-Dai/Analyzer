import csv
import os
from collections import defaultdict

import pandas as pd

path = 'E:/ASE/实验数据/3-侵入式修改'
Intrusive_files = 'ownership_file_count'
coupling_files = 'file-pattern'
conflicts_path = 'E:/PycharmProjects/Analyzer/conflicts'
intrusives = defaultdict(list)
conffiles = defaultdict(list)
responsible_field = defaultdict(list)

def process_responsible_field():
    data = pd.read_excel('./责任田信息.xlsx')
    for index, row in data.iterrows():
        # print(row['包含目录/文件'])
        if ';' in row['包含目录/文件']:
            responsible_field[row['责任田名称']].extend(row['包含目录/文件'].split(';'))
        else:
            responsible_field[row['责任田名称']].append(row['包含目录/文件'])
    print(responsible_field)

def get_file_pkg(file_path: str):
    if 'src' in file_path:
        file_path = file_path.split('src')[0]
    if 'java' in file_path:
        file_path = file_path.split('java')[0]
    if 'tests' in file_path and not file_path.startswith('tests'):
        file_path = file_path.split('tests')[0]
    return file_path

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

def get_conf_csvs():
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
        for item in row['Conf_details'][1:-1].split(', '):
            if item != '':
                # print(item)
                confs.append(item[1:-1])
    return confs


def get_conf_csv(version_couple: str):
    for root, lists, files in os.walk(conflicts_path):
        for file in files:
            version = file.split('-merge')[0]
            write = os.path.join(root, file)
            if version_couple in version:
                return write

def process_file_conf_times(data: pd.DataFrame, file_path: str):
    times = 0
    for index, row in data.iterrows():
        for item in row['Conf_details'][1:-1].split(', '):
            if file_path in item:
                times = times + 1
    return times


def process_coupling_pattern():
    for root, lists, files in os.walk(path):
        for file in files:
            if coupling_files in file:
                conf_times = []
                version = root.split('\\')[-1]
                write = os.path.join(root, file)
                print('%s %s' % (version, write))
                coupling_data = pd.read_csv(write)
                conf_data = pd.read_csv(get_conf_csv(version))
                # Go through the whole coupling files in current version
                for coupling_file in coupling_data['filename']:
                    conf_times.append(process_file_conf_times(conf_data, coupling_file))
                coupling_data['Conflict_times'] = conf_times
                coupling_data.to_csv(os.path.join('./coupling/', version+'.csv', ))


def filter_pkg(file_list: list):
    pkg = []
    for file in file_list:
        current_pkg = get_file_pkg(file)
        if current_pkg not in pkg:
            pkg.append(current_pkg)
    return pkg

def conf_vs_intrusive():
    result = []
    for conf_version,conf_files in conffiles.items():
        for intru_version,intru_files in intrusives.items():
            if intru_version in conf_version:
                version = [conf_version]
                conf_intrusive = []
                conf_not_intrusive = []
                for conf_file in conf_files:
                    if conf_file in intru_files:
                        conf_intrusive.append(conf_file)
                    else:
                        conf_not_intrusive.append(conf_file)
                version.append(len(filter_pkg(conf_intrusive)))
                version.append(str(filter_pkg(conf_intrusive)))
                version.append(len(filter_pkg(conf_not_intrusive)))
                version.append(str(filter_pkg(conf_not_intrusive)))
                version.append(len(conf_intrusive))
                version.append(len(conf_not_intrusive))
                version.append(str(conf_intrusive))
                version.append(str(conf_not_intrusive))
                result.append(version)
    return result

def output_intrusive(data):
    name_attribute = ['Project', 'Conf_intrusive_pkg', 'Conf_intrusive_pkgs', 'Conf_not_intrusive_pkg', 'Conf_not_intrusive_pkgs', 'Conf_intrusive', 'Conf_not_intrusive', 'Conf_intrusive_detail', 'Conf_not_intrusive_details']
    writerCSV = pd.DataFrame(columns=name_attribute, data=data)
    writerCSV.to_csv('./conf_vs_intrusive.csv', encoding='utf-8')

def list_to_csv(csv_path, data):
    with open(csv_path, 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in data.items()]


if __name__ == '__main__':
    list_to_csv('./Intrusive_files.csv', get_final_ownership())
    list_to_csv('./conf_files.csv', get_conf_csvs())
    # get_final_ownership()
    # get_merge_files()
    output_intrusive(conf_vs_intrusive())
    process_coupling_pattern()
    process_responsible_field()
