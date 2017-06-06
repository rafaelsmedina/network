import spotify_access as sa
import networkx as nx
import file_manager as fm
import pickle


def artist_network(artist_name, max_size=None, getInfo=True):
	artists_info = None
	artists_info = []

	visited_artists = []
	unvisited_artists = []

	# step 1: create graph
	artist_graph = nx.DiGraph()

	# step 2: 1st iteration
	print 'working on ' + artist_name
	artists_info, visited_artists, unvisited_artists, artist_graph = visit_artist(
																		artist_name, 
																		getInfo, 
																		visited_artists, 
																		unvisited_artists, 
																		artists_info, 
																		artist_graph)

	
	# step 3: expand graph
	if max_size != None:
		graph_size = 1
		while graph_size < max_size:
			next_artist = unvisited_artists[0]
			print 'working on ' + next_artist
			artists_info, visited_artists, unvisited_artists, artist_graph = visit_artist(
																			next_artist, 
																			getInfo, 
																			visited_artists, 
																			unvisited_artists, 
																			artists_info, 
																			artist_graph)
			graph_size = graph_size + 1

	else:
		graph_size = 1
		while len(unvisited_artists) > 0:
			next_artist = unvisited_artists[0]
			print 'working on ' + next_artist
			artists_info, visited_artists, unvisited_artists, artist_graph = visit_artist(
																			next_artist, 
																			getInfo, 
																			visited_artists, 
																			unvisited_artists, 
																			artists_info, 
																			artist_graph)
			graph_size = graph_size + 1
			if graph_size % 2 == 0:
				fm.write_pickle_graph(artist_graph, 'spotify_graph')
				pickle.dump(visited_artists, open("visited", "w"))
				pickle.dump(unvisited_artists, open("unvisited", "w"))
				pickle.dump(artists_info, open("info", "w"))

	return artist_graph, artists_info


def visit_artist(artist_name, get_info, visited_artists, unvisited_artists, artists_info, artist_graph):
	
	#get everything about artist
	artist_info, neighbours = sa.get_all_info(artist_name)

	#mark artist as visited
	visited_artists.append(artist_info[0])

	if artist_info[0] in unvisited_artists:
		unvisited_artists.remove(artist_info[0])

	#save artists info
	artists_info.append(artist_info)

	for item in neighbours:
		#connect artist to neighbours
		artist_graph.add_edge(artist_info[0], item)
		if (item not in visited_artists) and (item not in unvisited_artists):
			#saves list of neighbours that haven't been visited
			unvisited_artists.append(item)

	return artists_info, visited_artists, unvisited_artists, artist_graph

def restart_retrieving():

	artist_graph = lm.read_pickle_graph('spotify_graph')
	visited_artists = pickle.load(open("visited", "r" ))
	unvisited_artists = pickle.load(open("unvisited", "r" ))
	artists_info = pickle.load(open("info", "r" ))

	graph_size = len(visited_artists)
		while len(unvisited_artists) > 0:
			next_artist = unvisited_artists[0]
			print 'working on ' + next_artist
			artists_info, visited_artists, unvisited_artists, artist_graph = visit_artist(
																			next_artist, 
																			getInfo, 
																			visited_artists, 
																			unvisited_artists, 
																			artists_info, 
																			artist_graph)
			graph_size = graph_size + 1
			if graph_size % 2 == 0:
				fm.write_pickle_graph(artist_graph, 'spotify_graph')
				pickle.dump(visited_artists, open("visited", "w"))
				pickle.dump(unvisited_artists, open("unvisited", "w"))
				pickle.dump(artists_info, open("info", "w"))

	return artist_graph, artists_info



#get info from unvisited nodes
def get_rest_of_info(artist_graph, artists_info, visited_artists):
	print 'Getting info from unvisited nodes...'
	artists_in_graph = list(artist_graph.nodes())
	
	for artist in artists_in_graph:
		if artist not in visited_artists:
			info = sa.get_artist_info(artist)
			visited_artists.append(artist)
			artists_info.append(info)

	return artist_graph, artists_info