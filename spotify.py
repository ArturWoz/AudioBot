#coding: utf-8
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


"""
def searchYoutubeAlternative(songName):
    # YouTube will block you if you query too many songs using this search.
    textToSearch = songName
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = bs4(html, 'html.parser')
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        print('https://www.youtube.com' + vid['href'])


def searchYoutube(songName):
    api = youtube.API(client_id=APIs["youtube"]["client_id"],
              client_secret=APIs["youtube"]["client_secret"],
              api_key=APIs["youtube"]["api_key"])
    video = api.get('search', q=songName, maxResults=1, type='video', order='relevance')
    return("https://www.youtube.com/watch?v="+video["items"][0]["id"]["videoId"])

"""


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
