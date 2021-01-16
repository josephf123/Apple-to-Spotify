import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
import re
import difflib

# Keys that are required for requests to be made, stored as environment variables
spotipy_client_id = os.environ["SPOTIPY_CLIENT_ID"]
spotipy_client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
spotipy_redirect_uri = os.environ["SPOTIPY_REDIRECT_URI"]

# Get html from the website of the playlist and place it into a file called doc.html
f = open("doc.html", "r")
newFile = f.read()
soup = BeautifulSoup(newFile, "html.parser")

# Locate the div that contains the song name and artist name
songInfo = soup.find_all(class_="song-name-wrapper")
songInfoArr = []

for x in songInfo:
    song = "".join(x.contents[1].stripped_strings)
    artist = "".join(x.contents[3].stripped_strings)
    if "," in artist:
        # use only the main artist
        artist = artist.split(",")[0]
    ob = (song,artist)
    songInfoArr.append(ob)

# Permission of what the application can do
scope = 'playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

username = "_.joey._.f"
name = "Test Name"
# Create an empty playlist
playlist_id = sp.user_playlist_create(username, name, public=True, collaborative=False, description='')["id"]

foundTracks = []

for x in songInfoArr:
    found = False
    songName = x[0]
    artistName = x[1]
    queryString = "track:" + songName + " artist:" + artistName
    results = sp.search(q=queryString, type="track", limit=5)
    songList = results["tracks"]["items"]
    for song in songList:
        if (song["name"].upper() == songName.upper() and song["artists"][0]["name"].upper() == artistName.upper()):
            # If the song name and artist match exactly with the search result, add id to foundTracks
            foundTracks.append(song["id"])
            found = True
            break
    if found != True:
        # If the song name and artist doesn't match exactly, execute below
        arr = []
        if songList == []:
            # Remove any parts of the song name that contain brackets or parenthesis
            res = re.findall(r"\(.*\)|\[.*\]", songName)
            print(res)
            for x in res:
                songName = songName.replace(x, "")
            results = sp.search(q=songName, type="track", limit=5)
            songList = results["tracks"]["items"]
        print(songName)
        for song in songList:
            name = song["name"]
            artist = song["artists"][0]["name"]
            songId = song["id"]
            pop = song["popularity"]
            ob = (name, artist, songId, pop)
            arr.append(ob) 
        print(arr)
        if len(arr) > 0:
            rating = []
            for x in arr:
                # Find the similarity between the search result and actual song
                songSimilarity = difflib.SequenceMatcher(None, x[0], songName).ratio()
                artistSimilarity = 2 * difflib.SequenceMatcher(None, x[1], artistName).ratio()
                popularity = x[3]
                val = songSimilarity * artistSimilarity * popularity
                rating.append(val)
            print(rating)
            # Find the index of the search result which has the highest rating
            maxIndex = rating.index(max(rating))
            # Add the search result with the highest rating
            foundTracks.append(arr[maxIndex][2])

pos = 0    
while len(foundTracks) > 0:
    firstHundred = foundTracks[:100]
    # Add the first hundred items of the array into the playlist
    sp.playlist_add_items(playlist_id,firstHundred, pos)
    # Remove the first hundred items from the array
    foundTracks = foundTracks[100:]
    pos += 100