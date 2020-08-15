from requests import get
from bs4 import BeautifulSoup
#url = "https://music.apple.com/au/playlist/luke-guess-the-song/pl.u-xlyNNYXuk76Rj6"
f = open("innerhtml", "r")
content = f.read()
songList = []
artistList = []

soup = BeautifulSoup(content, "html.parser")
# class has the thing below for title
# tracklist-item__text__headline targeted-link__target

#class has the thing below for the artist
# data-test-song-artist-url


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
print songList
print artistList


