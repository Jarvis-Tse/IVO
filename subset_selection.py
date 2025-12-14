#!/usr/bin/env python3
import json
import sys
from collections import defaultdict, deque

def filter_descendants(graph, root_id):
    """Return subgraph with root_id and all its descendants (following obj→sub)."""
    edges = graph.get("edges", [])
    nodes = graph.get("nodes", [])

    # Build adjacency list: parent (obj) -> list of children (sub)
    children = defaultdict(list)
    for e in edges:
        parent = e.get("obj")
        child = e.get("sub")
        if parent and child:
            children[parent].append(child)

    # BFS to find all descendants of root
    reachable = set()
    queue = deque([root_id])
    while queue:
        node = queue.popleft()
        if node in reachable:
            continue
        reachable.add(node)
        queue.extend(children[node])

    # Filter nodes and edges
    filtered_nodes = [n for n in nodes if n.get("id") in reachable]
    filtered_edges = [
        e for e in edges
        if e.get("sub") in reachable and e.get("obj") in reachable
    ]

    return {"nodes": filtered_nodes, "edges": filtered_edges}


def main(input_file, output_file, root_id):
    # Load JSON
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Expect structure like {"graphs": [ {...} ]}
    graph = data["graphs"][0]
    filtered_graph = filter_descendants(graph, root_id)

    # Replace and write output
    data["graphs"][0] = filtered_graph
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Filtered graph written to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python subset_selection.py input.json output.json root_node_id")
        sys.exit(1)

    # root_id should be in double quotations
    input_file, output_file, root_id = sys.argv[1], sys.argv[2], sys.argv[3]
    main(input_file, output_file, root_id)
