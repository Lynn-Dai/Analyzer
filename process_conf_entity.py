import csv
import json
from collections import defaultdict
import pandas as pd

conf_files = defaultdict(list)


def get_conflict_detail(path: str):
    df = pd.read_csv(path, encoding="gbk")[['Conf_details', 'Loc_details']]
    for index, row in df.iterrows():
        conf_files[row['Conf_details']] = eval(row['Loc_details'])


def read_json(path: str):
    with open(path, 'r', encoding="utf-8") as f:
        data = json.loads(f.read())
        for entity in data['variables']:
            if 'File' in entity.keys():
                file_name = entity['File']
                if 'location' in entity.keys():
                    start_line = entity['location']['startLine']
                    end_line = entity['location']['endLine']
                    for item in conf_files.items():
                        if file_name in item[0]:
                            for start, end, count in item[1]:
                                if start >= start_line and end <= end_line:
                                    if entity['category'] == "Method":
                                        print("Method: " + entity['qualifiedName'])
                                if start <= start_line and end >= end_line:
                                    print("Var: " + entity['qualifiedName'])

# def read_java(path: str):


if __name__ == '__main__':
    get_conflict_detail("./conf_meths/lineage-19.1-meths.csv")
    read_json("E:/冲突节点与文件/冲突原文件/lineage19.1/lineage19.1-out.json")
