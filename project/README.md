1. Run the python file parser.py. This file will pull a list of playlists from my spotify account. 
2. The program will then ask which numbered playlist you want to sort, and which playlists you want to sort into
    a. Use "2" for the first input, and "1 6 18 19 25 27 28 29 30" for the second input
    b. The number 2 playlist is my Flavor of the Year playlist with 400+ songs. The playlists for the second input are some of the playlists that center around a central category
    c. Some examples of the general categories for these playlists are metalcore, chill, soundtracks, rap.
3. The program will now pull all songs from the playlists that we are sorting into and pull features for each song.
4. It will then use these features (specified near the top of parser.py in a multi-line comment) to computer centroids for each playlist
5. I then loop through all songs in the playlist to sort and use Rocchio Classification to determine the most similar playlist to the song
6. The program will then ask you if you want to add the song to the playlist it recommends, if you don't it will move onto the next song.
7. I was not able to integrate the program with a discord bot or some other type of UI other than interactions in the command line
