import csv

# Read the NEW hierarchy (with parent relationships)
print("Reading new hierarchy CSV...")
new_nodes = []
with open(r'/Users/wonton-eater/Desktop/Work/Fall 2025/Symbolic AI in Health/final_project/prototype/parent_output-2025-Oct.csv', 'r') as f: # change 1
    reader = csv.DictReader(f)
    for row in reader:
        new_nodes.append(row)
print(f"Loaded {len(new_nodes)} nodes from new hierarchy")

# Read the OLD hierarchy (with Num_Children and Max_Num_Descendant_Diffscendant_Diff)
print("Reading old hierarchy CSV...")
old_file = r'/Users/wonton-eater/Desktop/Work/Fall 2025/Symbolic AI in Health/final_project/prototype/hpo_2025-Aug-hierarchy.csv' # change 2
old_nodes = []
with open(old_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        old_nodes.append(row)
print(f"Loaded {len(old_nodes)} nodes from old hierarchy")
print()

# Create a dictionary for old hierarchy info
old_node_info = {}
for node in old_nodes:
    node_id = node['ID']
    old_node_info[node_id] = {
        'Num_Children': int(node['Num_Children']) if node['Num_Children'] else 0,
        'Max_Num_Descendant_Diffscendant_Diff': int(node['Max_Num_Descendant_Diff']) if node['Max_Num_Descendant_Diff'] else 0,
        'Depth': int(node['Depth'])
    }

# Process each node in the NEW hierarchy
results = []
for node in new_nodes:
    node_id = node['node_id']
    node_label = node['node_label']
    num_parents = int(node['num_parents']) if node['num_parents'] else 0

    parent_max_desc_diff = None
    parent_ids_found = []  # NEW: Store parent IDs
    parent_children_counts = []  # Store children counts for each parent
    parent_children_count = None
    parent_depth = None

    if num_parents > 0 and node.get('parent_ids'):
        # Parse parent IDs
        parent_ids_str = node['parent_ids']
        # Handle both comma and space separation
        parent_ids_str = parent_ids_str.replace(' ', ',')
        parent_ids = [p.strip() for p in parent_ids_str.split(';') if p.strip()]

        qualifying_parent_diffs = []

        for parent_id in parent_ids:
            # Check if this parent exists in the OLD hierarchy
            if parent_id in old_node_info:
                parent_ids_found.append(parent_id)  # NEW: Collect parent IDs
                parent_depth = old_node_info[parent_id]['Depth']
                old_node_info[parent_id]['Max_Num_Descendant_Diffscendant_Diff']
                qualifying_parent_diffs.append(
                    old_node_info[parent_id]['Max_Num_Descendant_Diffscendant_Diff']
                )
                parent_children_counts.append(
                    old_node_info[parent_id]['Num_Children']
                )


        # Get the maximum if we found any qualifying parents
        if qualifying_parent_diffs:
            parent_max_desc_diff = max(qualifying_parent_diffs)
        if(len(parent_children_counts)>0):
            parent_children_count = min(parent_children_counts)


    results.append({
        'Node_ID': node_id,
        'Node_Label': node_label,
        #'Num_Parents': num_parents,
        'Parent_IDs': ','.join(parent_ids_found) if parent_ids_found else '',  # NEW
        'Parent_Children_Count (min)': parent_children_count,
        'Parent_Max_Desc_Diff': parent_max_desc_diff if parent_max_desc_diff is not None else '',
        'Parent_Depth': parent_depth if parent_depth is not None else ''
    })

# Write results to CSV
with open(r'/Users/wonton-eater/Desktop/Work/Fall 2025/Symbolic AI in Health/final_project/prototype/node_parent_analysis.csv', 'w', newline='') as f: # change 3
    fieldnames = ['Node_ID', 'Node_Label', 'Parent_IDs', 'Parent_Children_Count (min)', 'Parent_Max_Desc_Diff','Parent_Depth'] 
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("\nAnalysis complete. Results saved to 'node_parent_analysis.csv'")
print(f"Total nodes analyzed: {len(results)}")

# Count nodes with qualifying parents
nodes_with_parents = sum(1 for r in results if r['Parent_Max_Desc_Diff'] != '')
print(f"Nodes with qualifying parents (parent had 0 or 1 children in old hierarchy): {nodes_with_parents}")
