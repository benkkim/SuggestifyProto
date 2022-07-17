class Track:
    #Information regarding the track
    def __init__(self, name, artist, id):
        self.name = name #Name of the track
        self.id = id #Spotify ID of the track
        self.artist = artist #Artist of the track

    def createSpotifyURI(self):
        #Creates a Spotify URI to communicate with the Spotify API
        return f"spotify:track:{self.id}"

    def __str__(self):
        #Returns the name of the track
        return f"{self.name} by {self.artist}"