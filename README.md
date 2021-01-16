# Apple-to-Spotify

This python script enables the user to convert an Apple music playlist into a spotify playlist. This is done by using Beautiful soup to scrape the website with the Apple Music playlist and to then find it in Spotify using the Spotify API and Spotipy.


## Setup
To make this application work, the user must first go to the website in which the Apple music playlist is, inspect element and then copy the outerHTML of the body of the website. You must then create a new file labelled **"doc.html"** within the same folder as this script and paste. Run the script via the command line and it will prompt you to provide your spotify username as well as what you want the playlist to be called (Ensure you have the right username).
