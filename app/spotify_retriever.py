import requests
import json
import os


#get access token
def get_resquest_token():

	client_id = os.environ.get('SPOTIFY_CLIENT_ID')
	client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

	grant_type = 'client_credentials'

	body_params = {'grant_type' : grant_type}

	url = 'https://accounts.spotify.com/api/token'

	r = requests.post(url, data=body_params, auth = (client_id, client_secret))
	response = json.loads(r.text)
	
	return response['access_token']


#search artist
def search_artist(artist_name):
	token = get_resquest_token()
	r = requests.get('https://api.spotify.com/v1/search?q=' + artist_name + '&type=artist', 
		headers={"Authorization": "Bearer " + token})
	response = json.loads(r.text)
	return response

#get artist from id
def artist(artist_id):
	token = get_resquest_token()
	r = requests.get('https://api.spotify.com/v1/artists/' + artist_id, 
		headers={"Authorization": "Bearer " + token})
	response = json.loads(r.text)
	return response



#get artist's neighbours (from name)
def artist_related_artists(artist_name):
	token = get_resquest_token()

	r = requests.get('https://api.spotify.com/v1/search?q=' + artist_name + '&type=artist', 
		headers={"Authorization": "Bearer " + token})
	artist_id = json.loads(r.text)['artists']['items'][0]['id']

	r = requests.get('https://api.spotify.com/v1/artists/' + artist_id + '/related-artists', 
		headers={"Authorization": "Bearer " + token})
	response = json.loads(r.text)

	return response


#get artist's info and neighbours
def artist_all(artist_name, album_type=None, country=None, limit=None):

	parameters = '?'
	if album_type != None:
		parameters = parameters + 'album_type=' + album_type + '&'
	if country != None:
		parameters = parameters + 'market=' + country + '&'
	if limit == None:
		parameters = parameters + 'limit=20'
	else:
		parameters = parameters + 'limit=' + str(limit)

	token = get_resquest_token()

	r = requests.get('https://api.spotify.com/v1/search?q=' + artist_name + '&type=artist', 
		headers={"Authorization": "Bearer " + token})

	i = 0

	if len(json.loads(r.text)['artists']['items']) > 0:
		while i < len(json.loads(r.text)['artists']['items']) and (json.loads(r.text)['artists']['items'][i]['name'] != artist_name):
			i = i + 1

	 	artist_id = json.loads(r.text)['artists']['items'][i]['id']

		r_related = requests.get('https://api.spotify.com/v1/artists/' + artist_id + '/related-artists', 
			headers={"Authorization": "Bearer " + token})

		r_info = requests.get('https://api.spotify.com/v1/artists/' + artist_id, 
			headers={"Authorization": "Bearer " + token})
		
		r_albums = requests.get('https://api.spotify.com/v1/artists/' + artist_id + '/albums' + parameters, 
			headers={"Authorization": "Bearer " + token})

		info = json.loads(r_info.text)
		albums = json.loads(r_albums.text)
		related = json.loads(r_related.text)

		return info, albums, related
	else:
		return None, None, None

