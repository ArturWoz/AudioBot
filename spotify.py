import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pytubefix as pytube


def url_from_yt_object(youtube):
    start = 'videoId='
    end = '>'
    s = str(youtube)
    s2 = 'https://www.youtube.com/watch?v=' + s[s.find(start) + len(start):s.rfind(end)]
    print(s2)
    return s2


# Opening our JSON configuration file (which has our tokens).
with open("config.json", encoding='utf-8-sig') as json_file:
    APIs = json.load(json_file)


def getTracks(playlistURL):
    # Creating and authenticating our Spotify app.
    client_credentials_manager = SpotifyClientCredentials(APIs["spotify"]["client_id"], APIs["spotify"]["client_secret"])
    client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Getting a playlist.
    results = client.playlist_items(playlistURL, additional_types=('track',))['items']
    for i in results:
        print(i)

    trackList = []
    # For each track in the playlist.
    for i in results:
        # In case there's only one artist.
        if (i["track"]["artists"].__len__() == 1):
            # We add trackName - artist.
            trackList.append(i["track"]["name"] + " - " + i["track"]["artists"][0]["name"])
        # In case there's more than one artist.
        else:
            nameString = ""
            # For each artist in the track.
            for index, b in enumerate(i["track"]["artists"]):
                nameString += (b["name"])
                # If it isn't the last artist.
                if (i["track"]["artists"].__len__() - 1 != index):
                    nameString += ", "
            # Adding the track to the list.
            trackList.append(i["track"]["name"] + " - " + nameString)

    return trackList


def spotify_list(url):
    tracks = getTracks(url)
    print("Searching songs...")
    songs = []
    for i in tracks:
        print(i)
        s = pytube.Search(i)
        url = url_from_yt_object(s.videos[0])
        songs.append(url)
    return songs
