from Classes import Song
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# SPOTIPY_CLIENT_ID='9a9006996b3447c99ccafa78766af60e'
# SPOTIPY_CLIENT_SECRET='12ce6ac5a2b54c95a1f521681827aab6'

auth_manager = SpotifyClientCredentials('9a9006996b3447c99ccafa78766af60e', '12ce6ac5a2b54c95a1f521681827aab6')
sp = spotipy.Spotify(auth_manager=auth_manager)

# examples for testing functions
example_artist = 'https://open.spotify.com/artist/1o2NpYGqHiCq7FoiYdyd1x'
example_track = 'https://open.spotify.com/track/5f2zZawBtGBEw24ABweErz'


def song_search(name: str) -> Song:
    """
    Takes a song name as a parameter, and outputs a Song object corresponding to the inputted song.

    - name: name of the song to search
    """
    results = sp.search(q=' track:' + name, type='track')
    if not results['tracks']['items']:
        raise Exception('Song Not Found')
    track_id = results['tracks']['items'][0]['id']
    track_name = results['tracks']['items'][0]['name']
    return get_features(track_name, track_id)


def song_search_id(name: str) -> str:
    """
    Takes a song name as a parameter, and outputs the id of the song from spotipy.

    - name: name of the song to search
    """
    results = sp.search(q=' track:' + name, type='track')
    if not results['tracks']['items']:
        raise Exception('Song Not Found')
    return results['tracks']['items'][0]['id']


def get_features(name: str, track: str) -> Song:
    """
    Helper function for song_search. Get audio features for a given track.
    Input the name of the track and it's id or url, and output a Song class object with the correct attributes
    for the given song.

    - name : name of the song
    - track : id or url of the song
    """
    tracks = [track]
    features = sp.audio_features(tracks)
    id = features[0]['id']
    ac = features[0]['acousticness']
    dance = features[0]['danceability']
    energy = features[0]['energy']
    ins = features[0]['instrumentalness']
    live = features[0]['liveness']
    speech = features[0]['speechiness']
    tempo = features[0]['tempo']
    val = features[0]['valence']

    return Song(id, name, ac, dance, energy, ins, live, speech, tempo, val)
