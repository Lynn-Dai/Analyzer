import csv

from pydriller import Repository, ModifiedFile, Git
import pandas as pd
import json

# url = "https://github.com/LineageOS/android_frameworks_base"
url = '/Users/pingguo/PycharmProjects/android_frameworks_base'
commits = []
modified_files = []


def traverse(from_commit, to_commit):
    for commit in Repository(url, from_commit=from_commit, to_commit=to_commit).traverse_commits():
        print(
            'The commit {} has been modified by {}, '
            'committed by {} in date {}'.format(
                commit.hash,
                commit.author.name,
                commit.committer.name,
                commit.committer_date
            )
        )
        commit_record = {
            'hash': commit.hash,
            'commit': commit.msg,
            'date': str(commit.committer_date)
        }
        commits.append(commit_record)
        for file in commit.modified_files:
            if '.java' in file.filename:
                print('file: ' + file.filename)
                # Capture information about the commit in object format so I can reference it later
                meths = []
                for meth in file.changed_methods:
                    meths.append(meth.name)
                modified_file = {
                    'hash': commit.hash,
                    'filename': file.filename,
                    'diff': file.diff,
                    'added_lines': file.added_lines,
                    'deleted_lines': file.deleted_lines,
                    'changed_methods': ', '.join(meths),
                }
                modified_files.append(modified_file)
    df_commits = pd.DataFrame(commits)
    df_commits.to_excel('./change_code/lineage-17.1-commits.xlsx', engine='xlsxwriter')
    df_modified_files = pd.DataFrame(modified_files)
    df_modified_files.to_excel('./change_code/lineage-17.1-modified-files.xlsx', engine='xlsxwriter')

    # with open("./change_code/lineage-19.1.json", 'w') as FOUT:
    #     js = json.dumps(modified, indent=True)
    #     FOUT.write(js)

    # with open('./change_code/lineage-19.1.json', 'w', newline='') as f:
    #     writer = csv.DictWriter(f, fieldnames=modified.keys())
    #     writer.writeheader()
    #     writer.writerow(modified)


if __name__ == '__main__':
    traverse('8943bbe92bfbc3ead44f63a6a3c145a135548b7c', 'a6e614646103d3c8aca5a28b46a8adde1996af5c')
