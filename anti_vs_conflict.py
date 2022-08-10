from anti_analyzer import process_anti_file, json_to_python, get_anti_files
from process_conflict import get_conflict_files

'''
Get the files which both in conflicts and anti-patterns, or both in different versions.
'''
def get_same_files(anti_path: str, conflict_path: str):
    same_files = []
    for file in anti_files:
        if file in conflict_files:
            same_files.append(file)
    return same_files


if __name__ == '__main__':
    anti_result = "E:\\ASE\\反模式结果\\lineage-18.1.json"
    # conflict_result = "E:\\PycharmProjects\\DataExtraction\\CustomizedAndroid\\history\\android_base\\ast\\omnirom\\android-10-merge.csv"
    conflict_result = "E:\\ASE\\反模式结果\\lineage-18.1.json"
    anti_files = get_anti_files(process_anti_file(json_to_python(anti_result)))
    print("anti files num:")
    print(len(anti_files))
    # conflict_files = get_conflict_files(conflict_result)
    conflict_files = get_anti_files(process_anti_file(json_to_python(conflict_result)))
    print("conflict files num")
    print(len(conflict_files))
    same_files = get_same_files(anti_result, conflict_result)
    print(len(same_files))
