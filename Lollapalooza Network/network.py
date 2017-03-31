import spotipy
import networkx as nx
import matplotlib.pyplot as plt

#ARTISTS AND RELATED ONES FROM SPOTIFY
def search_artist(artist_name):
	spotify = spotipy.Spotify()
	results = spotify.search(q='artist:' + artist_name, type='artist')
	if len(results['artists']['items']) > 0:
		return results['artists']['items'][0]['id']
	return None


def get_related_artists(artist_id):
	spotify = spotipy.Spotify()
	if artist_id != None:
		related_artists_response = spotify.artist_related_artists(artist_id)

		related_artists_list = []
		for artist in related_artists_response['artists']:
			related_artists_list.append(artist['name'])
		return related_artists_list
	return None


def get_related_artists_from_name(artist_name):
	artist_id = search_artist(artist_name)
	return get_related_artists(artist_id)


#ARTISTS I WANT 
def read_artists_file(filename):
	file = open(filename, 'r')
	return file.read().splitlines()


#NETWORK
def create_artist_network(artist_name, artist_graph, lollapalooza_artists):
	print 'Now working on...' + artist_name
	related_artists_list = get_related_artists_from_name(artist_name)
	#artist_name = artist_name.decode('utf-8')
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

#PRINT
def print_network(artist_graph):
	G = artist_graph
	pos=nx.spring_layout(G)
	colors=range(len(list(G.edges())))
	nx.draw(G,pos,node_color='#A0CBE2',edge_color=colors,width=4,edge_cmap=plt.cm.Blues,with_labels=False)
	plt.savefig("edge_colormap.png") # save as png
	plt.show()


def initialize_and_save_graph():
	lollapalooza_artists = read_artists_file('artists.txt')
	artist_graph = create_network_from_list(lollapalooza_artists)
	write_pickle_graph(artist_graph, 'lolla')

#MAIN
def main():
	initialize_and_save_graph()
	g = read_pickle_graph('lolla')

if __name__ == "__main__":
	main()