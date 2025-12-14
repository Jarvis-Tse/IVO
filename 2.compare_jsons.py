import json
import sys
import os

def load_json_file(filepath):
    """Load and parse a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filepath}': {e}")
        sys.exit(1)

def extract_nodes(data):
    """Extract all nodes (ID and label) from the JSON structure."""
    nodes = {}

    # Navigate through the 'graphs' array
    if 'graphs' in data:
        for graph in data['graphs']:
            if 'nodes' in graph:
                for node in graph['nodes']:
                    if 'id' in node:
                        node_id = node['id']
                        node_label = node.get('lbl', 'N/A')
                        nodes[node_id] = node_label

    return nodes

def save_ids_to_file(ids, labels, output_path):
    """Save IDs as comma-separated list to a text file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write comma-separated IDs
            id_list = sorted(ids)
            f.write(','.join(id_list))
        print(f"  Saved to: {output_path}")
    except Exception as e:
        print(f"  Error saving file '{output_path}': {e}")

def compare_json_files(file1_path, file2_path):
    """Compare two JSON files and find unique nodes."""
    print(f"Loading {file1_path}...")
    data1 = load_json_file(file1_path)

    print(f"Loading {file2_path}...")
    data2 = load_json_file(file2_path)

    # Extract nodes from both files
    nodes_file1 = extract_nodes(data1)
    nodes_file2 = extract_nodes(data2)

    # Find unique IDs
    ids_file1 = set(nodes_file1.keys())
    ids_file2 = set(nodes_file2.keys())

    only_in_file1 = ids_file1 - ids_file2
    only_in_file2 = ids_file2 - ids_file1
    common_ids = ids_file1 & ids_file2

    # Get script directory and base names for output files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file1_base = os.path.splitext(os.path.basename(file1_path))[0]
    file2_base = os.path.splitext(os.path.basename(file2_path))[0]

    # Print results
    print("\n" + "="*80)
    print("COMPARISON RESULTS")
    print("="*80)

    print(f"\nTotal nodes in {file1_path}: {len(ids_file1)}")
    print(f"Total nodes in {file2_path}: {len(ids_file2)}")
    print(f"Common nodes in both files: {len(common_ids)}")

    print(f"\n{'='*80}")
    print(f"Nodes ONLY in {file1_path}: {len(only_in_file1)}")
    print(f"{'='*80}")
    if only_in_file1:
        for node_id in sorted(only_in_file1):
            label = nodes_file1[node_id]
            print(f"  ID:  {node_id}")
            print(f"  Lbl: {label}")
            print()
        # Save to file in script directory
        output_file = os.path.join(script_dir, f"only_in_{file1_base}.txt")
        save_ids_to_file(only_in_file1, nodes_file1, output_file)
    else:
        print("  (none)")

    print(f"\n{'='*80}")
    print(f"Nodes ONLY in {file2_path}: {len(only_in_file2)}")
    print(f"{'='*80}")
    if only_in_file2:
        for node_id in sorted(only_in_file2):
            label = nodes_file2[node_id]
            print(f"  ID:  {node_id}")
            print(f"  Lbl: {label}")
            print()
        # Save to file in script directory
        output_file = os.path.join(script_dir, f"only_in_{file2_base}.txt")
        save_ids_to_file(only_in_file2, nodes_file2, output_file)
    else:
        print("  (none)")

    return only_in_file1, only_in_file2

def main():
    """Main function to run the comparison."""
    if len(sys.argv) != 3:
        print("Usage: python compare_jsons.py <file1.json> <file2.json>")
        print("\nExample:")
        print("  python compare_jsons.py ontology1.json ontology2.json")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]

    compare_json_files(file1_path, file2_path)

if __name__ == "__main__":
    main()
