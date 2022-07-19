import json
import requests
from track import Track
from playlist import Playlist

class SpotifyClient: 
    #Spotify Client that handles all the communication and operations with the Spotify API'
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.getToken()
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def getAPIRequest(self, url):
        response = requests.get(
            url, 
            headers = {
                "Content-Type": "application/json", 
                "Authorization": f"Bearer {self.client_id}"
            }
        )
        return response
    
    def getLastPlayedTracks(self, limit = 25):
        #Returns the user's last played tracks 
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self.getAPIRequest(url)
        responseJSON = response.json()
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) 
                    for track in responseJSON["items"]]
        return tracks

    def getTrackRecommendations(self, seedTracks, limit = 50):
        #Returns a list of recommended tracks based on seed tracks
        seedTracksURL = ""
        for seedTrack in seedTracks:
            seedTracksURL += seedTrack.id + ","
        seedTracksURL = seedTracksURL[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seedTracksURL}&limit={limit}"
        response = self.getAPIRequest(url)
        responseJSON = response.json()
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for 
                    track in responseJSON["tracks"]]
        return tracks

    def createPlaylist(self, name):
        #creates playlist based on recommendations
        data = json.dumps({
            "name": name,
            "description": "Recommended tracks based on your listening history",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = self.postAPIRequest(url, data)
        responseJSON = response.json()

        playlistID = responseJSON["id"]
        playlist = Playlist(name, playlistID)
        return playlist

    def postAPIRequest(self, url, data):
        response = requests.post(
            url, 
            data = data, 
            headers = {
                "Content-Type": "application/json", 
                "Authorization": f"Bearer {self.client_id}"
            }
        )

    def addTracksToPlaylist(self, playlist, tracks):
        #Adds tracks to playlist
        tracksURIS = [track.createURI() for track in tracks]
        data = json.dumps(tracksURIS)
        url = f"https://api.spotify.com/v1/{playlist.id}/tracks"
        response = self.postAPIRequest(url, data)
        return response.json()