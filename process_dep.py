import json


def read_json(path: str):
    meth_entity = field_entity = type_entity = meth_match = field_match = type_match = 0
    with open(path, 'r') as f:
        data = json.loads(f.read())
        print(data['relationNum'])
        print(data['entityNum'])
        for entity in data['variables']:
            if entity['category'] == 'Method':
                meth_entity = meth_entity + 1
                if 'hidden' in entity:
                    meth_match = meth_match + 1
            elif entity['category'] == 'Variable' and entity['global'] == True:
                field_entity = field_entity + 1
                if 'hidden' in entity:
                    field_match = field_match + 1
            else:
                if entity['category'] == 'Class' or entity['category'] == 'Interface' or entity['category'] == 'Enum' or entity['category'] == 'Annotation':
                    type_entity = type_entity + 1
                    if 'hidden' in entity:
                        type_match = type_match + 1

        print(field_entity, field_match, meth_entity, meth_match, type_entity, type_match)


def read_commit(path: str):
    f = open(path, encoding="utf-8")
    lines = f.readlines()
    commit = 0
    for line in lines:
        if line.startswith('commit'):
            commit = commit + 1
    return commit


if __name__ == '__main__':
    file_path = "E:\\ASE\\实验数据\\2-Hidden\\匹配情况\\11\\hidden-11.json"
    read_json(file_path)

    print("--------------------------------------------------------")

    file_path = "E:\\ASE\\实验数据\\2-Hidden\\匹配情况\\12\\hidden-12.json"
    read_json(file_path)

    print("--------------------------------------------------------")

    file_path = "E:\\ASE\\实验数据\\2-Hidden\\匹配情况\\lineage-18.1\\base-out-lineage18.json"
    read_json(file_path)

    print("--------------------------------------------------------")

    file_path = "E:\\ASE\\实验数据\\2-Hidden\\匹配情况\\lineage-19.1\\base-out-lineage19.json"
    read_json(file_path)

    # commit_path = "E:/PycharmProjects/DataExtraction/CustomizedAndroid/history/android/branches/android12-gsi.txt"
    # print(read_commit(commit_path))
    # commit_path = "E:/PycharmProjects/DataExtraction/CustomizedAndroid/history/android/branches/simpleperf-release.txt"
    # print(read_commit(commit_path))
    # commit_path = "E:/PycharmProjects/DataExtraction/CustomizedAndroid/history/android/branches/android12-gsi.txt"
    # print(read_commit(commit_path))
    # commit_path = "E:/PycharmProjects/DataExtraction/CustomizedAndroid/history/android/branches/android10-qpr2-release.txt"
    # print(read_commit(commit_path))
