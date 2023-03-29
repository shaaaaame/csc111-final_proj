from Classes import Song, Graph
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# SPOTIPY_CLIENT_ID='9a9006996b3447c99ccafa78766af60e'
# export SPOTIPY_CLIENT_SECRET='12ce6ac5a2b54c95a1f521681827aab6'

auth_manager = SpotifyClientCredentials('9a9006996b3447c99ccafa78766af60e', '12ce6ac5a2b54c95a1f521681827aab6')
sp = spotipy.Spotify(auth_manager=auth_manager)

# playlists = sp.user_playlists('spotify')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None


example_artist = 'https://open.spotify.com/artist/1o2NpYGqHiCq7FoiYdyd1x'
example_track = 'https://open.spotify.com/track/5f2zZawBtGBEw24ABweErz'


def get_related_artists(artist: str):
    """
    Get related artists from the given artist
    """
    return_artists = []
    related = sp.artist_related_artists(artist)
    artists = related['artists']
    for r in range(len(artists)):
        return_artists.append(artists[r]['name'])
    return return_artists


def get_features(name: str, track: str) -> Song:
    """
    Get audio features for a given track. Input the name of the track and it's id or url, and output
    a Song class object with the correct attributes for the given song.
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


def song_search(name: str):
    """
    Search a song by the inputted name in the spotify api, and return a Song class object for the given song.
    """
    results = sp.search(q=' track:' + name, type='track')
    if not results['tracks']['items']:
        raise Exception('Song Not Found')
    track_id = results['tracks']['items'][0]['id']
    track_name = results['tracks']['items'][0]['name']
    return get_features(track_name, track_id)
