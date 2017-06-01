import spotify_access as sa
import networkx as nx
import file_manager as fm

#create connections
def connect_artist_to_neighbours(artist_name, artist_graph, artists_list=None, visited_artists=None, artists_info=None, get_info=False):
	if ((visited_artists != None) and (artist_name not in visited_artists)) or (visited_artists == None):

		print 'Now working on...' + artist_name

		related_artists_list, other_info = sa.get_related_artists_from_name(artist_name, get_info)

		if related_artists_list != None:
			for related_artist in related_artists_list:
				if (artists_list == None) or (related_artist.encode('utf-8') in artists_list):
					related_artist = related_artist.encode('utf-8')
					artist_graph.add_edge(artist_name, related_artist)

		if get_info:
			artists_info.append(other_info)

		artist_graph.add_node(artist_name)

	return artist_graph, artists_info

#get artist first degree connections
def create_network_from_artist_name(artist_name, get_info=False):
	artist_graph = nx.Graph()

	artists_info = None
	if get_info:
		artists_info = []

	visited_artists = []

	artist_graph, artists_info = connect_artist_to_neighbours(artist_name, artist_graph, None, visited_artists, artists_info, get_info)

	visited_artists.append(artist_name)

	return artist_graph, visited_artists, artists_info

#get next connections
def expand_network(artist_graph, visited_artists=None, artists_info=None, get_info=False):
	artists_in_graph = list(artist_graph.nodes())

	for artist in artists_in_graph:
		artist_graph, artists_info = connect_artist_to_neighbours(artist, artist_graph, None, visited_artists, artists_info, get_info)

		if visited_artists != None:
			visited_artists.append(artist)

	return artist_graph, visited_artists, artists_info

#find adjacent nodes
def artist_network(artist_name, iterations=0, get_info=False):

	artists_info = None
	if get_info:
		artists_info = []

	artist_graph, visited_artists, artists_info = create_network_from_artist_name(artist_name, get_info)

	for i in range(0, iterations):
		artist_graph, visited_artists, artists_info = expand_network(artist_graph, visited_artists, artists_info, get_info)

	if get_info:
		artist_graph, artists_info = get_rest_of_info(artist_graph, artists_info, visited_artists)

	return artist_graph, artists_info

#connect artists in list
def list_network(artists_list, get_info=False):
	artist_graph = nx.Graph()

	if get_info:
		artists_info = []
	else:
		artists_info = None

	for artist_name in artists_list:
		artist_graph, artists_info = connect_artist_to_neighbours(artist_name, artist_graph, artists_list, None, artists_info, get_info)
	return artist_graph, artists_info

#get info from unvisited nodes
def get_rest_of_info(artist_graph, artists_info, visited_artists):
	print 'Getting info from unvisited nodes...'
	artists_in_graph = list(artist_graph.nodes())
	
	for artist in artists_in_graph:
		if artist not in visited_artists:
			info = sa.get_artist_info_by_name(artist)
			visited_artists.append(artist)
			artists_info.append(info)

	return artist_graph, artists_info