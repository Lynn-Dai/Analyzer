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
                            # print(file_name)
                            for start, end, count in item[1]:
                                if max(start, start_line) <= min(end, end_line):
                                    print(entity['category'] + ": " + entity['qualifiedName'])
                                    entity['conflict'] = True
                                    entity['confLOC'] = min(end, end_line) - max(start, start_line) + 1
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

    with open("./conf_entity/lineage16.0-31664aa5de.json", 'w') as f_new:
        json.dump(res, f_new, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    get_conflict_detail("./conf_meths/lineage-16.0-meths.csv")
    read_json("lineage16.0-31664aa5de.json", "31664aa5defc5bc091dffc8201ef48e540aa21c7")
