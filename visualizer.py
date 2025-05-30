# disk_access_model/visualizer.py
import matplotlib.pyplot as plt
from tree_builder import TreeNode

def visualize_points(points):
    if not points:
        print("No points to display.")
        return

    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    colors = [p[2] for p in points]  # Assume Z is some value to color

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(x_vals, y_vals, c=colors, cmap='viridis', s=10)
    plt.colorbar(scatter, label='Z value')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Query Result Point Cloud')
    plt.grid(True)
    plt.show()

def visualize_tree(node, bounds=None, depth=0, ax=None):
    if node is None:
        return

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        bounds = {
            'xmin': 394372.0, 'xmax': 394376.0,
            'ymin': 39305.6, 'ymax': 39306.1
        }

    axis = node.axis
    median = node.median

    if axis == 0:
        ax.plot([median, median], [bounds['ymin'], bounds['ymax']], color='red', linestyle='--')
        left_bounds = bounds.copy()
        left_bounds['xmax'] = median
        right_bounds = bounds.copy()
        right_bounds['xmin'] = median
    elif axis == 1:
        ax.plot([bounds['xmin'], bounds['xmax']], [median, median], color='blue', linestyle='--')
        left_bounds = bounds.copy()
        left_bounds['ymax'] = median
        right_bounds = bounds.copy()
        right_bounds['ymin'] = median
    else:
        return

    if node.left:
        visualize_tree(node.left, left_bounds, depth + 1, ax)
    if node.right:
        visualize_tree(node.right, right_bounds, depth + 1, ax)

    if depth == 0:
        ax.set_xlim(bounds['xmin'], bounds['xmax'])
        ax.set_ylim(bounds['ymin'], bounds['ymax'])
        ax.set_title("Binary Tree Partition Visualization")
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.show()