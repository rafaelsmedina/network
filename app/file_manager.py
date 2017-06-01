import networkx as nx
import matplotlib.pyplot as plt

def read_artists_file(filename):
	file = open(filename, 'r')
	return file.read().splitlines()


def write_pickle_graph(artist_graph, title):
	nx.write_gpickle(artist_graph, "graph/" + title + ".gpickle")

def read_pickle_graph(title):
	return nx.read_gpickle("graph/" + title + ".gpickle")


def save_nodes_and_edges(artist_graph):
	nodes = []
	for artist in artist_graph.nodes():
		nodes.append({"name": artist})
	edges = []
	for edge in artist_graph.edges():
		artist1, artist2 = edge
		if artist1 != artist2:
			edges.append({"source": artist1, "target": artist2})

	nodes_file = open('graph/nodes.txt', 'w')
	for item in nodes:
  		print>>nodes_file, item

  	edges_file = open('graph/edges.txt', 'w')
  	for item in edges:
  		print>>edges_file, item


def print_network(artist_graph, title):
	pos = nx.spring_layout(artist_graph)
	colors = range(len(list(artist_graph.edges())))
	nx.draw(artist_graph, 
			pos,
			node_color='#A0CBE2',
			edge_color=colors,
			width=4,
			edge_cmap=plt.cm.Blues,
			with_labels=False)
	plt.savefig("graph/" + title + ".png")
	plt.show()