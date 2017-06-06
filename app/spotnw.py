import spotify_access as sa
import networkx as nx
import file_manager as fm
import pickle
from collections import deque
import ipdb

VISITED_VERTICES_FILE='visited.txt'
KNOWN_VERTICES_FILE='known.txt'


def artist_network(artist_name, max_size=float('Inf'), getInfo=True):
	artists_info = []
	visited_artists = set()
	known_artists = set([artist_name])
	with open(KNOWN_VERTICES_FILE, 'w') as known_file:
            print>> known_file, artist_name

	# step 0: initialize unvisited artists
	unvisited_artists = deque([a for a in known_artists if a not in visited_artists])
        ipdb.set_trace()

	# step 1: create graph
	artist_graph = nx.DiGraph()

	# step 3: expand graph
	while artist_graph.size() < max_size and len(unvisited_artists) > 0:
		next_artist = unvisited_artists.popleft()
		print 'working on ' + next_artist
		artists_info, visited_artists, unvisited_artists, known_artists, artist_graph = visit_artist(
																		next_artist,
																		getInfo,
																		visited_artists,
																		unvisited_artists,
																		known_artists,
																		artists_info,
																		artist_graph)
		with open(VISITED_VERTICES_FILE,'a') as visited_file:
			print>> visited_file, next_artist

		if artist_graph.size() % 500 == 0:
			fm.write_pickle_graph(artist_graph, 'spotify_graph')

			#if graph_size % 2 == 0:
				#fm.write_pickle_graph(artist_graph, 'spotify_graph')
				#pickle.dump(visited_artists, open("visited", "w"))
				#pickle.dump(unvisited_artists, open("unvisited", "w"))
				#pickle.dump(artists_info, open("info", "w"))

	return artist_graph, artists_info


def visit_artist(artist_name, get_info, visited_artists, unvisited_artists, known_artists, artists_info, artist_graph):

	#get everything about artist
	artist_info, neighbours = sa.get_all_info(artist_name)

	#mark artist as visited
	visited_artists.add(artist_info[0])

	#save artists info
	artists_info.append(artist_info)

	with open(KNOWN_VERTICES_FILE, 'a') as known_file:
		for item in neighbours:
			#connect artist to neighbours
			artist_graph.add_edge(artist_info[0], item)
			if item not in known_artists:
				#saves list of neighbours that haven't been visited
				unvisited_artists.append(item)
				known_artists.add(item)
				print>> known_file, item

	return artists_info, visited_artists, unvisited_artists, known_artists, artist_graph

def restart_retrieving():

	artist_graph = fm.read_pickle_graph('spotify_graph')
	visited_artists = pickle.load(open("visited", "r" ))
	unvisited_artists = pickle.load(open("unvisited", "r" ))
	artists_info = pickle.load(open("info", "r" ))

	graph_size = len(visited_artists)
	while len(unvisited_artists) > 0:
		next_artist = unvisited_artists[0]
		print 'working on ' + next_artist
		artists_info, visited_artists, unvisited_artists, artist_graph = visit_artist(
																		next_artist,
																		True,
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
