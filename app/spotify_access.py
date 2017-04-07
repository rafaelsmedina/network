import spotipy

def get_artist_id_from_name(artist_name):
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
	artist_id = get_artist_id_from_name(artist_name)
	return get_related_artists(artist_id)
