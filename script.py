import os

from spotifyClient import SpotifyClient


def main():
    #initialize a spotify client
    spotifyClient = SpotifyClient(os.getenv("SPOTIFY_CLIENT_ID"), os.getenv("SPOTIFY_CLIENT_SECRET"))

    #get the user's last played tracks
    numTracks = int(input("How many tracks would you like to visualize?"))
    recentTracks = spotifyClient.getLastPlayedTracks(numTracks)

    print(f"Here are your {numTracks} most recent tracks:")
    for it, track, in enumerate(numTracks):
        print(f"{it+1}. {track.name} by {track.artist}")

    #user selects seed tracks
    indices = input("Enter a list of up to 10 tracks you'd like to base your recommendations on. Use indices separated by a space: ")
    indices = indices.split()
    seedTracks = [recentTracks[int(index) - 1] for index in indices]

    #get recommendations based off seed tracks
    recommendations = spotifyClient.getTrackRecommendations(seedTracks)
    print("Here are your recommendations based on your seed tracks:")
    for index, track in enumerate(recommendations):
        print(f"{index+1}. {track.name} by {track.artist}")
    
    #create a playlist with recommendation tracks
    playlistName = input("What would you like to name your playlist? ")
    playlist = spotifyClient.createPlaylist(playlistName)
    print(f"{playlist.name} was created successfully!")

    #add recommendations to playlist
    spotifyClient.addTracksToPlaylist(playlist, recommendations)
    print(f"Recommended tracks have been added to {playlist.name}")

    if __name__ == "__main__":
        main()