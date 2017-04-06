import networkx as nx
import matplotlib.pyplot as plt

def read_artists_file(filename):
	file = open(filename, 'r')
	return file.read().splitlines()

def write_pickle_graph(artist_graph, title):
	nx.write_gpickle(artist_graph, title + ".gpickle")

def read_pickle_graph(title):
	return nx.read_gpickle(title + ".gpickle")

def turn_graph_into_visualization_data(artist_graph):
	nodes = []
	for artist in artist_graph.nodes():
		nodes.append({"name": artist})
	edges = []
	for edge in artist_graph.edges():
		artist1, artist2 = edge
		if artist1 != artist2:
			edges.append({"source": artist1, "target": artist2})
	return nodes, edges

def print_network(artist_graph):
	G = artist_graph
	pos=nx.spring_layout(G)
	colors=range(len(list(G.edges())))
	nx.draw(G,pos,node_color='#A0CBE2',edge_color=colors,width=4,edge_cmap=plt.cm.Blues,with_labels=False)
	plt.savefig("edge_colormap.png") # save as png
	plt.show()