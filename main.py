# disk_access_model/main.py
import os
from sorter import external_sort
from tree_builder import build_tree, save_tree
from query import query_tree
from visualizer import visualize_points, visualize_tree

# Ayarlar
INPUT_FILE = 'data/file.csv'
SORTED_FILE = 'data/sorted_points.csv'
TREE_FILE = 'data/tree_structure.json'
OUTPUT_DIR = 'data/partitions'
RESULT_FILE = 'data/query_result.csv'
MEMORY_LIMIT = 10 * 1024 * 1024  # 10 MB

# Bounding box sorgu araligi (ornek)
BBOX = {
    'xmin': 394373.0,
    'xmax': 394375.0,
    'ymin': 39305.7,
    'ymax': 39306.0
}

if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("[1/4] External sorting started...")
    external_sort(INPUT_FILE, SORTED_FILE, MEMORY_LIMIT, sort_by=0)  # X koordinatina gore sirala

    print("[2/4] Building binary tree...")
    tree = build_tree(SORTED_FILE, OUTPUT_DIR, MEMORY_LIMIT, depth=0)
    save_tree(tree, TREE_FILE)

    print("[3/4] Querying tree...")
    results = query_tree(tree, BBOX)

    print(f"[4/4] Visualizing {len(results)} points...")
    visualize_points(results)
    visualize_tree(tree)
