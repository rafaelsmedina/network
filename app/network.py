import networkx as nx
from collections import Counter

def getnetwork(name):
	file = open(name + '/' + name + '.txt', 'r')
	nodes = file.readlines()
	g = nx.Graph()
	for i in nodes:
		j = i.split()
		g.add_edge(j[0], j[1])
	return g

#Write and read pickle
def pwrite(g, name):
	nx.write_gpickle(g, name + '/' + name + '.gpickle')

def pread(name):
	return nx.read_gpickle(name + '/' + name + '.gpickle')


def degree_distribution(g):
	degree = g.degree()
	degree_list = []
	for node in degree:
		degree_list.append(degree[str(node)])
	degree_distribution = Counter(degree_list)
	return degree_distribution


def clustering_distribution(g):
	clustering = nx.clustering(g)
	clustering_list = []
	for node in clustering:
		clustering_list.append(clustering[str(node)])
	clustering_distribution = Counter(clustering_list)
	return clustering_distribution


def subgraphs(g):
	components = nx.connected_component_subgraphs(g)
	sub_graphs = []
	for i, sg in enumerate(components):
		sub_graphs.append((i, sg.number_of_nodes(), sg.number_of_edges()))
	return sub_graphs #Component number, number of nodes, number of edges


def closeness_distribution(g):
	closeness = nx.closeness_centrality(g)
	closeness_list = []
	for node in closeness:
		closeness_list.append(closeness[str(node)])
	closeness_distribution = Counter(closeness_list)
	return closeness_distribution


def betweenness_distribution(g):
	betweenness = nx.betweenness_centrality(g)
	betweenness_list = []
	for node in betweenness:
		betweenness_list.append(betweenness[str(node)])
	betweenness_distribution = Counter(betweenness_list)
	return betweenness_distribution


def degree_centrality_distribution(g):
	degree = nx.degree_centrality(g)
	degree_list = []
	for node in degree:
		degree_list.append(degree[str(node)])
	degree_distribution = Counter(degree_list)
	return degree_distribution


def diameter(g):
	return nx.diameter(g)


def calculate(name):
	g = pread(name)

	degree = degree_distribution(g)
	degree_file = open(name + '/degree_file.txt', 'w')
	degree_file.write("%s\n" % degree)
	degree_file.close()
	print 'Degree OK'


	clustering = clustering_distribution(g)
	clustering_file = open(name + '/clustering_file.txt', 'w')
	clustering_file.write("%s\n" % clustering)
	clustering_file.close()
	print 'Clustering OK'


	this_subgraphs = subgraphs(g)
	this_subgraphs_file = open(name + '/subgraphs_file.txt', 'w')
	this_subgraphs_file.write("%s\n" % this_subgraphs)
	this_subgraphs_file.close()
	print 'Subgraphs OK'


	closeness = closeness_distribution(g)
	closeness_file = open(name + '/closeness_file.txt', 'w')
	closeness_file.write("%s\n" % closeness)
	closeness_file.close()
	print 'Closeness OK'


	betweenness = betweenness_distribution(g)
	betweenness_file = open(name + '/betweenness_file.txt', 'w')
	betweenness_file.write("%s\n" % betweenness)
	betweenness_file.close()
	print 'Betweenness OK'


	degree_cent = degree_centrality_distribution(g)
	degree_cent_file = open(name + '/degree_cent_file.txt', 'w')
	degree_cent_file.write("%s\n" % degree_cent)
	degree_cent_file.close()
	print 'Degree Centrality OK'

def calculate_all(names):
	for name in names:
		calculate(name)
		print "DONE!" + name