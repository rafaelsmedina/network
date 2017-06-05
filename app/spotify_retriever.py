import requests
import json
import os

def search_artist(artist_name):
	token = get_resquest_token()
	r = requests.get('https://api.spotify.com/v1/search?q=' + artist_name + '&type=artist', 
		headers={"Authorization": "Bearer " + token})
	response = json.loads(r.text)
	return response

def artist(artist_id):
	token = get_resquest_token()
	r = requests.get('https://api.spotify.com/v1/artists/' + artist_id, 
		headers={"Authorization": "Bearer " + token})
	response = json.loads(r.text)
	return response


def artist_related_artists(artist_id):
	token = get_resquest_token()
	r = requests.get('https://api.spotify.com/v1/artists/' + artist_id + '/related-artists', 
		headers={"Authorization": "Bearer " + token})
	response = json.loads(r.text)
	return response


def artist_albums(artist_id, album_type=None, country=None, limit=None):
	

	parameters = '&'

	#parameters
	if album_type != None:
		parameters = parameters + 'album_type=' + album_type + '&'
	if country != None:
		parameters = parameters + 'market=' + country + '&'
	if limit == None:
		parameters = parameters + 'limit=20'
	else:
		parameters = parameters + 'limit=' + limit

	token = get_resquest_token()
	r = requests.get('https://api.spotify.com/v1/artists/' + artist_id + '/albums', 
		headers={"Authorization": "Bearer " + token})
	response = json.loads(r.text)
	return response


def get_resquest_token():

	client_id = os.environ.get('SPOTIFY_CLIENT_ID')
	client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

	grant_type = 'client_credentials'

	body_params = {'grant_type' : grant_type}

	url = 'https://accounts.spotify.com/api/token'

	r = requests.post(url, data=body_params, auth = (client_id, client_secret))
	response = json.loads(r.text)
	
	return response['access_token']
