import json
from collections import defaultdict


def json_to_python(filepath):
    f = open(filepath, 'r', encoding='utf-8')
    s = f.read()
    data = json.loads(s)
    return data


def get_values(data):
    return data['res']['values']


'''
Return dict{"anti-pattern": [files]}
'''
def process_anti_file(data):
    print("CURRENT FILE ANTI RESULT: ")
    data_dict = defaultdict(list)
    for value in get_values(data):
        print(value)
        print(get_values(data)[value]['count'])
        res = get_values(data)[value]['res']
        for r in res:
            # print(r['resCount'])
            for anti_relations in r['res']:
                for anti_relation in anti_relations:
                    if anti_relation['src']['File'] not in data_dict[value]:
                        data_dict[value].append(anti_relation['src']['File'])
                    if anti_relation['dest']['File'] not in data_dict[value]:
                        data_dict[value].append(anti_relation['dest']['File'])
                    # print(anti_relation['src']['File'])
                    # print(anti_relation['dest']['File'])
            # print(r['filterCount'])
    return data_dict


'''
Check whether one file may contain multiple anti-patterns
'''
def convert_to_file(data: dict):
    file_dict = defaultdict(list)
    for anti in data.keys():
        for file in data[anti]:
            file_dict[file].append(anti)
    return file_dict


'''
Get all files which contain anti-pattern.
'''
def get_anti_files(data: dict):
    file_list = []
    for anti in data.keys():
        for file in data[anti]:
            file_list.append(file)
    return file_list


def dict_to_json_write_file(data_dict, filename):
    with open(filename, 'w') as f:
        json.dump(data_dict, f, sort_keys=True, indent=4, separators=(',', ':'))


if __name__ == '__main__':
    anti_result = "E:\ASE\反模式结果\LA.QSSI.12.0.r1-05800.01-qssi.0.json"
    anti_files = process_anti_file(json_to_python(anti_result))
    file_antis = convert_to_file(anti_files)
    dict_to_json_write_file(file_antis, "conflicts/LA.QSSI.12.0.r1-05800.01-qssi.0.json")
