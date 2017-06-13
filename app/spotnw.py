
import spotify_access as sa
import networkx as nx
import file_manager as fm
import pickle
from collections import deque
#import ipdb

VISITED_VERTICES_FILE='visited.txt'
KNOWN_VERTICES_FILE='known.txt'
LAST_VISITED_FILE='last.txt'


def artist_network(artist_name, max_size=float('Inf'), getInfo=True):
	visited_artists = set()
	known_artists = set([artist_name])
	with open(KNOWN_VERTICES_FILE, 'w') as known_file:
            print>> known_file, artist_name.encode('utf-8')

	# step 0: initialize unvisited artists
	unvisited_artists = deque([a for a in known_artists if a not in visited_artists])
        #ipdb.set_trace()

	# step 1: create graph
	artist_graph = nx.DiGraph()

	# step 3: expand graph
	while artist_graph.size() < max_size and len(unvisited_artists) > 0:
		next_artist = unvisited_artists.popleft()
		print 'working on ' + next_artist
		visited_artists, unvisited_artists, known_artists, artist_graph = visit_artist(
																		next_artist,
																		getInfo,
																		visited_artists,
																		unvisited_artists,
																		known_artists,
																		artist_graph)
		with open(VISITED_VERTICES_FILE,'a') as visited_file:
			print>> visited_file, next_artist.encode('utf-8')

		if len(visited_artists) % 5 == 0:
			fm.write_pickle_graph(artist_graph, 'spotify_graph')
			pickle.dump(next_artist.encode('utf-8'), open(LAST_VISITED_FILE, "w"))

	fm.write_pickle_graph(artist_graph, 'spotify_graph_final')
	return artist_graph


def visit_artist(artist_name, get_info, visited_artists, unvisited_artists, known_artists, artist_graph):

	#get everything about artist
	artist_info, neighbours = sa.get_all_info(artist_name)

	#mark artist as visited
	visited_artists.add(artist_name)

	if artist_info != None:

		with open(KNOWN_VERTICES_FILE, 'a') as known_file:
			for item in neighbours:
				#connect artist to neighbours
				artist_graph.add_node(artist_name, info=artist_info)
				artist_graph.add_edge(artist_name, item)
				if item not in known_artists:
					#saves list of neighbours that haven't been visited
					unvisited_artists.append(item)
					known_artists.add(item)
					print>> known_file, item.encode('utf-8')

	return visited_artists, unvisited_artists, known_artists, artist_graph

def restart_retrieving():

	last_visited_artist = pickle.load(open(LAST_VISITED_FILE, "r"))

	visited_artists = set()

	visited_file = open(VISITED_VERTICES_FILE, 'r')

	for line in visited_file:
		artist = line.strip()
		if artist != last_visited_artist:
			visited_artists.add(artist)
		else:
			visited_artists.add(artist) 
			break

	known_artists = [line.strip() for line in open(KNOWN_VERTICES_FILE)]
	unvisited_artists = deque([a for a in known_artists if a not in visited_artists])
	known_artists = set(known_artists)

	artist_graph = fm.read_pickle_graph('spotify_graph')


	# step 3: expand graph
	while artist_graph.size() < float('Inf') and len(unvisited_artists) > 0:
		next_artist = unvisited_artists.popleft()
		print 'working on ' + next_artist
		visited_artists, unvisited_artists, known_artists, artist_graph = visit_artist(
																		next_artist,
																		True,
																		visited_artists,
																		unvisited_artists,
																		known_artists,
																		artist_graph)
		with open(VISITED_VERTICES_FILE,'a') as visited_file:
			print>> visited_file, next_artist
		if len(visited_artists) % 5 == 0:
			fm.write_pickle_graph(artist_graph, 'spotify_graph')
			pickle.dump(next_artist, open(LAST_VISITED_FILE, "w"))

	fm.write_pickle_graph(artist_graph, 'spotify_graph_final')
	return artist_graph



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
