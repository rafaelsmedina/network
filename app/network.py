import networkx as nx
from collections import Counter
import numpy

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

def read_datafile(filename, size=6):
	file = open(filename + '.txt', 'r').readlines()[0].split(',')
	data = []
	for item in file:
		i = item.split(':')
		data.append('{"id": ' + i[0].strip()[0:size] + ', "value":' + i[1] + '},')
	result_file = open(filename + '_result.txt', 'w')
	for item in data:
		print>>result_file, item


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

def closeness_of_each(g):
	return nx.closeness_centrality(g)


def betweenness_distribution(g):
	betweenness = nx.betweenness_centrality(g)
	betweenness_list = []
	for node in betweenness:
		betweenness_list.append(betweenness[str(node)])
	betweenness_distribution = Counter(betweenness_list)
	return betweenness_distribution

def betweenness_of_each(g):
	return nx.betweenness_centrality(g)


def degree_centrality_distribution(g):
	degree = nx.degree_centrality(g)
	degree_list = []
	for node in degree:
		degree_list.append(degree[str(node)])
	degree_distribution = Counter(degree_list)
	return degree_distribution

def degree_centrality_of_each(g):
	return nx.degree_centrality(g)


def diameter(g):
	return nx.diameter(g)


def calculate_centralities(name):
	g = pread(name)

	closeness = closeness_of_each(g)
	closeness_file = open(name + '/closeness_each_file.txt', 'w')
	closeness_file.write("%s\n" % closeness)
	closeness_file.close()
	print 'Closeness OK'

	betweenness = betweenness_of_each(g)
	betweenness_file = open(name + '/betweenness_each_file.txt', 'w')
	betweenness_file.write("%s\n" % betweenness)
	betweenness_file.close()
	print 'Betweenness OK'

	degree_cent = degree_centrality_of_each(g)
	degree_cent_file = open(name + '/degree_cent_each_file.txt', 'w')
	degree_cent_file.write("%s\n" % degree_cent)
	degree_cent_file.close()
	print 'Degree Centrality OK'

def calculate_centralities_all(names):
	for name in names:
		calculate_centralities(name)
		print "DONE!" + name


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



def pearson_correlation(filename1, filename2):
	file1 = open(filename1 + '.txt', 'r').readlines()[0].split(',')
	data1 = []
	for item in file1:
		i = item.split(':')
		data1.append(float(i[1]))

	data2 = []
	file2 = open(filename2 + '.txt', 'r').readlines()[0].split(',')
	for item in file2:
		i = item.split(':')
		data2.append(float(i[1]))

	print data1 == data2
	
	return numpy.corrcoef(data1, data2)