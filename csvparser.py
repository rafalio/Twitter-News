import csv, json
graph = []
with open('blah.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        graph.append(row)

master = []
dataset = {}
adjacencies = []
for row in graph:
	adjancency_row = {}
	adjancency_row['nodeFrom'] = row[0]
	adjancency_row['nodeTo'] = row[1]
	adjancency_row['data'] = {}
	adjacencies.append(adjancency_row)
dataset['adjacencies'] = adjacencies
dataset['data'] = {
			          "$color": "#C74243",
			          "$type": "star",
			          "$dim": 8
			        }
dataset['id'] = "kurwa"
dataset['name'] = "kurwaSzymanski"
master.append(dataset);

# Save json as string
filename = "setJsonAs"
FILE = open(filename, "w")
FILE.writelines(json.dumps(master, indent=4))


# print jsonArray
 	


#		 {
#         "adjacencies": [],
#         "data": {
#           "$color": "#C74243",
#           "$type": "star",
#           "$dim": 8
#         },
#         "id": "graphnode20",
#         "name": "graphnode20"
#       }

# 
# 
# 
# 
# out_graph = json.dumps(jsonArray, indent=4)
# header = 'var json = [ { "adjacencies": '
# footer = '} ]'
# #File operations
# filename = "graph.dat"
# 
# FILE = open(filename, "w")
# FILE.writelines(header)
# FILE.writelines(out_graph)
# FILE.writelines(footer)

# print graph
# filename = "graph.txt"
