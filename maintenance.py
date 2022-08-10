import json
import this
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List
import csv
import git
from pathlib import Path
from pydriller import Repository, ModifiedFile, Git
from pydriller.metrics.process.change_set import ChangeSet
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.contributors_count import ContributorsCount
from pydriller.metrics.process.contributors_experience import ContributorsExperience
from pydriller.metrics.process.hunks_count import HunksCount
from pydriller.metrics.process.lines_count import LinesCount


@dataclass
class FileMetric:
    total_code_churn: int
    max_code_churn: int
    average_code_churn: int
    commits: int
    contributors: int
    minor_contributors_num: int
    highest_contributors_percentage: bool
    median_number_of_hunk: bool
    total_added_line: int
    max_added_line: int
    average_added_line: int
    total_removed_line: int
    max_removed_line: int
    average_removed_line: int

    def __init__(self):
        self.total_code_churn = 0
        self.max_code_churn = 0
        self.average_code_churn = 0
        self.commits = 0
        self.contributors = 0
        self.minor_contributors_num = 0
        self.highest_contributors_percentage = 0
        self.median_number_of_hunk = 0
        self.total_added_line = 0
        self.max_added_line = 0
        self.average_added_line = 0
        self.total_removed_line = 0
        self.max_removed_line = 0
        self.average_removed_line = 0


def test_commit(local_path, start_commit_id, end_commit_id):
    # for commit in Repository(local_path, from_commit=start_commit_id, to_commit=end_commit_id).traverse_commits():
    for commit in Repository(local_path).traverse_commits():
        for modifiedFile in commit.modified_files:
            print(modifiedFile.old_path)
            print(modifiedFile.new_path)
            print(modifiedFile.added_lines)
            print(modifiedFile.deleted_lines)
            print(modifiedFile.nloc)
        print(commit.hash)
        print(commit.merge)
        print(commit.files)


def test_metrics(local_path, start_commit_id, end_commit_id):
    metric = ChangeSet(path_to_repo=local_path, from_commit=start_commit_id, to_commit=end_commit_id)
    maximum = metric.max()
    average = metric.avg()
    print('Maximum number of files committed together: {}'.format(maximum))
    print('Average number of files committed together: {}'.format(average))
    data = defaultdict(FileMetric)
    metric = CodeChurn(path_to_repo=local_path, from_commit=start_commit_id, to_commit=end_commit_id)
    files_count = metric.count()
    files_max = metric.max()
    files_avg = metric.avg()
    for file, count in dict(files_count).items():
        file_metric = FileMetric()
        file_metric.total_code_churn = count
        data[file] = file_metric
    for file, count in dict(files_max).items():
        data[file].__setattr__('max_code_churn', count)
    for file, count in dict(files_avg).items():
        data[file].__setattr__('average_code_churn', count)
    metric = CommitsCount(path_to_repo=local_path, from_commit=start_commit_id, to_commit=end_commit_id)
    files = metric.count()
    for file, count in dict(files).items():
        data[file].__setattr__('commits', count)
    metric = ContributorsCount(path_to_repo=local_path, from_commit=start_commit_id, to_commit=end_commit_id)
    count = metric.count()
    minor = metric.count_minor()
    for file, num in dict(count).items():
        data[file].__setattr__('contributors', num)
    for file, num in dict(minor).items():
        data[file].__setattr__('minor_contributors_num', num)
    metric = ContributorsExperience(path_to_repo=local_path, from_commit=start_commit_id, to_commit=end_commit_id)
    files = metric.count()
    for file, num in dict(files).items():
        data[file].__setattr__('highest_contributors_percentage', num)
    metric = HunksCount(path_to_repo=local_path, from_commit=start_commit_id, to_commit=end_commit_id)
    files = metric.count()
    for file, num in dict(files).items():
        data[file].__setattr__('median_number_of_hunk', num)
    metric = LinesCount(path_to_repo=local_path, from_commit=start_commit_id, to_commit=end_commit_id)
    added_count = metric.count_added()
    added_max = metric.max_added()
    added_avg = metric.avg_added()
    for file, num in dict(added_count).items():
        data[file].__setattr__('total_added_line', num)
    for file, num in dict(added_max).items():
        data[file].__setattr__('max_added_line', num)
    for file, num in dict(added_avg).items():
        data[file].__setattr__('average_added_line', num)
    removed_count = metric.count_removed()
    removed_max = metric.max_removed()
    removed_avg = metric.avg_removed()
    for file, num in dict(removed_count).items():
        data[file].__setattr__('total_removed_line', num)
    for file, num in dict(removed_max).items():
        data[file].__setattr__('max_removed_line', num)
    for file, num in dict(removed_avg).items():
        data[file].__setattr__('average_removed_line', num)
    return data


def dump_metric_dict(metric_dict: dict[str, FileMetric], file_name: str):
    title = 'file | total_code_churn | max_code_churn | average_code_churn | commits | contributors_num | ' \
            'minor_contributors_num | highest_contributors_percentage | median_number_of_hunk | total_added_line | ' \
            'max_added_line | average_added_line | total_removed_line | max_removed_line | average_removed_line'
    title_head = title.split('|')
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(title_head)
        for file_path, metric in metric_dict.items():
            if file_path.endswith(".java"):
                writer.writerow([file_path, metric.total_code_churn, metric.max_code_churn, metric.average_code_churn,
                                 metric.commits, metric.contributors, metric.minor_contributors_num,
                                 metric.highest_contributors_percentage, metric.median_number_of_hunk,
                                 metric.total_added_line, metric.max_added_line, metric.average_added_line,
                                 metric.total_removed_line, metric.max_removed_line, metric.average_removed_line])

# def get_depo(local_path) -> dict[str, list[str]]:
#     current = Git(local_path)
#     ret = defaultdict(list)
#     for file in current.files():
#
#     return ret


def test_merge(repo: Git.repo):
    tags = repo.branches
    for tag in tags:
        print(tag)
    repo.index.merge_tree("android10", "android12L")
    unmerged_blobs = repo.index.unmerged_blobs()
    for path in unmerged_blobs:
        list_of_blobs = unmerged_blobs[path]
        for (stage, blob) in list_of_blobs:
            print(blob)
            print(stage)
    # repo.merge_base()


if __name__ == '__main__':
    repo_path = "E:\\PycharmProjects\\DataExtraction\\CustomizedAndroid\\platforms\\lineage\\base"
    end_commit = 'a6ec214469cb8ad26bc948bc0b60006ffd1fdf5b'
    start_commit = '54b6cfa9a9e5b861a9930af873580d6dc20f773c'
    # test_commit(repo_path, start_commit, end_commit)
    dump_metric_dict(test_metrics(repo_path, start_commit, end_commit), "conflicts/lineage-17.1-metrics.csv")
    # get_depo(repo_path)
    # test_merge(git.Repo(repo_path))

    # g = git.cmd.Git(repo_path)
