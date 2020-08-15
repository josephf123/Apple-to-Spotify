import spotipy
import spotipy.util as util
from requests import get
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import math
#url = "https://music.apple.com/au/playlist/luke-guess-the-song/pl.u-xlyNNYXuk76Rj6"
# Have to copy html and place it in a file because beautiful soup can't do it from the website directly as it is too large
f = open("innerhtml", "r")
content = f.read()
songList = []
artistList = []
songIDs = []
soup = BeautifulSoup(content, "html.parser")
track_ids = []

dataName = soup.find_all("span", class_="we-truncate we-truncate--single-line ember-view tracklist-item__text__headline targeted-link__target")

dataArtist = soup.find_all("a", class_="table__row__link table__row__link--secondary")

for songs in dataName:
    s = songs.get_text()
    s = (s[2:-1]).encode('ascii', 'ignore')
    songList.append(s)

for artist in dataArtist:
    a = artist.get_text()
    a = (a).encode('ascii', 'ignore')
    artistList.append(a)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def highestRatio(song, artist, item1, item2, item3):
    score1 = similar(item1['name'], song) + similar(item1['artists'][0]['name'], artist)
    score2 = similar(item2['name'], song) + similar(item2['artists'][0]['name'], artist)
    score3 = similar(item3['name'], song) + similar(item3['artists'][0]['name'], artist)
    array = [score1, score2, score3]
    highest = max(array)
    if highest == score1:
        return item1
    elif highest == score2:
        return item2
    elif highest == score3:
        return item3
    

scope = 'playlist-modify-public'
# my spotify id: vsGO3du0Rf227Todi1DrjA

token = util.prompt_for_user_token("_.joey._.f", scope)

#export SPOTIPY_CLIENT_ID='bcb23e6549cd447481429fb268e95407'
#export SPOTIPY_CLIENT_SECRET='2e3a8368964b4eaf83de80b6340f8e9a'
#export SPOTIPY_REDIRECT_URI='http://www.google.com/'
def findID(songName, artistName):
    sp = spotipy.Spotify(auth=token)
    query = str(songName) + " " + str(artistName)
    results = sp.search(q=query, type="track")
    if len(results['tracks']['items']) == 0:
        print "hi"
        query = str(songName)
        results = sp.search(q=query, type="track")
        if len(results['tracks']['items']) == 0:
            return  
    if len(results['tracks']['items']) == 1:
        item1 = results['tracks']['items'][0]
        item2 = results['tracks']['items'][0]
        item3 = results['tracks']['items'][0]  

    elif len(results['tracks']['items']) == 2:
        item1 = results['tracks']['items'][0]
        item2 = results['tracks']['items'][1]
        item3 = results['tracks']['items'][1]
    else:
        item1 = results['tracks']['items'][0]
        item2 = results['tracks']['items'][1]
        item3 = results['tracks']['items'][2]

    desired = highestRatio(songName, artistName, item1, item2, item3)
    desiredID = desired['id']
    track_ids.append(desiredID.encode('ascii', 'ignore'))
    return desiredID
name = "Moving on up 2.5 by Fin"
username = "_.joey._.f"

def cutArray(array, length):
    cut = int(math.ceil(length/100)) + 1
    for x in range(cut):
        loopStart = (x) * 100
        loopEnd = (x+1) * 100
        sp.user_playlist_add_tracks(username, playlist_id, array[loopStart:loopEnd])
if token:
    sp = spotipy.Spotify(auth=token)
    sp.user_playlist_create(username, name)
    result = sp.user_playlists(username)
    for x in range(len(result['items'])):
        if result['items'][x]['name'] == name:
            playlist_id = result['items'][x]['id']
    for x in range(len(songList)):
        print songList[x], artistList[x]
        print findID(songList[x], artistList[x])

    cutArray(track_ids, len(track_ids))
    print track_ids
    


else:
    print "Can't get token for", username

