import csv
import json
from collections import defaultdict
import pandas as pd

conf_files = defaultdict(list)
res = []


def get_conflict_detail(path):
    df = pd.read_csv(path, encoding="gbk")[['Merge', 'Conf_details', 'Loc_details']]
    for index, row in df.iterrows():
        conf_files[row['Merge'] + "-" + row['Conf_details']] = eval(row['Loc_details'])


def read_json(path, merge):
    print(conf_files)
    with open(path, 'r') as f:
        data = json.loads(f.read())
        for entity in data['variables']:
            if 'File' in entity.keys():
                file_name = entity['File']
                if 'location' in entity.keys():
                    start_line = entity['location']['startLine']
                    end_line = entity['location']['endLine']
                    for item in conf_files.items():
                        if file_name in item[0] and merge in item[0]:
                            print(file_name)
                            for start, end, count in item[1]:
                                if max(start, start_line) < min(end, end_line):
                                    print(entity['category'] + ": " + entity['qualifiedName'])
                                    entity['conflict'] = True
                                    entity['confLOC'] = count
                                    data.update(entity)
                                    res.append(entity)
                                # if start >= start_line and end <= end_line:
                                #     if entity['category'] == "Method":
                                #         print("Method: " + entity['qualifiedName'])
                                #         entity['conflict'] = True
                                #         entity['confLOC'] = count
                                #         data.update(entity)
                                #         res.append(entity)
                                # if start <= start_line and end >= end_line:
                                #     print("Var: " + entity['qualifiedName'])
                                #     entity['conflict'] = True
                                #     entity['confLOC'] = 1
                                #     data.update(entity)
                                #     res.append(entity)

    with open("./conf_entity/lineage17.1-9d930f996e.json", 'w') as f_new:
        json.dump(res, f_new, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    get_conflict_detail("./conf_meths/lineage-17.1-meths.csv")
    read_json("lineage17.1-9d930f996e.json", "9d930f996e6d31820e201f4eb7dd7bf11127f932")
