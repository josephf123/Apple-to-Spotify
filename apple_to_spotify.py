#This program opens a text file called 'innerhtml' which is the html of a playlist link and searches for all the names of the songs and the respective artist and sends
#a request to a spotify api to search for the particular song, get it's id and add it to a playlist

#Environment variables were already declared
import spotipy
import spotipy.util as util
from requests import get
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import math
# Have to copy html and place it in a file because beautiful soup can't do it from the website directly as it is too large
f = open("innerhtml", "r")
content = f.read()
songList = []
artistList = []
songIDs = []
soup = BeautifulSoup(content, "html.parser")
track_ids = []

#Find all the song names from the innerhtml text file
dataName = soup.find_all("span", class_="we-truncate we-truncate--single-line ember-view tracklist-item__text__headline targeted-link__target")
#Find all the corresponding artists from the innerhtml text file
dataArtist = soup.find_all("a", class_="table__row__link table__row__link--secondary")

for songs in dataName:
    s = songs.get_text()
    s = (s[2:-1]).encode('ascii', 'ignore')
    #Add the song to a song list
    songList.append(s)

for artist in dataArtist:
    a = artist.get_text()
    a = (a).encode('ascii', 'ignore')
    #Add the artist to an artist list
    artistList.append(a)


def similar(a, b):
    #finds the similarity between two texts using difflib
    return SequenceMatcher(None, a, b).ratio()

def highestRatio(song, artist, item1, item2, item3):
    #Finds which item is the most similar to the actual song name and artist (which is gotten from the scraping)
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

#Allows for the program to manipulate the spotify users playlist
token = util.prompt_for_user_token("_.joey._.f", scope)

def findID(songName, artistName):
    sp = spotipy.Spotify(auth=token)
    query = str(songName) + " " + str(artistName)
    results = sp.search(q=query, type="track")
    if len(results['tracks']['items']) == 0:
        #If no results come from searching with the artist as well as the song name, the song name is tried by itself
        query = str(songName)
        results = sp.search(q=query, type="track")
        if len(results['tracks']['items']) == 0:
            #If there are no results, exit function
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
        #Gets the top three results from searching the spotify database
        item1 = results['tracks']['items'][0]
        item2 = results['tracks']['items'][1]
        item3 = results['tracks']['items'][2]
    #This is then compared with the actual song name and song's artist and the one with the highest score will be the desired
    desired = highestRatio(songName, artistName, item1, item2, item3)
    desiredID = desired['id']
    #The desired song's id is added to a track id list 
    track_ids.append(desiredID.encode('ascii', 'ignore'))
    return desiredID

nameofPlaylist = "A playlist converted from Apple Music"

username = "_.joey._.f"

def cutArray(array, length):
    #Because the api function can only take a maximum of 100 requests to add to a playlist, the 'add tracks' function had to be called multiple times if the length of the track list is > 100
    cut = int(math.ceil(length/100)) + 1
    for x in range(cut):
        loopStart = (x) * 100
        loopEnd = (x+1) * 100
        sp.user_playlist_add_tracks(username, playlist_id, array[loopStart:loopEnd])
if token:
    #If the user allows for the program to modify their spotify account
    sp = spotipy.Spotify(auth=token)
    sp.user_playlist_create(username, nameofPlaylist)
    result = sp.user_playlists(username)
    for x in range(len(result['items'])):
        #Searches all the playlists the user has and finds which one is the one songs need to be added to
        if result['items'][x]['name'] == name:
            playlist_id = result['items'][x]['id']
    cutArray(track_ids, len(track_ids))    
else:
    print "Can't get token for", username

