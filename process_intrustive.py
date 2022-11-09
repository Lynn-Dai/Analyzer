import csv
import os
from collections import defaultdict

import pandas as pd

path = 'E:/ASE/实验数据/3-侵入式修改'
Intrusive_files = 'final_ownership_file_count'
coupling_files = 'file-pattern'
Intrusive_details = 'intrusive_file_count'
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
    # print(responsible_field)


def process_responsible_file_pkg(file_path: str):
    # print(get_file_pkg(file_path[1:]))
    return get_file_pkg(file_path[1:])


def get_file_responsible(file_path: str):
    file_path = '/' + file_path
    for key, value in responsible_field.items():
        if file_path in value:
            # print(file_path)
            return key, process_responsible_file_pkg(file_path)
        for pkg_or_file in value:
            if file_path.startswith(pkg_or_file):
                # print(pkg_or_file)
                return key, pkg_or_file
    return '', process_responsible_file_pkg(file_path)


def get_file_pkg(file_path: str):
    # if 'src' in file_path:
    #     file_path = file_path.split('src')[0]
    # if 'java' in file_path:
    #     file_path = file_path.split('java')[0]
    # if 'tests' in file_path and not file_path.startswith('tests'):
    #     file_path = file_path.split('tests')[0]
    pkg = '/'
    for file_piece in file_path.split('/'):
        if not file_piece[0].isupper():
            pkg = pkg + file_piece + '/'
        elif file_piece.endswith('.java'):
            break
        else:
            pkg = pkg + file_piece + '/'
            # break
    return pkg


def get_final_ownership():
    print("--获取是否为侵入式文件--")
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
    print("---获取各版本冲突信息---")
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

def get_couple_csv(version_intrusive: str):
    for root, lists, files in os.walk('./coupling'):
        for file in files:
            version = file.split('.')[0]
            write = os.path.join(root, file)
            if version_intrusive in version:
                return write


def process_file_conf_times(data: pd.DataFrame, file_path: str):
    times = 0
    for index, row in data.iterrows():
        for item in row['Conf_details'][1:-1].split(', '):
            if file_path in item:
                times = times + 1
    return times


def process_coupling_pattern():
    print("--获取耦合信息--")
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
                coupling_data = coupling_data.fillna(0)
                coupling_data.to_csv(os.path.join('./coupling/', version + '.csv', ))


def process_intrusive_detail():
    print("--获取侵入式细节信息--")
    for root, lists, files in os.walk(path):
        for file in files:
            if Intrusive_details in file:
                conf_times = []
                version = root.split('\\')[-1]
                write = os.path.join(root, file)
                print('%s %s' % (version, write))
                coupling_data = pd.read_csv(write)
                conf_data = pd.read_csv(get_conf_csv(version))
                # Go through the whole coupling files in current version
                for coupling_file in coupling_data['file']:
                    conf_times.append(process_file_conf_times(conf_data, coupling_file))
                coupling_data['Conflict_times'] = conf_times
                coupling_data = coupling_data.fillna(0)
                coupling_data.to_csv(os.path.join('./intrusive/', version + '.csv', ))


def filter_pkg(file_list: list):
    pkg = []
    res = []
    for file in file_list:
        responsible, current_pkg = get_file_responsible(file)
        # if responsible == '':
        #     current_pkg = get_file_pkg(file)
        # print(current_pkg)
        if current_pkg not in pkg:
            pkg.append(current_pkg)
        if responsible not in res and responsible != '':
            res.append(responsible)
    return res, pkg


def conf_vs_intrusive():
    result = []
    for conf_version, conf_files in conffiles.items():
        for intru_version, intru_files in intrusives.items():
            if intru_version in conf_version:
                version = [conf_version]
                conf_intrusive = []
                conf_not_intrusive = []
                for conf_file in conf_files:
                    if conf_file in intru_files:
                        conf_intrusive.append(conf_file)
                    else:
                        conf_not_intrusive.append(conf_file)
                res, pkg = filter_pkg(conf_intrusive)
                version.append(len(res))
                version.append(len(pkg))
                version.append(str(res))
                version.append(str(pkg))
                res, pkg = filter_pkg(conf_not_intrusive)
                version.append(len(res))
                version.append(len(pkg))
                version.append(str(res))
                version.append(str(pkg))
                version.append(len(conf_intrusive))
                version.append(len(conf_not_intrusive))
                version.append(str(conf_intrusive))
                version.append(str(conf_not_intrusive))
                result.append(version)
    return result


def output_intrusive(data):
    name_attribute = ['Project', 'Conf_Intru_Res_Num', 'Conf_intrusive_Pkg_Num', 'Conf_Intru_Res',
                      'Conf_intrusive_pkgs',
                      'Conf_Not_Intru_Res_Num', 'Conf_Not_intrusive_Pkg_Num', 'Conf_Not_Intru_Res',
                      'Conf_Not_intrusive_pkgs',
                      'Conf_intrusive', 'Conf_not_intrusive', 'Conf_intrusive_detail', 'Conf_not_intrusive_details']
    writerCSV = pd.DataFrame(columns=name_attribute, data=data)
    writerCSV.to_csv('./conf_vs_intrusive.csv', encoding='utf-8')


def list_to_csv(csv_path, data):
    with open(csv_path, 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in data.items()]


def merge_csv():
    for root, lists, files in os.walk('./intrusive'):
        for file in files:
            version = file.split('.')[0]
            write = os.path.join(root, file)
            print('%s %s' % (version, write))
            intrusive_data = pd.read_csv(write)
            couple_data = pd.read_csv(get_couple_csv(version))
            result = pd.merge(intrusive_data, couple_data, left_on='file', right_on='filename')
            result.to_csv('./intrusive_couple_conf/'+version+'.csv', encoding='utf-8')


if __name__ == '__main__':
    process_responsible_field()
    list_to_csv('./Intrusive_files.csv', get_final_ownership())
    list_to_csv('./conf_files.csv', get_conf_csvs())
    # get_final_ownership()
    # get_merge_files()
    output_intrusive(conf_vs_intrusive())
    process_coupling_pattern()
    process_intrusive_detail()
    merge_csv()
