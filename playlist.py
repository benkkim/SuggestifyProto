class Playlist:
    def __init__(self, name, id):
        self.name = name #Name of the playlist
        self.id = id #Spotify ID of the playlist


    def __str__(self):
        return f"Playlist: {self.name}"