from types import *
import network
import networkx as nx

def test_if_search_artist_returns_string(artist_name):
	assert type(network.search_artist(artist_name)) is unicode

def test_if_related_artists_returns_a_list(artist_id):
	assert type(network.get_related_artists(artist_id)) is list

def test_if_search_artist_returns_correct_id():
	assert network.search_artist('Lana del Rey') == '00FQb4jTyendYWaN8pK0wa'

def test_if_get_list_of_related_artists_returns_list(artist_name):
	assert type(network.get_related_artists_from_name(artist_name)) is list

def test_if_create_artist_graph_returns_a_graph(artist_name, artist_graph):
	assert type(network.create_artist_network(artist_name, artist_graph, [])) is nx.classes.graph.Graph

def test_if_artist_graph_has_nodes(artist_name, artist_graph):
	assert len(list(network.create_artist_network(artist_name, artist_graph, []).nodes())) > 0

def test_if_artist_graph_has_edges(artist_name, artist_graph):
	assert len(list(network.create_artist_network(artist_name, artist_graph, []).edges())) > 0

def test_if_expand_network_returns_a_different_network():
	test_graph = nx.Graph()
	test_graph.add_node('Lana del Rey')
	assert test_graph.nodes() != network.expand_network(test_graph, []).nodes()

def if_create_network_returns_a_network(artist_name):
	assert type(network.create_network(artist_name, [])) is nx.classes.graph.Graph

def run_all_tests():
	print 'Running all tests. It might take a while...'
	test_if_search_artist_returns_string('Lana del Rey')
	test_if_related_artists_returns_a_list('00FQb4jTyendYWaN8pK0wa')
	test_if_search_artist_returns_correct_id()
	test_if_get_list_of_related_artists_returns_list('Lana del Rey')
	test_if_create_artist_graph_returns_a_graph('Lana del Rey', nx.Graph())
	test_if_artist_graph_has_nodes('Lana del Rey', nx.Graph())
	test_if_artist_graph_has_edges('Lana del Rey', nx.Graph())
	test_if_expand_network_returns_a_different_network()
	if_create_network_returns_a_network('Lana del Rey')
	print 'All worked!'

def run_latest_tests():
	print 'Running latest tests...'
	if_create_network_returns_a_network('Lana del Rey')
	print 'All worked!'

def main():
	run_latest_tests()

if __name__ == "__main__":
	main()