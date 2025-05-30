# disk_access_model/tree_builder.py
import csv
import os
import json
import tempfile
from sorter import external_sort, get_file_size

class TreeNode:
    def __init__(self, axis=None, median=None, left=None, right=None, file=None):
        self.axis = axis  # 0 for X, 1 for Y
        self.median = median
        self.left = left
        self.right = right
        self.file = file  # only for leaf nodes

    def to_dict(self):
        return {
            'axis': self.axis,
            'median': self.median,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None,
            'file': self.file
        }

    @staticmethod
    def from_dict(data):
        if data is None:
            return None
        node = TreeNode(
            axis=data['axis'],
            median=data['median'],
            file=data['file']
        )
        node.left = TreeNode.from_dict(data['left'])
        node.right = TreeNode.from_dict(data['right'])
        return node

def count_lines(file_path):
    with open(file_path, 'r') as f:
        return sum(1 for _ in f) - 1  # exclude header

def get_median_from_sorted(file_path, axis):
    num_lines = count_lines(file_path)
    median_index = num_lines // 2
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for i, row in enumerate(reader):
            if i == median_index:
                return float(row[axis])

def split_by_median(file_path, axis, median, output_dir):
    left_file = os.path.join(output_dir, next(tempfile._get_candidate_names()) + '.csv')
    right_file = os.path.join(output_dir, next(tempfile._get_candidate_names()) + '.csv')
    with open(file_path, 'r') as infile, \
         open(left_file, 'w', newline='') as left_out, \
         open(right_file, 'w', newline='') as right_out:

        reader = csv.reader(infile)
        left_writer = csv.writer(left_out)
        right_writer = csv.writer(right_out)
        header = next(reader)
        left_writer.writerow(header)
        right_writer.writerow(header)

        for row in reader:
            val = float(row[axis])
            if val < median:
                left_writer.writerow(row)
            else:
                right_writer.writerow(row)

    return left_file, right_file

def build_tree(file_path, output_dir, memory_limit, depth):
    if get_file_size(file_path) <= memory_limit:
        return TreeNode(file=file_path)

    axis = depth % 2
    sorted_file = os.path.join(output_dir, next(tempfile._get_candidate_names()) + '_sorted.csv')
    external_sort(file_path, sorted_file, memory_limit, sort_by=axis)
    median = get_median_from_sorted(sorted_file, axis)
    left_file, right_file = split_by_median(sorted_file, axis, median, output_dir)
    left = build_tree(left_file, output_dir, memory_limit, depth + 1)
    right = build_tree(right_file, output_dir, memory_limit, depth + 1)

    return TreeNode(axis=axis, median=median, left=left, right=right)

def save_tree(tree, filename):
    with open(filename, 'w') as f:
        json.dump(tree.to_dict(), f, indent=2)

def load_tree(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        return TreeNode.from_dict(data)