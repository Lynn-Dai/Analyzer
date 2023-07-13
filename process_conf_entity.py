import csv
import json
from collections import defaultdict
import pandas as pd

conf_files = defaultdict(list)
res = []

def get_conflict_detail(path: str):
    df = pd.read_csv(path, encoding="gbk")[['Merge', 'Conf_details', 'Loc_details']]
    for index, row in df.iterrows():
        conf_files[row['Merge']+"-"+row['Conf_details']] = eval(row['Loc_details'])


def read_json(path: str, merge: str):
    with open(path, 'r', encoding="utf-8") as f:
        data = json.loads(f.read())
        for entity in data['variables']:
            if 'File' in entity.keys():
                file_name = entity['File']
                if 'location' in entity.keys():
                    start_line = entity['location']['startLine']
                    end_line = entity['location']['endLine']
                    for item in conf_files.items():
                        if file_name in item[0] and merge in item[0]:
                            for start, end, count in item[1]:
                                if start >= start_line and end <= end_line:
                                    if entity['category'] == "Method":
                                        print("Method: " + entity['qualifiedName'])
                                        entity['conflict'] = True
                                        entity['confLOC'] = count
                                        data.update(entity)
                                        res.append(entity)
                                if start <= start_line and end >= end_line:
                                    print("Var: " + entity['qualifiedName'])
                                    entity['conflict'] = True
                                    entity['confLOC'] = 1
                                    data.update(entity)
                                    res.append(entity)

    with open("./conf_entity/lineage19.1-8acf7b3981a55a3da70fd03d38b3645437b84d46.json", 'w') as f_new:
        json.dump(res, f_new, indent=4, ensure_ascii=False)


# def read_java(path: str):


if __name__ == '__main__':
    get_conflict_detail("./conf_meths/lineage-19.1-meths.csv")
    # 参数：依赖解析文件路径，发生冲突的merge的ID
    read_json("E:/冲突节点与文件/冲突原文件/lineage19.1/lineage19.1-8acf7b3981a55a3da70fd03d38b3645437b84d46.json", "8acf7b3981a55a3da70fd03d38b3645437b84d46")
