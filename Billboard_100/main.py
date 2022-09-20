import requests as requests
from bs4 import BeautifulSoup
import requests, os, spotipy, json, ast
from spotipy.oauth2 import SpotifyOAuth

user_year = input("What year would you like to travel to? Type date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{user_year}"
print(URL)

playlist_response = requests.get(URL)
web_page = playlist_response.text
soup = BeautifulSoup(web_page, "html.parser")

music_list_100 = soup.select("h3#title-of-a-story.c-title.lrv-u-font-size-16")
music_list_100 = [song.getText().strip() for song in music_list_100]
print(f"top 100 for {user_year} {music_list_100[:6]}")
# artist_list = soup.select("span.c-label.a-font-primary-s")
# artist_list = [tag.getText().strip() for tag in artist_list]
spotify_id = os.environ.get('SPOTIPY_CLIENT_ID')
spotify_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
spotify_uri = "http://example.com/"
scope = "user-library-read playlist-modify-private user-top-read user-read-recently-played"

spotify_oauth = SpotifyOAuth(client_id=spotify_id, client_secret=spotify_secret, redirect_uri=spotify_uri, scope=scope,
                             show_dialog=True, cache_path="token.txt")
sp = spotipy.Spotify(auth_manager=spotify_oauth)

user_id = sp.current_user()['id']
playlist_name = f"{user_year} Billboard 100"
body = {"name": playlist_name, "public": True}
with open("token.txt", "r") as connection:
    content = connection.read()
    print(type(content))
    js = ast.literal_eval(content)
    print(type(js))

access_token = js['access_token']
playlist_response = requests.post(url=f"https://api.spotify.com/v1/users/{user_id}/playlists",
                                  data=body,
                                  headers={"Content-Type": "application/json", "Authorisation": access_token})

print(playlist_response, playlist_response.text)

uri_list = []
for track in music_list_100:
    try:
        json = sp.search(q=track, limit=1)
        track_uri = json['tracks']['items'][0]['uri']
        uri_list.append(track_uri)
    except:
        print(f"Couldn't find '{track}' on Spotify")

print(uri_list)



# Everything works except Spotipy's create playlist method, and Spotify's own API for making a playlist doens't work either