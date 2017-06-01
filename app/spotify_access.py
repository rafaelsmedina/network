import spotipy

spotify = spotipy.Spotify()

def get_artist_id_from_name(artist_name):
	spotify = spotipy.Spotify()
	results = spotify.search(q='artist:' + artist_name, type='artist')
	if len(results['artists']['items']) > 0:
		return results['artists']['items'][0]['id']
	return None


def get_related_artists(artist_id, get_info=False):
	if artist_id != None:
		related_artists_response = spotify.artist_related_artists(artist_id)
		
		if get_info:
			other_info = get_artist_info(artist_id)
		else:
			other_info = None

		related_artists_list = []

		for artist in related_artists_response['artists']:
			related_artists_list.append(artist['name'])

		return related_artists_list, other_info

	return None, None


def get_related_artists_from_name(artist_name, get_info=False):
	artist_id = get_artist_id_from_name(artist_name)
	return get_related_artists(artist_id, get_info)

def get_artist_info(artist_id):
	info = None

	if artist_id != None:
		albums_number = len(spotify.artist_albums(artist_id, album_type='album', country='BR', limit=50)['items'])
		artist = spotify.artist(artist_id)
		name = artist['name']
		genres = artist['genres']
		popularity = artist['popularity']
		info = (name, albums_number, genres, popularity)

	return info

def get_artist_info_by_name(artist_name):
	artist_id = get_artist_id_from_name(artist_name)
	return get_artist_info(artist_id)