from spotify_access import get_related_artists_from_name
import networkx as nx
from file_manager import read_artists_file, write_pickle_graph, read_pickle_graph,turn_graph_into_visualization_data, print_network

#NETWORK
def create_artist_network(artist_name, artist_graph, lollapalooza_artists):
	print 'Now working on...' + artist_name
	related_artists_list = get_related_artists_from_name(artist_name)
	if related_artists_list != None:
		for related_artist in related_artists_list:
			if related_artist.encode('utf-8') in lollapalooza_artists:
				related_artist = related_artist.encode('utf-8')
				artist_graph.add_edge(artist_name, related_artist)

	artist_graph.add_node(artist_name)
	return artist_graph


def expand_network(artist_graph, lollapalooza_artists):
	artists_list = list(artist_graph.nodes())
	for artist in artists_list:
		if artist in lollapalooza_artists:
			create_artist_network(artist, artist_graph, lollapalooza_artists)
	return artist_graph


def create_network(artist_name, lollapalooza_artists):
	artist_graph = nx.Graph()
	artist_graph = expand_network(create_artist_network(artist_name, artist_graph, lollapalooza_artists), lollapalooza_artists)
	return artist_graph

def create_network_from_list(lollapalooza_artists):
	artist_graph = nx.Graph()
	for artist_name in lollapalooza_artists:
		artist_graph = create_artist_network(artist_name, artist_graph, lollapalooza_artists)
	return artist_graph

#MAIN
def main():
	lollapalooza_artists = read_artists_file('static/artists.txt')
	artist_graph = create_network_from_list(lollapalooza_artists)
	write_pickle_graph(artist_graph, 'lolla')

if __name__ == "__main__":
	main()