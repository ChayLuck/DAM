# disk_access_model/query.py
import csv
from tree_builder import TreeNode

def point_in_bbox(point, bbox):
    x, y = float(point[0]), float(point[1])
    return bbox['xmin'] <= x <= bbox['xmax'] and bbox['ymin'] <= y <= bbox['ymax']

def query_tree(node, bbox):
    if node is None:
        return []

    # Leaf node: load points and filter
    if node.file:
        results = []
        with open(node.file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                if point_in_bbox(row, bbox):
                    results.append((float(row[0]), float(row[1]), float(row[2])))
        return results

    axis = node.axis
    median = node.median
    results = []

    if axis == 0:  # X-axis
        if bbox['xmin'] < median:
            results.extend(query_tree(node.left, bbox))
        if bbox['xmax'] >= median:
            results.extend(query_tree(node.right, bbox))
    elif axis == 1:  # Y-axis
        if bbox['ymin'] < median:
            results.extend(query_tree(node.left, bbox))
        if bbox['ymax'] >= median:
            results.extend(query_tree(node.right, bbox))

    return results