import csv, json
graph = []
with open('blah.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        graph.append(row)
json_graph = []
for row in graph:
	json_graph_row = {}
	json_graph_row['nodeFrom'] = row[0]
	json_graph_row['nodeTo'] = row[1]
	json_graph_row['data'] = {}
	json_graph.append(json_graph_row)
# print json_graph
 	
out_graph = json.dumps(json_graph, indent=4)
header = 'var json = [ { "adjacencies": '
footer = '} ]'
#File operations
filename = "graph.dat"

FILE = open(filename, "w")
FILE.writelines(header)
FILE.writelines(out_graph)
FILE.writelines(footer)

# print json_graph
# filename = "json_graph.txt"
