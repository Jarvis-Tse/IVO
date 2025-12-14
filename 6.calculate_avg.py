import csv
from collections import defaultdict
import statistics

# Read the CSV file
def read_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data

# Group data by depth
def group_by_depth(data):
    grouped = defaultdict(list)
    for row in data:
        depth = int(row['Depth'])
        grouped[depth].append(row)
    return grouped

# Calculate statistics for a list of values
def calc_stats(values):
    if not values:
        return None, None, None, None

    values = [float(v) for v in values if v]  # Convert to float and filter empty

    if not values:
        return None, None, None, None

    return {
        'min': min(values),
        'max': max(values),
        'mean': statistics.mean(values),
        'median': statistics.median(values)
    }

# Main processing
filename = '/Users/wonton-eater/Desktop/Work/Fall 2025/Symbolic AI in Health/final_project/prototype/hpo_2025-Aug-hierarchy.csv' # change 1
data = read_csv(filename)
grouped_data = group_by_depth(data)

# Columns to analyze
columns = ['Num_Descendants', 'Max_Num_Descendant_Diff', 'Num_Children', 'Num_Parents']

# Calculate and display statistics
print("Statistics grouped by Depth:")
print("=" * 100)

results = []

for depth in sorted(grouped_data.keys()):
    print(f"\nDepth: {depth}")
    print("-" * 100)

    depth_rows = grouped_data[depth]
    num_nodes = len(depth_rows)
    result = {'Depth': depth, 'Num_Nodes': num_nodes}

    print(f"Number of Nodes: {num_nodes}")

    for col in columns:
        values = [row[col] for row in depth_rows if row.get(col)]
        stats = calc_stats(values)

        if stats:
            result[f'{col}_min'] = stats['min']
            result[f'{col}_max'] = stats['max']
            result[f'{col}_mean'] = stats['mean']
            result[f'{col}_median'] = stats['median']

            print(f"\n{col}:")
            print(f"  Min:    {stats['min']:.2f}")
            print(f"  Max:    {stats['max']:.2f}")
            print(f"  Mean:   {stats['mean']:.2f}")
            print(f"  Median: {stats['median']:.2f}")

    results.append(result)

# Save results to CSV
output_filename = '/Users/wonton-eater/Desktop/Work/Fall 2025/Symbolic AI in Health/final_project/prototype/statistics_by_depth.csv' # change 2
if results:
    with open(output_filename, 'w', newline='') as f:
        fieldnames = ['Depth', 'Num_Nodes']
        for col in columns:
            fieldnames.extend([f'{col}_min', f'{col}_max', f'{col}_mean', f'{col}_median'])

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("\n" + "=" * 100)
    print(f"Results saved to '{output_filename}'")
