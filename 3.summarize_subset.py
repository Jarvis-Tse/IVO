import json
import os
from collections import defaultdict, deque

# File path variable - update this to your actual file location
JSON_FILEPATH = r'/Users/wonton-eater/Desktop/Work/Fall 2025/Symbolic AI in Health/final_project/prototype/hp-base-2025-Aug-Phenotypic abnormality.json' # change 1

def analyze_hpo_hierarchy():
    """
    Analyze HPO ontology structure from JSON file.

    Returns:
        List of dictionaries containing node hierarchy information including depth
    """
    # Check if file exists
    if not os.path.exists(JSON_FILEPATH):
        raise FileNotFoundError(f"File not found: {JSON_FILEPATH}")

    # Load data from file
    print(f"Loading data from: {JSON_FILEPATH}")
    with open(JSON_FILEPATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract nodes and edges
    graph = data['graphs'][0]
    nodes = {node['id']: node.get('lbl', 'Unknown') for node in graph['nodes']}
    edges = graph['edges']

    print(f"Loaded {len(nodes)} nodes and {len(edges)} edges")

    # Build parent-child relationships
    children = defaultdict(list)  # parent -> [children]
    parents = defaultdict(list)   # child -> [parents]

    for edge in edges:
        if edge['pred'] == 'is_a':
            child_id = edge['sub']
            parent_id = edge['obj']
            children[parent_id].append(child_id)
            parents[child_id].append(parent_id)

    # Identify root nodes (nodes with no parents)
    root_nodes = [node_id for node_id in nodes if not parents[node_id]]
    print(f"Found {len(root_nodes)} root node(s): {root_nodes}")

    # Calculate depth for each node using BFS
    depths = {}
    queue = deque()

    # Initialize with root nodes at depth 0
    for root in root_nodes:
        depths[root] = 0
        queue.append(root)

    # BFS to calculate depths
    while queue:
        current_node = queue.popleft()
        current_depth = depths[current_node]

        for child in children[current_node]:
            # If child hasn't been visited, or we found a shorter path
            if child not in depths or depths[child] > current_depth + 1:
                depths[child] = current_depth + 1
                queue.append(child)

    # Calculate descendants recursively
    def count_descendants(node_id, visited=None):
        if visited is None:
            visited = set()

        if node_id in visited:
            return 0

        visited.add(node_id)
        count = 0

        for child in children[node_id]:
            count += 1  # Count the child
            count += count_descendants(child, visited)  # Count child's descendants

        return count

    # Calculate descendants for all nodes first
    descendants_count = {}
    for node_id in nodes:
        descendants_count[node_id] = count_descendants(node_id)

    # Prepare results
    results = []
    for node_id in nodes:
        node_parents = parents.get(node_id, [])
        node_children = children.get(node_id, [])
        num_descendants = descendants_count[node_id]
        node_depth = depths.get(node_id, -1)  # -1 if unreachable from root

        # Calculate Max_Num_Descendant_Diff
        max_descendant_diff = 0
        if node_parents:
            # Get all siblings across all parents
            all_siblings = set()
            for parent_id in node_parents:
                # Add all children of this parent (including the node itself)
                all_siblings.update(children.get(parent_id, []))

            # Remove the node itself from siblings
            all_siblings.discard(node_id)

            # Find the maximum number of descendants among siblings
            if all_siblings:
                max_sibling_descendants = max(descendants_count.get(sibling, 0) for sibling in all_siblings)
                max_descendant_diff = max(0, max_sibling_descendants - num_descendants)

        results.append({
            'id': node_id,
            'label': nodes[node_id],
            'depth': node_depth,
            'parents': [{'id': p, 'label': nodes.get(p, 'Unknown')} for p in node_parents],
            'children': [{'id': c, 'label': nodes.get(c, 'Unknown')} for c in node_children],
            'num_children': len(node_children),
            'num_descendants': num_descendants,
            'max_descendant_diff': max_descendant_diff
        })

    # Sort by depth first, then by ID
    results.sort(key=lambda x: (x['depth'], x['id']))

    return results

def print_results(results):
    """Print results in a readable format."""
    for node in results:
        print(f"\n{'='*80}")
        print(f"ID: {node['id']}")
        print(f"Label: {node['label']}")
        print(f"Depth: {node['depth']}")
        print(f"\nParents ({len(node['parents'])}):")
        if node['parents']:
            for p in node['parents']:
                print(f"  - {p['id']}")
                print(f"    {p['label']}")
        else:
            print("  None (root node)")

        print(f"\nChildren ({node['num_children']}):")
        if node['children']:
            for c in node['children']:
                print(f"  - {c['id']}")
                print(f"    {c['label']}")
        else:
            print("  None (leaf node)")

        print(f"\nTotal Descendants: {node['num_descendants']}")

# Main execution
if __name__ == "__main__":
    try:
        # Analyze the hierarchy
        results = analyze_hpo_hierarchy()

        print("\nHPO HIERARCHY ANALYSIS")
        print("="*80)
        print(f"Total nodes analyzed: {len(results)}")

        # Print depth statistics
        depths = [node['depth'] for node in results]
        print(f"Maximum depth: {max(depths)}")
        print(f"Minimum depth: {min(depths)}")

        # Count nodes at each depth
        from collections import Counter
        depth_counts = Counter(depths)
        print(f"\nNodes per depth level:")
        for depth in sorted(depth_counts.keys()):
            print(f"  Depth {depth}: {depth_counts[depth]} nodes")

        # Export to CSV
        import csv
        output_csv = '/Users/wonton-eater/Desktop/Work/Fall 2025/Symbolic AI in Health/final_project/prototype/hpo_hierarchy.csv' # change 2
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Label', 'Depth', 'Num_Parents', 'Num_Children', 'Num_Descendants', 'Max_Num_Descendant_Diff'])
            for node in results:
                parents = node['parents']
                writer.writerow([
                    node['id'],
                    node['label'],
                    node['depth'],
                    len(node['parents']),
                    node['num_children'],
                    node['num_descendants'],
                    node['max_descendant_diff']
                ])

        print(f"\nResults exported to '{output_csv}'")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please update the JSON_FILEPATH variable with the correct path.")
    except KeyError as e:
        print(f"Error: Invalid JSON structure. Missing key: {e}")
        print("Make sure the JSON file has 'graphs' containing 'nodes' and 'edges'.")
    except Exception as e:
        print(f"An error occurred: {e}")
