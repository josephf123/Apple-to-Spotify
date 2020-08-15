from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def highestRatio(song, artist, item1, item2, item3):
    score1 = similar(item1['name'], song) + similar(item1['artists'][0]['name'], artist)
    score2 = similar(item2['name'], song) + similar(item2['artists'][0]['name'], artist)
    score3 = similar(item3['name'], song) + similar(item3['artists'][0]['name'], artist)
    array = [score1, score2, score3]
    highest = max(array, key=lambda x: x[array])
    print highest


    