import json
import csv
from collections import defaultdict

def load_hierarchy(json_file):
    """Load the HP ontology hierarchy from JSON file."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

def load_node_list(txt_file):
    """Load the list of node IDs from text file."""
    with open(txt_file, 'r') as f:
        content = f.read().strip()
    # Split by comma and strip whitespace
    nodes = [node.strip() for node in content.split(',')]
    return nodes

def build_parent_child_maps(edges):
    """Build mappings of parents to children and children to parents."""
    child_to_parents = defaultdict(list)
    parent_to_children = defaultdict(list)

    for edge in edges:
        if edge.get('pred') == 'is_a':
            child = edge.get('sub')
            parent = edge.get('obj')
            if child and parent:
                child_to_parents[child].append(parent)
                parent_to_children[parent].append(child)

    return child_to_parents, parent_to_children

def get_node_label(node_id, nodes):
    """Get the label for a node ID."""
    for node in nodes:
        if node.get('id') == node_id:
            return node.get('lbl', '')
    return ''

def find_siblings(node_id, child_to_parents, parent_to_children):
    """Find all siblings of a node (nodes sharing the same parent)."""
    siblings = set()
    parents = child_to_parents.get(node_id, [])

    for parent in parents:
        # Get all children of this parent
        children = parent_to_children.get(parent, [])
        # Add all children except the node itself
        for child in children:
            if child != node_id:
                siblings.add(child)

    return list(siblings)

def main():
    # File paths - adjust these as needed
    hierarchy_file = r'/Users/wonton-eater/Desktop/Work/Fall 2025/Symbolic AI in Health/final_project/prototype/hp-base-2025-Oct-Phenotypic abnormality.json' # change 1
    node_list_file = r'/Users/wonton-eater/Desktop/Work/Fall 2025/Symbolic AI in Health/final_project/prototype/only_in_hp-base-2025-Oct-Phenotypic abnormality.txt' # change 2
    output_file = r'/Users/wonton-eater/Desktop/Work/Fall 2025/Symbolic AI in Health/final_project/prototype/parent_output.csv' # change 3

    print("Loading hierarchy...")
    hierarchy_data = load_hierarchy(hierarchy_file)

    print("Loading node list...")
    target_nodes = load_node_list(node_list_file)

    # Extract nodes and edges from the hierarchy
    graph = hierarchy_data['graphs'][0]
    nodes = graph['nodes']
    edges = graph['edges']

    print(f"Building parent-child relationships from {len(edges)} edges...")
    child_to_parents, parent_to_children = build_parent_child_maps(edges)

    # Prepare output data
    output_data = []

    print(f"Processing {len(target_nodes)} nodes...")
    for node_id in target_nodes:
        print(node_id)
        node_label = get_node_label(node_id, nodes)
        parents = child_to_parents.get(node_id, [])
        siblings = find_siblings(node_id, child_to_parents, parent_to_children)
        print(parents)

        # Get labels for parents and siblings
        parent_labels = [get_node_label(p, nodes) for p in parents]
        sibling_labels = [get_node_label(s, nodes) for s in siblings]

        output_data.append({
            'node_id': node_id,
            'node_label': node_label,
            'parent_ids': '; '.join(parents),
            'parent_labels': '; '.join(parent_labels),
            'sibling_ids': '; '.join(siblings),
            'sibling_labels': '; '.join(sibling_labels),
            'num_parents': len(parents),
            'num_siblings': len(siblings)
        })

    # Write to CSV
    print(f"Writing results to {output_file}...")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['node_id', 'node_label', 'parent_ids', 'parent_labels',
                      'sibling_ids', 'sibling_labels', 'num_parents', 'num_siblings']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(output_data)

    print(f"Done! Processed {len(output_data)} nodes.")
    print(f"Output saved to {output_file}")

if __name__ == '__main__':
    main()
