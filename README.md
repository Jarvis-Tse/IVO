To use IVO, first download HPO release from here: https://github.com/obophenotype/human-phenotype-ontology/releases.

Included downloaded scripts: hp-base-2025-Oct.json & hp-base-2025-Aug.json.

-------------------------------------------------------------------------------------------------------

Then, run subset_selection.py to filter the downloaded JSON file based on root node by following instruction:

Usage: python subset_selection.py input.json output.json root_node_id

-------------------------------------------------------------------------------------------------------

Next, rename output.json to root_node_name.json. Example filtered JSON file: Abnormality of the skeletal system.json.

Then, open IVO.qmd with RStudio, change the variable "root_item_name" to the name of the name of the root node. Then, run all cells in the file. The interactive visulization will then appear.

-------------------------------------------------------------------------------------------------------

**Below are the instructions for reproducing the results for numeric evaluation (i.e. by checking how many nodes between the HPO releases can be flagged using the two computational methods)**

-------------------------------------------------------------------------------------------------------

2.compare_jsons.py

Usage: python compare_jsons.py <file1.json> <file2.json>
The two JSON files should be two HPO subsets

Example outputs: only_in_hp-base-2025-Aug-Abnormality of the skeletal system.txt; only_in_hp-base-2025-Oct-Abnormality of the skeletal system.txt

-------------------------------------------------------------------------------------------------------

3.summarize_subset.py

Usage: change the two commented variables, which correspond to the input and output files, respectively, to convert the JSON file that represents the HPO subset of the OLDER ontology being compared into the statistics for each node

Example output: hpo_2025-Aug-hierarchy.csv

-------------------------------------------------------------------------------------------------------
4.find_parents.py

Usage: change the three commented variables to merge the NEWER ontology's JSON file and only-existing terms to output all parents/siblings of these terms in the NEWER ontology

Example output: parent_output-2025-Oct.csv

-------------------------------------------------------------------------------------------------------
5.old_parent_analysis.py

Usage: change three variables to check if the parents in the NEWER ontology exist in the OLDER hierarchy, the outputted file is a .csv file

Example output: node_parent_analysis.csv

-------------------------------------------------------------------------------------------------------

6.calculate_avg.py

Usage: change the two commented variables to read in the hierarchy csv file from 3.summarize_subset.py then analyze the data by depth

Example output: statistics_by_depth.csv
