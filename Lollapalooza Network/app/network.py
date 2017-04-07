import spotify_access as sa
import networkx as nx
import file_manager as fm

#create connections
def connect_artist_to_neighbours(artist_name, artist_graph, artists_list=None, visited_artists=None):
	if ((visited_artists != None) and (artist_name not in visited_artists)) or (visited_artists == None):
		print 'Now working on...' + artist_name
		related_artists_list = sa.get_related_artists_from_name(artist_name)
		if related_artists_list != None:
			for related_artist in related_artists_list:
				if (artists_list == None) or (related_artist.encode('utf-8') in artists_list):
					related_artist = related_artist.encode('utf-8')
					artist_graph.add_edge(artist_name, related_artist)
		artist_graph.add_node(artist_name)
	return artist_graph

#get artist first degree connections
def create_network_from_artist_name(artist_name):
	artist_graph = nx.Graph()
	visited_artists = []
	artist_graph = connect_artist_to_neighbours(artist_name, artist_graph)
	visited_artists.append(artist_name)
	return artist_graph, visited_artists

#get next connections
def expand_network(artist_graph, visited_artists=None):
	artists_in_graph = list(artist_graph.nodes())
	for artist in artists_in_graph:
		connect_artist_to_neighbours(artist, artist_graph, None, visited_artists)
		if visited_artists != None:
			visited_artists.append(artist)
	return artist_graph, visited_artists

#find adjacent nodes
def artist_network(artist_name, iterations=0):
	artist_graph, visited_artists = create_network_from_artist_name(artist_name)
	for i in range(0, iterations):
		artist_graph, visited_artists = expand_network(artist_graph, visited_artists)
	return artist_graph

#connect artists in list
def list_network(artists_list):
	artist_graph = nx.Graph()
	for artist_name in artists_list:
		artist_graph = connect_artist_to_neighbours(artist_name, artist_graph, artists_list)
	return artist_graph