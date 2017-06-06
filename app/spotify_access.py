import spotify_retriever as sr


#gets only the artist id
def get_artist_id_from_name(artist_name):
	results = sr.search_artist(artist_name)
	if len(results['artists']['items']) > 0:
		return results['artists']['items'][0]['id']
	return None


#get info about the artist
def get_artist(artist_name):
	results = sr.search_artist(artist_name)
	if len(results['artists']['items']) > 0:
		return results['artists']['items'][0]
	return None	


def get_related_artists(artist_name, get_info=False):
	related_artists_response = sr.artist_related_artists(artist_name)
		
	if get_info:
		other_info = get_artist_info(artist_name)
	else:
		other_info = None

	related_artists_list = []

	for artist in related_artists_response['artists']:
		related_artists_list.append(artist['name'])

	return related_artists_list, other_info


def get_artist_info(artist_name):
	info = None

	if artist_name != None:

		artist, albums = sr.artist_info_and_albums(artist_name, album_type='album', country='BR', limit=50)
		albums_number = len(albums['items'])

		name = artist['name']
		genres = artist['genres']
		popularity = artist['popularity']

		info = (name, albums_number, genres, popularity)

	return info

def get_all_info(artist_name):
	artist, albums, related_artists_response = sr.artist_all(artist_name, album_type='album', country='BR', limit=50)

	albums_number = len(albums['items'])

	name = artist['name']
	genres = artist['genres']
	popularity = artist['popularity']

	info = (name, albums_number, genres, popularity)

	neighbours = []

	for artist in related_artists_response['artists']:
		neighbours.append(artist['name'])

	return info, neighbours